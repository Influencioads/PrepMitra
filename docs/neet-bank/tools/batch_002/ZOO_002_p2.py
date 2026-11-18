"""Builder for package ZOO_002_p2 of BATCH_002 (Zoology, 127 questions, NEET_ZOO_000374..NEET_ZOO_000500).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_002/ZOO_002_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_002_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_002_ZOO_p2.json"
FIRST_ID = 374

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
# HR: 10 primary spermatocytes -> 2 secondary spermatocytes each -> 4 spermatids each; each spermatid has 23
spermatids = 10 * 2 * 2
assert spermatids == 40 and spermatids * 23 == 920           # correct: 920
assert spermatids * 46 == 1840                                # distractor: spermatids taken as diploid
assert 10 * 2 * 23 == 460                                     # distractor: stopped at secondary spermatocytes
assert 10 * 23 == 230                                         # distractor: one haploid cell per spermatocyte

# EVO: N = 10,000, 9,100 show the dominant phenotype -> q^2 = 0.09, q = 0.3, p = 0.7
N_pop = 10_000
q2 = F(N_pop - 9_100, N_pop)
qe = F(3, 10)
assert qe * qe == q2
pe = 1 - qe
assert pe * pe * N_pop == 4_900                              # correct: AA = 4,900
assert 2 * pe * qe * N_pop == 4_200                          # distractor: heterozygotes
assert F(91, 100) ** 2 * N_pop == 8_281                      # distractor: squared the dominant-phenotype frequency
assert pe * N_pop == 7_000                                    # distractor: used p instead of p^2

# EVO: 2pq = 0.48 with p > q -> p = 0.6, q = 0.4 (the only split of p + q = 1 with 2pq = 0.48 and p > q)
roots = [F(k, 10) for k in range(11) if 2 * F(k, 10) * (1 - F(k, 10)) == F(48, 100)]
assert roots == [F(4, 10), F(6, 10)]
pp, qq = max(roots), min(roots)
assert qq * qq == F(16, 100)                                  # correct: q^2 = 0.16
assert pp * pp == F(36, 100) and pp * qq == F(24, 100) and pp * pp + qq * qq == F(52, 100)  # distractors

# EVO: earth about 4.5 billion years old; life appeared about 500 million years later
assert F(45, 10) - F(5, 10) == 4                              # correct: about 4 billion years ago
assert F(45, 10) + F(5, 10) == 5 and F(45, 10) - F(5, 100) == F(445, 100)  # distractors: added; 50 million

# BPP: circular plasmid of 6,000 bp, sites at 1,000 and 2,500 -> two fragments
plasmid, s1, s2 = 6_000, 1_000, 2_500
circ = sorted([s2 - s1, plasmid - (s2 - s1)])
assert circ == [1_500, 4_500] and sum(circ) == plasmid        # correct
assert sorted([s1, s2 - s1, plasmid - s2]) == [1_000, 1_500, 3_500]  # distractor: treated as linear

# BPP: linear 10 kb DNA, EcoRI at 2 and 7 kb, BamHI at 5 kb, double digest -> bands of distinct size
cuts = [0, 2, 5, 7, 10]
frags = [b - a for a, b in zip(cuts, cuts[1:])]
assert frags == [2, 3, 2, 3] and sum(frags) == 10 and len(set(frags)) == 2   # correct: 2 bands
assert len(frags) == 4                                        # distractor: one band per fragment

# ================================================================ Chemical Coordination and Integration (5/6/5)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "The hypothalamus contains several groups of neurosecretory cells, which produce hormones that regulate the "
  "synthesis and secretion of pituitary hormones. These groups of cells are called:",
  "Hypothalamus as an endocrine structure",
  "The hypothalamus, the basal part of the diencephalon, contains several groups of neurosecretory cells called "
  "nuclei. They produce releasing and inhibiting hormones that regulate the pituitary.",
  ["Hypothalamus → groups of neurosecretory cells", "These groups are called nuclei",
   "Their hormones: releasing hormones and inhibiting hormones"],
  "The hypothalamus",
  at="A", correct="Nuclei", wrong=["Ganglia", "Islets", "Follicles"],
  why="Ganglia are clusters of neuron cell bodies outside the CNS; islets are the endocrine units of the pancreas; "
      "follicles are the units of the thyroid and ovary.", secs=25)

Z(CCI, "Mechanism of hormone action", B, D,
  "According to the definition used in NCERT, hormones are:",
  "Definition of hormones",
  "Hormones are non-nutrient chemicals which act as intercellular messengers and are produced in trace amounts. "
  "They are carried to target organs, which may be far from the gland that secretes them.",
  ["Non-nutrient chemicals", "Intercellular messengers", "Produced in trace amounts"],
  "Endocrine glands and hormones",
  at="B", correct="Non-nutrient chemicals that act as intercellular messengers and are produced in trace amounts",
  wrong=["Nutrient chemicals that are produced in large amounts and stored in the target organ",
         "Enzymes poured by exocrine glands into ducts",
         "Chemicals that act only inside the cell that produces them"],
  why="Hormones are not nutrients and are made in trace amounts; enzymes in ducts are exocrine secretions; a "
      "hormone acts as an intercellular messenger, not only inside its own cell.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "The thyroid gland has two lobes located on either side of the trachea. The two lobes are interconnected by a thin "
  "flap of connective tissue called the:",
  "Structure of the thyroid gland",
  "The thyroid has two lobes on either side of the trachea, joined by a thin flap of connective tissue called the "
  "isthmus. The gland is made of follicles and stromal tissue.",
  ["Two lobes on either side of the trachea", "Joined by the isthmus"],
  "Thyroid gland",
  at="C", correct="Isthmus", wrong=["Infundibulum", "Pars intermedia", "Sella turcica"],
  why="The infundibulum is the funnel-shaped part of the oviduct; the pars intermedia is part of the pituitary; the "
      "sella turcica is the bony cavity that holds the pituitary.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "The adrenal cortex is divided into three layers. The innermost layer is the:",
  "Layers of the adrenal cortex",
  "The adrenal cortex has three layers: the zona reticularis (inner layer), the zona fasciculata (middle layer) "
  "and the zona glomerulosa (outer layer). The adrenal medulla lies at the centre, inside the cortex.",
  ["Outer → zona glomerulosa", "Middle → zona fasciculata", "Inner → zona reticularis"],
  "Adrenal gland",
  at="D", correct="Zona reticularis", wrong=["Zona glomerulosa", "Zona fasciculata", "Zona pellucida"],
  why="The zona glomerulosa is the outer layer and the zona fasciculata the middle layer; the zona pellucida is a "
      "membrane around the oocyte, not part of the adrenal gland.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "The pancreas is a composite gland. Its islets of Langerhans, about 1 to 2 million in a normal human pancreas, "
  "represent what proportion of the pancreatic tissue?",
  "Endocrine pancreas",
  "The endocrine pancreas consists of 'Islets of Langerhans'. There are about 1 to 2 million islets in a normal "
  "human pancreas, representing only 1 to 2 per cent of the pancreatic tissue; the rest is exocrine.",
  ["Islets: about 1–2 million in number", "They form only 1–2 per cent of pancreatic tissue"],
  "Pancreas",
  at="A", correct="Only 1 to 2 per cent", wrong=["About 20 per cent", "About half", "About 98 per cent"],
  why="The islets are a tiny endocrine fraction; most of the pancreas is exocrine tissue, so 20 %, half or 98 % "
      "are all far too high.", secs=25)

Z(CCI, "Hypothalamus and pituitary", I, STP,
  SP("Oxytocin acts on the smooth muscles of the body and stimulates their contraction.",
     "Vasopressin is stored in and released from the posterior pituitary, and it increases diuresis."),
  "Hormones released by the neurohypophysis",
  "Oxytocin acts on smooth muscles and stimulates their contraction (in women, vigorous contraction of the uterus at "
  "child birth and milk ejection from the mammary gland). Vasopressin (ADH) is indeed released from the posterior "
  "pituitary, but it acts on the kidney and stimulates resorption of water and electrolytes by the distal tubules, "
  "thereby REDUCING loss of water through urine (diuresis).",
  ["Statement I: true", "Statement II: false, because vasopressin is antidiuretic: it reduces diuresis"],
  "The pituitary gland", ans="C",
  why="Statement II fails only on its last part (increases diuresis), so 'both true' is wrong; Statement I is a "
      "direct NCERT line, so the options calling it false are wrong.", secs=40)

Z(CCI, "Thyroid, parathyroid and pineal", A, MUL,
  MS("Which of the following statements about the thyroid hormones are correct?",
     ["They play an important role in the regulation of the basal metabolic rate.",
      "They support the process of red blood cell formation.",
      "They control the metabolism of carbohydrates, proteins and fats.",
      "Maintenance of water and electrolyte balance is also influenced by them.",
      "Thyroxine (T₄) and triiodothyronine (T₃) are synthesised by the stromal tissue of the thyroid."]),
  "Functions of thyroid hormones",
  "The follicular cells of the thyroid synthesise thyroxine (T₄) and triiodothyronine (T₃). These hormones regulate "
  "the basal metabolic rate, support red blood cell formation, control the metabolism of carbohydrates, proteins and "
  "fats, and influence the maintenance of water and electrolyte balance.",
  ["(a) True", "(b) True", "(c) True", "(d) True",
   "(e) False: T₄ and T₃ are made by the follicular cells, not the stromal tissue"],
  "Thyroid gland",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (e) only", "(b), (c) and (d) only"],
  why="Any option with (e) is wrong because the hormones come from follicular cells; (b), (c) and (d) only leaves "
      "out the BMR role, which NCERT states first.", secs=60)

Z(CCI, "Adrenal, pancreas and gonads", I, MAT,
  ML(("hormone", "action"), ["Progesterone", "Estrogen", "Oxytocin", "Thymosins"],
     ["Differentiation of T-lymphocytes",
      "Vigorous contraction of the uterus at child birth",
      "Formation of alveoli in the mammary glands and milk secretion",
      "Appearance of female secondary sex characters such as a high-pitched voice"]),
  "Actions of selected hormones",
  "Progesterone acts on the mammary glands and stimulates the formation of alveoli (sac-like structures that store "
  "milk) and milk secretion. Estrogens bring about female secondary sex characters (for example, high pitch of "
  "voice). Oxytocin stimulates vigorous contraction of the uterus at child birth. Thymosins from the thymus play a "
  "major role in the differentiation of T-lymphocytes.",
  ["Progesterone → alveoli formation and milk secretion (III)", "Estrogen → secondary sex characters (IV)",
   "Oxytocin → uterine contraction at child birth (II)", "Thymosins → T-lymphocyte differentiation (I)"],
  "Thymus gland; Gonads; The pituitary gland",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="The commonest slip is swapping progesterone and estrogen; the other codes give oxytocin or progesterone the "
      "wrong action or send thymosins to the uterus.", secs=50)

Z(CCI, "Adrenal, pancreas and gonads", I, ASR,
  AR("Adrenaline (epinephrine) and noradrenaline (norepinephrine) are commonly called catecholamines.",
     "Adrenaline and noradrenaline are secreted by the zona glomerulosa of the adrenal cortex."),
  "Hormones of the adrenal medulla",
  "The adrenal medulla secretes adrenaline and noradrenaline, commonly called catecholamines. The adrenal cortex "
  "(including its outer zona glomerulosa) secretes corticoids, not catecholamines.",
  ["A: true (NCERT term)", "R: false, because catecholamines come from the adrenal medulla, not the cortex"],
  "Adrenal gland", ans="C",
  why="R is false, so neither 'both true' option can be correct; A is a direct NCERT statement, so 'A is false' "
      "is wrong.", secs=40)

Z(CCI, "Thyroid, parathyroid and pineal", I, STP,
  SP("In humans, four parathyroid glands are present on the back side of the thyroid gland, one pair each in the two "
     "lobes of the thyroid.",
     "Thyrocalcitonin (TCT), a protein hormone secreted by the thyroid gland, also regulates the blood calcium level."),
  "Parathyroid glands and calcium regulation",
  "NCERT describes four parathyroid glands on the back side of the thyroid, one pair in each lobe. The thyroid also "
  "secretes thyrocalcitonin, a protein hormone that regulates blood calcium levels; PTH and TCT together play a "
  "significant role in calcium balance.",
  ["Statement I: true", "Statement II: true"],
  "Parathyroid gland; Thyroid gland", ans="A",
  why="Both statements are NCERT lines, so every option that calls either one false is wrong.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("Glucagon increases the cellular uptake and utilisation of glucose.",
     "Insulin stimulates the conversion of glucose to glycogen (glycogenesis) in its target cells."),
  "Opposite actions of glucagon and insulin",
  "Glucagon acts mainly on hepatocytes, stimulates glycogenolysis and gluconeogenesis, and REDUCES cellular glucose "
  "uptake and utilisation, so it is hyperglycemic. Insulin stimulates conversion of glucose to glycogen "
  "(glycogenesis) in target cells, so it is hypoglycemic.",
  ["Statement I: false (glucagon reduces glucose uptake and utilisation)", "Statement II: true"],
  "Pancreas", ans="D",
  why="Statement I describes insulin's effect, not glucagon's, so the options that accept it are wrong; Statement II "
      "is correct, so 'both false' is wrong.", secs=40)

Z(CCI, "Mechanism of hormone action", A, MUL,
  MS("Which of the following statements about the mechanism of hormone action are correct?",
     ["Each hormone receptor is specific to one hormone only.",
      "Hormone receptors present in the cell membrane of target cells are called nuclear receptors.",
      "Binding of a hormone to its receptor leads to the formation of a hormone-receptor complex.",
      "Cyclic AMP, IP₃ and Ca²⁺ act as second messengers, which in turn regulate cellular metabolism.",
      "Estradiol and testosterone are protein hormones."]),
  "Hormone receptors and second messengers",
  "Hormones act through specific receptors present only in target tissues; each receptor is specific to one hormone. "
  "Receptors in the cell membrane are membrane-bound receptors; those inside the cell are intracellular receptors, "
  "mostly nuclear receptors. Hormone binding forms a hormone-receptor complex. Membrane-bound receptors generate "
  "second messengers (cAMP, IP₃, Ca²⁺). Estradiol and testosterone are steroids.",
  ["(a) True", "(b) False: membrane receptors are membrane-bound; nuclear receptors are intracellular", "(c) True",
   "(d) True", "(e) False: they are steroid hormones"],
  "Mechanism of hormone action",
  at="A", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"],
  why="Options with (b) mix up membrane-bound and nuclear receptors; options with (e) wrongly call steroid hormones "
      "proteins.", secs=70)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following statements about the hormones of the adrenal cortex are correct?",
     ["Cortisol is involved in maintaining the cardio-vascular system as well as the kidney functions.",
      "Cortisol stimulates RBC production.",
      "Aldosterone stimulates the excretion of Na⁺ and the reabsorption of K⁺ by the renal tubules.",
      "Small amounts of androgenic steroids secreted by the adrenal cortex play a role in the growth of axial hair, "
      "pubic hair and facial hair during puberty.",
      "Aldosterone helps in the maintenance of electrolytes, body fluid volume, osmotic pressure and blood "
      "pressure."]),
  "Glucocorticoids, mineralocorticoids and adrenal androgens",
  "Cortisol, the main glucocorticoid, helps maintain the cardio-vascular system and kidney functions and stimulates "
  "RBC production. Aldosterone, the main mineralocorticoid, acts on the renal tubules and stimulates reabsorption of "
  "Na⁺ and water and excretion of K⁺ and phosphate ions; it thus helps maintain electrolytes, body fluid volume, "
  "osmotic pressure and blood pressure. The cortex also secretes small amounts of androgenic steroids.",
  ["(a) True", "(b) True", "(c) False: aldosterone causes Na⁺ reabsorption and K⁺ excretion (the reverse)",
   "(d) True", "(e) True"],
  "Adrenal gland",
  at="D", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"],
  why="Any option with (c) reverses the action of aldosterone on Na⁺ and K⁺; (b), (d) and (e) only leaves out (a), "
      "which is a direct NCERT statement about cortisol.", secs=75)

Z(CCI, "Hormonal disorders", A, MAT,
  ML(("disorder", "cause"),
     ["Diabetes insipidus", "Gigantism", "Goitre (enlargement of the thyroid with hypothyroidism)",
      "Diabetes mellitus"],
     ["Prolonged hyperglycemia, with loss of glucose through urine and formation of ketone bodies",
      "Impaired synthesis or release of ADH, with excessive loss of water and dehydration",
      "Over-secretion of growth hormone",
      "Deficiency of iodine in the diet"]),
  "Endocrine disorders and their causes",
  "Impairment affecting the synthesis or release of ADH causes diabetes insipidus (excess water loss, dehydration). "
  "Over-secretion of GH causes abnormal growth of the body, called gigantism. Iodine deficiency causes "
  "hypothyroidism and enlargement of the thyroid (goitre). Prolonged hyperglycemia leads to diabetes mellitus, "
  "with loss of glucose through urine and formation of ketone bodies.",
  ["Diabetes insipidus → ADH problem (II)", "Gigantism → excess GH (III)", "Goitre → iodine deficiency (IV)",
   "Diabetes mellitus → prolonged hyperglycemia (I)"],
  "The pituitary gland; Thyroid gland; Pancreas",
  short="'Insipidus' = water problem (ADH); 'mellitus' = sugar problem.",
  at="B", match=({"A": "II", "B": "III", "C": "IV", "D": "I"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The trap codes swap the two kinds of diabetes (A-I, D-II) or link gigantism with iodine and goitre with "
      "growth hormone.", secs=55)

Z(CCI, "Adrenal, pancreas and gonads", A, ASR,
  AR("Estrogens regulate female sexual behaviour.",
     "Estrogens are synthesised and secreted mainly by the growing ovarian follicles."),
  "Sources and actions of estrogen",
  "Both statements are NCERT facts. Estrogens are produced by the growing ovarian follicles, and among their many "
  "actions they regulate female sexual behaviour. R only states WHERE estrogen is made; where a hormone is made does "
  "not explain why it influences behaviour (that depends on its action on its target tissues). So R does not explain "
  "A.",
  ["A: true", "R: true", "R names the source of estrogen; it says nothing about why estrogen affects behaviour"],
  "Gonads", ans="B",
  why="'R explains A' is wrong because the site of synthesis is a different property from the behavioural action; "
      "both statements are true, so C and D are wrong.", secs=45)

Z(CCI, "Thyroid, parathyroid and pineal", I, MAT,
  ML(("endocrine gland", "location"), ["Pineal gland", "Thymus", "Adrenal glands", "Pituitary gland"],
     ["In a bony cavity, the sella turcica, attached to the hypothalamus by a stalk",
      "On the dorsal side of the forebrain",
      "At the anterior part of each kidney",
      "Between the lungs, behind the sternum, on the ventral side of the aorta"]),
  "Locations of endocrine glands",
  "The pineal gland lies on the dorsal side of the forebrain. The thymus is a lobular structure between the lungs, "
  "behind the sternum, on the ventral side of the aorta. One pair of adrenal glands sits at the anterior part of each "
  "kidney. The pituitary lies in the sella turcica and is attached to the hypothalamus by a stalk.",
  ["Pineal → II", "Thymus → IV", "Adrenal → III", "Pituitary → I"],
  "Human endocrine system",
  at="D", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "I", "B": "IV", "C": "III", "D": "II"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The wrong codes swap the two brain-related glands (pineal and pituitary), swap thymus and adrenal, or put the "
      "thymus on the forebrain.", secs=45)

# ================================================================ Human Reproduction (7/9/7)
Z(HR, "Male and female reproductive systems", B, D,
  "Each testis of a human male has about how many compartments called testicular lobules?",
  "Internal structure of the testis",
  "Each testis has about 250 compartments called testicular lobules. Each lobule contains one to three highly coiled "
  "seminiferous tubules in which sperms are produced.",
  ["Testis → about 250 testicular lobules", "Each lobule → 1–3 seminiferous tubules"],
  "The male reproductive system",
  at="B", correct="About 250", wrong=["About 25", "About 2500", "Only 15–20"],
  why="25 and 2500 are off by a factor of ten; 15–20 is the number of mammary lobes in each breast.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "The enlarged end of the human penis, which is covered by a loose fold of skin called the foreskin, is the:",
  "External genitalia of the male",
  "The penis is the male external genitalia. Its enlarged end, called the glans penis, is covered by a loose fold of "
  "skin called the foreskin.",
  ["Enlarged end of the penis → glans penis", "Covered by the foreskin"],
  "The male reproductive system",
  at="B", correct="Glans penis", wrong=["Urethral meatus", "Clitoris", "Epididymis"],
  why="The urethral meatus is the external opening of the urethra; the clitoris is a female structure; the "
      "epididymis lies along the testis.", secs=25)

Z(HR, "Fertilisation and implantation", B, D,
  "In the human blastocyst, the group of cells attached to the trophoblast, which differentiates as the embryo, is "
  "called the:",
  "Structure of the blastocyst",
  "In the blastocyst, the blastomeres are arranged into an outer layer called the trophoblast and an inner group of "
  "cells attached to the trophoblast called the inner cell mass. The trophoblast attaches to the endometrium and the "
  "inner cell mass differentiates as the embryo.",
  ["Outer layer → trophoblast", "Inner group of cells → inner cell mass → embryo"],
  "Fertilisation and implantation",
  at="C", correct="Inner cell mass", wrong=["Chorionic villi", "Zona pellucida", "Morula"],
  why="Chorionic villi are projections on the trophoblast; the zona pellucida is the membrane around the oocyte; the "
      "morula is an earlier solid stage, not a group of cells inside the blastocyst.", secs=25)

Z(HR, "Gametogenesis", B, D,
  "The process by which spermatids are transformed into spermatozoa (sperms) is called:",
  "Spermiogenesis",
  "Secondary spermatocytes undergo the second meiotic division to form spermatids. The spermatids are transformed "
  "into spermatozoa by spermiogenesis. After spermiogenesis the sperm heads remain embedded in the Sertoli cells and "
  "are finally released from the seminiferous tubules by spermiation.",
  ["Spermatids → spermatozoa = spermiogenesis", "Release of sperms from seminiferous tubules = spermiation"],
  "Gametogenesis",
  at="D", correct="Spermiogenesis", wrong=["Spermiation", "Insemination", "Oogenesis"],
  why="Spermiation is the release of sperms from the tubules; insemination is the release of semen into the vagina; "
      "oogenesis is formation of the female gamete.", secs=25)

Z(HR, "Fertilisation and implantation", B, D,
  "During copulation (coitus), semen is released by the penis into the vagina. This process is called:",
  "Insemination",
  "The release of semen by the penis into the vagina during copulation is called insemination. Motile sperms then "
  "swim through the cervix and uterus to reach the junction of the isthmus and ampulla of the oviduct.",
  ["Semen released into the vagina → insemination"],
  "Fertilisation and implantation",
  at="B", correct="Insemination", wrong=["Ovulation", "Implantation", "Parturition"],
  why="Ovulation is the release of the ovum from the ovary; implantation is embedding of the blastocyst in the "
      "endometrium; parturition is delivery of the foetus.", secs=20)

Z(HR, "Male and female reproductive systems", B, MAT,
  ML(("female external genitalia", "description"), ["Mons pubis", "Labia majora", "Labia minora", "Hymen"],
     ["Paired folds of tissue under the labia majora",
      "Membrane that often partially covers the opening of the vagina",
      "Cushion of fatty tissue covered by skin and pubic hair",
      "Fleshy folds of tissue that extend down from the mons pubis and surround the vaginal opening"]),
  "Female external genitalia",
  "The mons pubis is a cushion of fatty tissue covered by skin and pubic hair. The labia majora are fleshy folds that "
  "extend down from the mons pubis and surround the vaginal opening. The labia minora are paired folds under the "
  "labia majora. The opening of the vagina is often covered partially by a membrane called the hymen.",
  ["Mons pubis → III", "Labia majora → IV", "Labia minora → I", "Hymen → II"],
  "The female reproductive system",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="The trap codes swap the labia majora and minora, or swap the mons pubis with the labia majora or the hymen.",
  secs=40)

Z(HR, "Menstrual cycle", B, D,
  "In human females, menstrual cycles cease at around 50 years of age. This is termed:",
  "Menopause",
  "Menstrual cycles cease around 50 years of age; this is termed menopause. Cyclic menstruation indicates the normal "
  "reproductive phase, which extends between menarche and menopause.",
  ["First menstruation → menarche", "End of menstrual cycles (about 50 years) → menopause"],
  "The menstrual cycle",
  at="C", correct="Menopause", wrong=["Menarche", "Ovulation", "Parturition"],
  why="Menarche is the first menstruation; ovulation is release of the ovum; parturition is child birth.", secs=20)

Z(HR, "Male and female reproductive systems", I, MUL,
  MS("Which of the following statements about the human female reproductive system are correct?",
     ["Each oviduct (fallopian tube) is about 10–12 cm long.",
      "The isthmus is the last part of the oviduct; it has a narrow lumen and joins the uterus.",
      "The ovarian stroma is divided into two zones: a peripheral cortex and an inner medulla.",
      "The uterus opens into the vagina through a wide cervix.",
      "Each ovary is about 10–12 cm in length."]),
  "Ovaries, oviducts and uterus",
  "Each ovary is about 2 to 4 cm long; its stroma is divided into a peripheral cortex and an inner medulla. Each "
  "oviduct is about 10–12 cm long and has an infundibulum, an ampulla and an isthmus; the isthmus has a narrow lumen "
  "and joins the uterus. The uterus opens into the vagina through a NARROW cervix.",
  ["(a) True", "(b) True", "(c) True", "(d) False: the cervix is narrow",
   "(e) False: an ovary is 2–4 cm long; 10–12 cm is the length of the oviduct"],
  "The female reproductive system",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="Options with (d) accept a 'wide' cervix; options with (e) give the ovary the length of the oviduct.", secs=60)

Z(HR, "Male and female reproductive systems", I, STP,
  SP("The hymen is often torn during the first coitus, but it can also be broken by a sudden fall or jolt, insertion "
     "of a vaginal tampon or active participation in sports such as horseback riding or cycling.",
     "The presence or absence of the hymen is a reliable indicator of virginity or sexual experience."),
  "The hymen",
  "NCERT states that the hymen is often torn during the first coitus, but it can also be broken by a sudden fall or "
  "jolt, insertion of a tampon or sports such as horseback riding and cycling, and in some women it persists even "
  "after coitus. Hence its presence or absence is NOT a reliable indicator of virginity or sexual experience.",
  ["Statement I: true", "Statement II: false"],
  "The female reproductive system", ans="C",
  why="Statement II is explicitly denied by NCERT, so the options calling it true are wrong; Statement I is an NCERT "
      "line, so 'both false' and 'I false' are wrong.", secs=35)

Z(HR, "Male and female reproductive systems", I, MAT,
  ML(("part of the mammary gland", "description"),
     ["Alveoli", "Mammary lobes", "Mammary ampulla", "Lactiferous duct"],
     ["Duct through which milk is sucked out",
      "The 15–20 subdivisions of the glandular tissue of each breast",
      "Clusters of cells that secrete milk, which is stored in their cavities (lumens)",
      "Wider structure formed by the joining of several mammary ducts"]),
  "Structure of the mammary gland",
  "The glandular tissue of each breast is divided into 15–20 mammary lobes containing clusters of cells called "
  "alveoli. Alveolar cells secrete milk, stored in their lumens. Alveoli open into mammary tubules; the tubules of "
  "each lobe join to form a mammary duct; several mammary ducts join to form a wider mammary ampulla, which is "
  "connected to the lactiferous duct through which milk is sucked out.",
  ["Alveoli → III", "Mammary lobes → II", "Mammary ampulla → IV", "Lactiferous duct → I"],
  "The female reproductive system",
  short="Order of milk flow: alveoli → tubules → mammary duct → ampulla → lactiferous duct.",
  at="D", match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The wrong codes confuse alveoli with lobes, the ampulla with the lactiferous duct, or alveoli with the "
      "ampulla.", secs=50)

Z(HR, "Gametogenesis", I, ASR,
  AR("Spermatogenesis in human males starts at the age of puberty.",
     "At puberty, the secretion of gonadotropin releasing hormone (GnRH) by the hypothalamus falls sharply."),
  "Hormonal control of spermatogenesis",
  "Spermatogenesis starts at puberty because of a significant INCREASE in the secretion of GnRH. GnRH acts on the "
  "anterior pituitary to increase LH and FSH; LH acts on the Leydig cells to secrete androgens, which stimulate "
  "spermatogenesis, and FSH acts on the Sertoli cells.",
  ["A: true", "R: false, because GnRH secretion rises (not falls) at puberty"],
  "Gametogenesis", ans="C",
  why="R reverses the NCERT statement, so neither 'both true' option holds; A is true, so D is wrong.", secs=40)

Z(HR, "Gametogenesis", I, STP,
  SP("The first meiotic division of the primary oocyte is unequal and results in a large haploid secondary oocyte "
     "and a tiny first polar body.",
     "The secondary oocyte retains the bulk of the nutrient-rich cytoplasm of the primary oocyte."),
  "First meiotic division in oogenesis",
  "Within the tertiary follicle the primary oocyte grows and completes its first meiotic division. The division is "
  "unequal: it forms a large haploid secondary oocyte and a tiny first polar body. The secondary oocyte keeps the "
  "bulk of the nutrient-rich cytoplasm of the primary oocyte.",
  ["Statement I: true", "Statement II: true"],
  "Gametogenesis", ans="A",
  why="Both statements are NCERT lines; the unequal division is exactly why the secondary oocyte keeps most of the "
      "cytoplasm.", secs=35)

Z(HR, "Menstrual cycle", I, STP,
  SP("The menstrual flow normally lasts for about 10–12 days.",
     "The menstrual cycle is repeated at an average interval of about 28/29 days."),
  "Duration of the menstrual cycle and menstrual flow",
  "The menstrual cycle is repeated at an average interval of about 28/29 days. The menstrual phase, when the "
  "menstrual flow occurs, lasts for 3–5 days.",
  ["Statement I: false (menstrual flow lasts 3–5 days)", "Statement II: true"],
  "The menstrual cycle", ans="D",
  why="10–12 days is wrong for the menstrual flow, so options accepting Statement I are wrong; Statement II is an "
      "NCERT figure, so 'both false' is wrong.", secs=30)

Z(HR, "Fertilisation and implantation", I, D,
  "In humans, the sex of the baby is decided by the father and not by the mother because:",
  "Sex determination in humans",
  "The chromosome pattern is XX in the human female and XY in the male. All haploid gametes (ova) produced by the "
  "female carry the X chromosome, whereas the male produces two types of sperms: about 50 per cent carry X and 50 per "
  "cent carry Y. The sperm that fertilises the ovum therefore decides the sex of the baby.",
  ["Female XX → all ova carry X", "Male XY → 50 % sperms X, 50 % sperms Y",
   "X sperm + ovum → XX (female); Y sperm + ovum → XY (male)"],
  "Fertilisation and implantation",
  at="C", correct="All ova carry an X chromosome, whereas about half the sperms carry X and half carry Y",
  wrong=["All sperms carry the Y chromosome, whereas ova carry either X or Y",
         "The father contributes more chromosomes to the zygote than the mother",
         "The ovum carries no sex chromosome at all"],
  why="Ova all carry X, sperms are of two types; each parent contributes 23 chromosomes; every ovum has an X "
      "chromosome.", secs=40)

Z(HR, "Pregnancy, parturition and lactation", A, MUL,
  MS("Which of the following statements about the human placenta are correct?",
     ["Chorionic villi and uterine tissue become interdigitated with each other and jointly form the placenta.",
      "The placenta is connected to the embryo through the umbilical cord.",
      "Chorionic villi are finger-like projections that appear on the inner cell mass after implantation.",
      "The placenta acts as an endocrine tissue and produces hCG, hPL, estrogens and progestogens.",
      "The placenta is expelled out of the uterus before the infant is delivered."]),
  "Placenta",
  "After implantation, finger-like projections called chorionic villi appear on the TROPHOBLAST. They interdigitate "
  "with the uterine tissue and jointly form the placenta, which is connected to the embryo through the umbilical cord "
  "and also acts as an endocrine tissue (hCG, hPL, estrogens, progestogens). Soon AFTER the infant is delivered, the "
  "placenta is also expelled out of the uterus.",
  ["(a) True", "(b) True", "(c) False: villi appear on the trophoblast", "(d) True",
   "(e) False: the placenta is expelled after the baby"],
  "Pregnancy and embryonic development; Parturition and lactation",
  at="D", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="Options with (c) put the villi on the inner cell mass; options with (e) reverse the order of expulsion of baby "
      "and placenta.", secs=60)

Z(HR, "Pregnancy, parturition and lactation", I, ASR,
  AR("The cells of the inner cell mass can give rise to all the tissues and organs of the body.",
     "The inner cell mass contains certain cells called stem cells, which have the potency to give rise to all the "
     "tissues and organs."),
  "Stem cells in the inner cell mass",
  "After implantation the inner cell mass differentiates into ectoderm, mesoderm and endoderm. NCERT states that the "
  "inner cell mass contains stem cells, which have the potency to give rise to all tissues and organs; this is why "
  "the inner cell mass can form the whole body.",
  ["A: true", "R: true", "R gives the reason: stem cells in the inner cell mass have the potency to form every tissue"],
  "Pregnancy and embryonic development", ans="A",
  why="R is the very property that makes A true, so 'R is not the explanation' is wrong; both statements are true, "
      "so C and D are wrong.", secs=40)

Z(HR, "Male and female reproductive systems", I, MUL,
  MS("Which of the following statements about the human testis are correct?",
     ["Each testis is about 10–12 cm in length.",
      "Each testicular lobule contains one to three highly coiled seminiferous tubules.",
      "The interstitial spaces outside the seminiferous tubules contain small blood vessels and interstitial "
      "(Leydig) cells.",
      "Each seminiferous tubule is lined on its inside by spermatogonia and Sertoli cells.",
      "Some immunologically competent cells are also present in the interstitial spaces."]),
  "Structure of the testis",
  "Each testis is oval, about 4 to 5 cm long and 2 to 3 cm wide. Its lobules each contain one to three highly coiled "
  "seminiferous tubules, lined by spermatogonia and Sertoli cells. The regions outside the tubules (interstitial "
  "spaces) contain small blood vessels, Leydig cells and other immunologically competent cells.",
  ["(a) False: a testis is 4–5 cm long", "(b) True", "(c) True", "(d) True", "(e) True"],
  "The male reproductive system",
  at="B", correct="(b), (c), (d) and (e) only",
  wrong=["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"],
  why="Options with (a) give the testis the length of the oviduct; (b), (c) and (d) only leaves out (e), which is an "
      "NCERT line.", secs=60)

Z(HR, "Gametogenesis", A, NUM,
  "In a human male, 10 primary spermatocytes complete spermatogenesis. A spermatogonium has 46 chromosomes. What is "
  "the total number of chromosomes present in all the spermatids formed?",
  "Meiosis in spermatogenesis",
  "Each primary spermatocyte (46 chromosomes) completes meiosis I to form two equal haploid secondary spermatocytes "
  "(23 chromosomes each). Each secondary spermatocyte completes meiosis II to form two haploid spermatids. So each "
  "primary spermatocyte gives four spermatids, each with 23 chromosomes.",
  ["Spermatids = 10 × 4 = 40", "Chromosomes per spermatid = 23 (haploid)", "Total = 40 × 23 = 920"],
  "Gametogenesis",
  at="B", correct="920", wrong=["1840", "460", "230"],
  short="Primary spermatocyte → 4 haploid cells: total = 10 × 4 × 23.",
  why="1840 treats spermatids as diploid (46); 460 stops at the secondary spermatocytes (20 × 23); 230 counts only "
      "one haploid cell per primary spermatocyte.", secs=60, vb=RECOMPUTED)

Z(HR, "Pregnancy, parturition and lactation", A, MAT,
  ML(("stage of human pregnancy", "development of the foetus"),
     ["After one month of pregnancy", "By the end of the second month", "During the fifth month",
      "By the end of 24 weeks (second trimester)"],
     ["Body is covered with fine hair, eye-lids separate and eyelashes are formed",
      "Heart is formed; its sound can be heard through a stethoscope",
      "First movements of the foetus and appearance of hair on the head are usually observed",
      "Foetus develops limbs and digits"]),
  "Embryonic development during pregnancy",
  "In humans, after one month of pregnancy the embryo's heart is formed (the first sign of a growing foetus can be "
  "noticed by listening to the heart sound through a stethoscope). By the end of the second month limbs and digits "
  "develop. First movements and hair on the head are usually seen in the fifth month. By the end of 24 weeks the "
  "body is covered with fine hair, the eye-lids separate and eyelashes are formed.",
  ["One month → II", "End of second month → IV", "Fifth month → III", "End of 24 weeks → I"],
  "Pregnancy and embryonic development",
  at="C", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="Each wrong code swaps two neighbouring milestones (heart and limbs, fifth month and 24 weeks, or limbs and "
      "first movements).", secs=60)

Z(HR, "Fertilisation and implantation", A, ASR,
  AR("The blastocyst becomes embedded in the endometrium of the uterus.",
     "After the trophoblast layer attaches to the endometrium, the uterine cells divide rapidly and cover the "
     "blastocyst."),
  "Implantation",
  "The trophoblast of the blastocyst attaches to the endometrium. After attachment, the uterine cells divide rapidly "
  "and cover the blastocyst; as a result, the blastocyst becomes embedded in the endometrium. This is implantation, "
  "and it leads to pregnancy.",
  ["A: true", "R: true", "R describes how the embedding happens, so it explains A"],
  "Fertilisation and implantation", ans="A",
  why="The covering of the blastocyst by dividing uterine cells is the mechanism of embedding, so B is wrong; both "
      "statements are NCERT facts, so C and D are wrong.", secs=45)

Z(HR, "Fertilisation and implantation", A, MUL,
  MS("Which of the following statements about events from fertilisation to implantation are correct?",
     ["After insemination, motile sperms reach the junction of the isthmus and the ampulla of the oviduct.",
      "Mitotic division (cleavage) starts as the zygote moves through the isthmus of the oviduct towards the uterus.",
      "The morula transforms into a blastocyst as it moves further into the uterus.",
      "Fusion of the haploid nuclei of the sperm and the ovum forms a haploid zygote.",
      "Implantation leads to pregnancy."]),
  "From zygote to implantation",
  "Sperms pass through the cervix and uterus to the ampullary-isthmic junction, where fertilisation takes place. The "
  "haploid nuclei of the sperm and ovum fuse to form a DIPLOID zygote. Cleavage starts as the zygote moves through "
  "the isthmus towards the uterus, forming 2, 4, 8, 16 blastomeres; the morula changes into a blastocyst as it moves "
  "further into the uterus. Implantation of the blastocyst leads to pregnancy.",
  ["(a) True", "(b) True", "(c) True", "(d) False: haploid + haploid = diploid zygote", "(e) True"],
  "Fertilisation and implantation",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (c) and (d) only", "(a), (c) and (e) only"],
  why="Options with (d) accept a haploid zygote; (a), (c) and (e) only leaves out (b), which NCERT states.", secs=70)

Z(HR, "Pregnancy, parturition and lactation", A, STP,
  SP("During pregnancy, the levels of estrogens, progestogens, cortisol, prolactin and thyroxine increase several-fold "
     "in the maternal blood.",
     "In the later phase of pregnancy, a hormone called relaxin is secreted by the ovary."),
  "Hormones during pregnancy",
  "NCERT states that during pregnancy the levels of other hormones such as estrogens, progestogens, cortisol, "
  "prolactin and thyroxine increase several-fold in the maternal blood, which supports fetal growth, metabolic "
  "changes in the mother and maintenance of pregnancy. In the later phase of pregnancy the ovary also secretes "
  "relaxin.",
  ["Statement I: true", "Statement II: true"],
  "Pregnancy and embryonic development", ans="A",
  why="Students who think only the placenta makes pregnancy hormones may call Statement II false, but NCERT names the "
      "ovary as the source of relaxin; Statement I is an NCERT line.", secs=40)

Z(HR, "Gametogenesis", A, MAT,
  ML(("cell in the testis", "feature"),
     ["Spermatogonia", "Primary spermatocytes", "Secondary spermatocytes", "Sertoli cells"],
     ["Undergo the second meiotic division to produce spermatids",
      "Diploid male germ cells that multiply by mitotic division",
      "Complete the first meiotic division to form two equal haploid cells",
      "Acted upon by FSH to secrete some factors that help in spermiogenesis"]),
  "Cells of the seminiferous tubule in spermatogenesis",
  "Spermatogonia (46 chromosomes) multiply by mitosis. Some become primary spermatocytes, which complete the first "
  "meiotic division (reduction division) to form two equal haploid secondary spermatocytes (23 chromosomes each). "
  "These undergo the second meiotic division to produce four haploid spermatids. FSH acts on the Sertoli cells and "
  "stimulates secretion of some factors that help in spermiogenesis.",
  ["Spermatogonia → II", "Primary spermatocytes → III", "Secondary spermatocytes → I", "Sertoli cells → IV"],
  "Gametogenesis",
  at="A", match=({"A": "II", "B": "III", "C": "I", "D": "IV"},
                 [{"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The commonest slip swaps the two meiotic divisions (B-I, C-III); others treat spermatogonia as the cells of "
      "meiosis I, or give the Sertoli cells' role to spermatogonia.", secs=55)

# ================================================================ Reproductive Health (4/6/4)
Z(RH, "Contraception", B, D,
  "Which of the following is a copper-releasing intra-uterine device (IUD)?",
  "Types of IUDs",
  "IUDs are of three kinds: non-medicated IUDs (e.g., Lippes loop), copper-releasing IUDs (CuT, Cu7, Multiload 375) "
  "and hormone-releasing IUDs (Progestasert, LNG-20).",
  ["Non-medicated → Lippes loop", "Copper-releasing → CuT, Cu7, Multiload 375",
   "Hormone-releasing → Progestasert, LNG-20"],
  "Birth control (intra-uterine devices)",
  at="A", correct="Multiload 375", wrong=["Lippes loop", "LNG-20", "Progestasert"],
  why="Lippes loop is non-medicated; LNG-20 and Progestasert release hormones, not copper.", secs=25)

Z(RH, "Contraception", B, D,
  "Besides oral pills, progestogens alone or in combination with estrogen can be used by females as:",
  "Injectable and implant contraceptives",
  "Progestogens alone or in combination with estrogen can be used as injections or implants under the skin. Their "
  "mode of action is similar to that of pills, but their effective periods are much longer.",
  ["Hormonal methods: pills, injections, implants", "Injections/implants act like pills but last much longer"],
  "Birth control (oral, injectable and implant methods)",
  at="B", correct="Injections or implants under the skin",
  wrong=["Barrier devices that cover the cervix", "Copper-releasing IUDs", "A surgical method that blocks the oviduct"],
  why="Cervical caps and diaphragms are barriers without hormones; copper IUDs release copper ions, not hormones; "
      "tubectomy is surgical.", secs=25)

Z(RH, "Infertility and ART", B, D,
  "In vitro fertilisation followed by embryo transfer (IVF-ET) is popularly known as the:",
  "In vitro fertilisation",
  "In IVF, fertilisation takes place outside the body in almost similar conditions as in the body, followed by "
  "embryo transfer (ET). This is popularly known as the 'test tube baby' programme.",
  ["Fertilisation outside the body (in vitro) + embryo transfer", "Popular name: test tube baby programme"],
  "Infertility",
  at="C", correct="Test tube baby programme", wrong=["Saheli programme", "Family planning programme",
                                                   "Lactational amenorrhea method"],
  why="Saheli is an oral contraceptive pill; family planning programmes deal with birth control; lactational "
      "amenorrhea is a natural contraceptive method.", secs=20)

Z(RH, "STDs and their prevention", B, D,
  "Which of the following are the early symptoms of most sexually transmitted infections (STIs)?",
  "Early symptoms of STIs",
  "The early symptoms of most STIs are minor: itching, fluid discharge, slight pain and swellings in the genital "
  "region. Because they are minor (and infected females are often asymptomatic), STIs may remain undetected for long.",
  ["Early symptoms → itching, fluid discharge, slight pain, swellings in the genital region"],
  "Sexually transmitted infections (STIs)",
  at="D", correct="Itching, fluid discharge, slight pain and swellings in the genital region",
  wrong=["Chills and high fever recurring every three to four days",
         "Paralysis of the limbs", "Formation of tumours in the lungs"],
  why="Recurring chills and fever every three to four days describe malaria; paralysis and lung tumours are not "
      "early STI symptoms.", secs=25)

Z(RH, "Contraception", I, MUL,
  MS("Which of the following statements about contraceptive methods are correct?",
     ["Diaphragms, cervical caps and vaults are made of rubber and are inserted into the female reproductive tract to "
      "cover the cervix during coitus.",
      "IUDs are inserted by doctors or expert nurses in the uterus through the vagina.",
      "IUDs are one of the most widely accepted methods of contraception in India.",
      "'Nirodh' is a popular brand of female condom.",
      "The lactational amenorrhea method is effective only up to a maximum period of six months following "
      "parturition."]),
  "Barrier methods, IUDs and natural methods",
  "Diaphragms, cervical caps and vaults are rubber barriers that cover the cervix during coitus. IUDs are inserted by "
  "doctors or expert nurses in the uterus through the vagina and are among the most widely accepted contraceptive "
  "methods in India. 'Nirodh' is a popular brand of condom for the MALE. Lactational amenorrhea is effective only up "
  "to a maximum of six months after parturition.",
  ["(a) True", "(b) True", "(c) True", "(d) False: Nirodh is a male condom", "(e) True"],
  "Birth control",
  at="A", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="Every option with (d) wrongly calls Nirodh a female condom.", secs=60)

Z(RH, "Contraception", I, ASR,
  AR("Surgical methods of contraception (sterilisation) are generally advised as a terminal method to prevent any "
     "more pregnancies.",
     "The reversibility of sterilisation is very poor."),
  "Surgical methods (sterilisation)",
  "Vasectomy and tubectomy are highly effective, but their reversibility is very poor. Because fertility usually "
  "cannot be restored, they are advised only as a terminal method, when the couple wants no more pregnancies.",
  ["A: true", "R: true", "Poor reversibility is exactly why sterilisation is kept as a terminal method"],
  "Birth control (surgical methods)", ans="A",
  why="R is the reason sterilisation is 'terminal', so B is wrong; both statements are NCERT facts, so C and D are "
      "wrong.", secs=40)

Z(RH, "MTP and amniocentesis", I, STP,
  SP("Misuse of amniocentesis to determine the sex of the unborn child, followed by MTP if the foetus is female, is "
     "a dangerous trend and is against the law.",
     "Most MTPs are performed by qualified doctors in hospitals, so they carry no risk."),
  "Problems related to MTP",
  "NCERT calls the misuse of amniocentesis to find the sex of the foetus (often followed by MTP of a female foetus) "
  "a dangerous trend that is totally against what is legal. It also states that a majority of MTPs are performed "
  "illegally by unqualified quacks, which are not only unsafe but could be fatal too.",
  ["Statement I: true", "Statement II: false (most MTPs are illegal ones by unqualified quacks and are unsafe)"],
  "Medical termination of pregnancy (MTP)", ans="C",
  why="Statement II contradicts NCERT, so the options accepting it are wrong; Statement I is an NCERT point, so B and "
      "D are wrong.", secs=40)

Z(RH, "Infertility and ART", I, STP,
  SP("ART facilities are inexpensive and are available in a large number of centres throughout India.",
     "Although the female is often blamed for a couple being childless in India, the problem is very often present in "
     "the male partner."),
  "Infertility and access to ART",
  "NCERT notes that in India the female is often blamed for infertility, but more often than not the problem lies in "
  "the male partner. ART procedures require extremely high precision handling by specialised professionals and "
  "expensive instrumentation, so these facilities are presently available only in very few centres in the country.",
  ["Statement I: false (ART is expensive and available only in very few centres)", "Statement II: true"],
  "Infertility", ans="D",
  why="Statement I is the opposite of NCERT, so A and C are wrong; Statement II is an NCERT line, so B is wrong.",
  secs=40)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive method", "how it prevents conception"),
     ["Condom", "Copper-releasing IUD", "Coitus interruptus (withdrawal)", "Tubectomy"],
     ["Copper ions released suppress sperm motility and the fertilising capacity of sperms",
      "The male partner withdraws his penis from the vagina just before ejaculation to avoid insemination",
      "A thin rubber/latex sheath prevents the ejaculated semen from entering the female reproductive tract",
      "A small part of the fallopian tube is removed or tied up, blocking gamete transport"]),
  "Modes of action of contraceptives",
  "Condoms are barriers made of thin rubber/latex that prevent deposition of ejaculated semen into the female tract. "
  "Copper IUDs release Cu ions that suppress sperm motility and fertilising capacity. In coitus interruptus the male "
  "withdraws just before ejaculation. Tubectomy removes or ties up a small part of the fallopian tube, which blocks "
  "gamete transport.",
  ["Condom → III", "Cu-IUD → I", "Withdrawal → II", "Tubectomy → IV"],
  "Birth control",
  at="B", match=({"A": "III", "B": "I", "C": "II", "D": "IV"},
                 [{"A": "I", "B": "III", "C": "II", "D": "IV"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"}]),
  why="The wrong codes give the condom the action of copper ions, swap withdrawal with tubectomy, or swap condom with "
      "withdrawal.", secs=50)

Z(RH, "MTP and amniocentesis", I, D,
  "According to NCERT, MTP is considered essential in certain cases. Which of the following is one of them?",
  "Need for MTP",
  "MTPs are performed to get rid of unwanted pregnancies (due to casual unprotected intercourse, failure of the "
  "contraceptive used during coitus, or rape). MTPs are also essential in certain cases where continuation of the "
  "pregnancy could be harmful or even fatal either to the mother or to the foetus or both.",
  ["Unwanted pregnancy (unprotected intercourse, contraceptive failure, rape)",
   "Continuation harmful or fatal to mother, foetus or both → MTP essential"],
  "Medical termination of pregnancy (MTP)",
  at="C", correct="When continuation of the pregnancy could be harmful or even fatal to the mother or the foetus or both",
  wrong=["When amniocentesis shows that the foetus is female",
         "As a routine method of contraception in place of birth-control measures",
         "Whenever the parents wish to choose the sex of their child"],
  why="Terminating a female foetus or choosing the sex of a child is illegal; MTP is not a substitute for "
      "contraception.", secs=35)

Z(RH, "STDs and their prevention", A, MUL,
  MS("Which of the following statements about sexually transmitted infections are correct?",
     ["In infected females, STIs are often asymptomatic and may remain undetected for long.",
      "Gonorrhoea and syphilis are sexually transmitted infections.",
      "If not treated, STIs can lead to complications such as abortions, still births and even cancer of the "
      "reproductive tract.",
      "Avoiding sex with unknown partners or multiple partners is one of the simple principles for preventing STIs.",
      "Hepatitis-B and HIV cannot pass from an infected mother to the foetus."]),
  "STIs: symptoms, complications and prevention",
  "Infected females are often asymptomatic, so STIs may remain undetected for long. Gonorrhoea, syphilis, genital "
  "herpes, chlamydiasis, genital warts, trichomoniasis, hepatitis-B and HIV are STIs. Untreated STIs can cause PID, "
  "abortions, still births, ectopic pregnancies, infertility and even cancer of the reproductive tract. Hepatitis-B "
  "and HIV can also be transmitted by sharing needles or surgical instruments, by transfusion of blood, and from an "
  "infected mother to the foetus.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: both can pass from mother to foetus"],
  "Sexually transmitted infections (STIs)",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="Every option with (e) denies mother-to-foetus transmission, which NCERT lists; the others are true.", secs=65)

Z(RH, "Contraception", A, ASR,
  AR("Spermicidal creams, jellies and foams are generally used alone as the main method of contraception.",
     "Spermicidal creams, jellies and foams are usually used along with barriers to increase their contraceptive "
     "efficiency."),
  "Use of spermicides",
  "NCERT states that spermicidal creams, jellies and foams are usually used ALONG WITH barrier methods "
  "(diaphragms, cervical caps, vaults) to increase their contraceptive efficiency. They are not described as a "
  "stand-alone main method.",
  ["A: false", "R: true"],
  "Birth control (barrier methods)", ans="D",
  why="A is false, so options A, B and C (which all need A to be true) are wrong.", secs=40)

Z(RH, "Contraception", A, D,
  "A woman wants to delay her first pregnancy and space her children later. According to NCERT, which of the "
  "following is ideal for her?",
  "Choosing a contraceptive",
  "NCERT says IUDs are ideal contraceptives for females who want to delay pregnancy and/or space children. "
  "Sterilisation (tubectomy, or vasectomy of the husband) is a terminal method with very poor reversibility, and MTP "
  "is not a contraceptive.",
  ["Need: delay + spacing (reversible)", "IUD → reversible, ideal for delaying/spacing",
   "Tubectomy/vasectomy → terminal, poor reversibility"],
  "Birth control",
  at="C", correct="An intra-uterine device (IUD)",
  wrong=["Tubectomy", "Vasectomy of her husband", "Repeated medical termination of pregnancy"],
  why="Tubectomy and vasectomy are terminal methods; MTP is not meant to be used as contraception.", secs=40)

Z(RH, "Infertility and ART", A, MUL,
  MS("Which of the following statements about infertility and assisted reproductive technologies are correct?",
     ["In IVF, ova from the wife or a donor and sperms from the husband or a donor are induced to form a zygote under "
      "simulated conditions in the laboratory.",
      "In intra cytoplasmic sperm injection (ICSI), a sperm is directly injected into the ovum.",
      "The reasons for infertility could be physical, congenital, diseases, drugs, immunological or even "
      "psychological.",
      "Embryos formed by in-vivo fertilisation (fusion of gametes within the female) can never be used for embryo "
      "transfer."]),
  "Assisted reproductive technologies",
  "In IVF, ova and sperms are induced to form a zygote under simulated conditions in the laboratory. In ICSI, a sperm "
  "is directly injected into the ovum to form an embryo in the laboratory. Infertility may have physical, congenital, "
  "disease-related, drug-related, immunological or psychological causes. NCERT also states that embryos formed by "
  "in-vivo fertilisation can be used for such transfer to assist females who cannot conceive.",
  ["(a) True", "(b) True", "(c) True", "(d) False: in-vivo embryos can also be transferred"],
  "Infertility",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d)", "(b) and (d) only", "(a) and (c) only"],
  why="Options with (d) contradict NCERT; (a) and (c) only leaves out the correct description of ICSI.", secs=55)

# ================================================================ Evolution (5/7/5)
Z(EVO, "Evidences of evolution", B, D,
  "The thorn of Bougainvillea and the tendril of Cucurbita are examples of:",
  "Homology in plants",
  "The thorns of Bougainvillea and the tendrils of Cucurbita perform different functions but have the same "
  "underlying origin, so NCERT gives them as an example of homology in plants. Homology is the result of divergent "
  "evolution.",
  ["Same origin, different function → homologous", "Homology ← divergent evolution"],
  "Evidences for evolution (comparative anatomy and morphology)",
  at="A", correct="Homologous structures, resulting from divergent evolution",
  wrong=["Analogous structures, resulting from convergent evolution",
         "Vestigial structures with no function", "Fossils preserved in sedimentary rocks"],
  why="Analogous structures have similar function but different origin (e.g. sweet potato and potato); both "
      "thorns and tendrils are functional; they are living structures, not fossils.", secs=25)

Z(EVO, "Darwinism and modern synthesis", B, D,
  "Alfred Wallace, a naturalist who came to conclusions similar to Darwin's around the same time, worked in the:",
  "Darwin and Wallace",
  "NCERT notes that Alfred Wallace, a naturalist who worked in the Malay Archipelago, had come to similar "
  "conclusions (about evolution by natural selection) around the same time as Darwin.",
  ["Wallace → naturalist in the Malay Archipelago", "Reached conclusions similar to Darwin's"],
  "Evolution by natural selection (Darwin's theory)",
  at="B", correct="Malay Archipelago", wrong=["Galapagos Islands", "Australian continent", "East African grasslands"],
  why="Darwin, not Wallace, studied the Galapagos finches; Australia is where marsupials radiated; the East African "
      "grasslands are linked with Australopithecines.", secs=25)

Z(EVO, "Human evolution", B, D,
  "About 15 million years ago, two primates, Dryopithecus and Ramapithecus, existed. Which of the following is "
  "correct about them?",
  "Early primates",
  "About 15 mya, Dryopithecus and Ramapithecus existed. They were hairy and walked like gorillas and chimpanzees. "
  "Ramapithecus was more man-like, while Dryopithecus was more ape-like.",
  ["Both: hairy, walked like gorillas and chimpanzees", "Ramapithecus → more man-like",
   "Dryopithecus → more ape-like"],
  "Origin and evolution of man",
  at="C", correct="Ramapithecus was more man-like, while Dryopithecus was more ape-like",
  wrong=["Dryopithecus was more man-like, while Ramapithecus was more ape-like",
         "Both had a brain capacity of about 1400 cc and buried their dead",
         "Both walked fully erect and used fire"],
  why="The first option reverses NCERT; a 1400 cc brain and burial of the dead describe Neanderthal man; these "
      "hairy primates walked like gorillas and chimpanzees.", secs=30)

Z(EVO, "Darwinism and modern synthesis", B, D,
  "The idea that the evolution of life forms is driven by the use and disuse of organs, as in the long neck of the "
  "giraffe, was proposed by:",
  "Lamarck's idea of use and disuse",
  "Lamarck said that evolution of life forms occurred but was driven by the use and disuse of organs; his example was "
  "the giraffe, whose ancestors were thought to have elongated their necks by stretching to reach high leaves. NCERT "
  "notes that no one believes this conjecture any more.",
  ["Use and disuse of organs → Lamarck"],
  "Evolution by natural selection",
  at="D", correct="Lamarck", wrong=["Hugo de Vries", "Alfred Wallace", "Charles Darwin"],
  why="de Vries proposed mutation (saltation); Wallace and Darwin proposed evolution by natural selection, not use "
      "and disuse.", secs=20)

Z(EVO, "Origin of life", B, NUM,
  "According to NCERT, the earth was formed about 4.5 billion years ago, and life appeared about 500 million years "
  "after the formation of the earth. Life on earth therefore appeared about:",
  "Time scale of the origin of life",
  "Life appeared 500 million (0.5 billion) years after the earth formed, so it appeared 4.5 − 0.5 = 4.0 billion years "
  "ago, i.e. almost four billion years back.",
  ["500 million years = 0.5 billion years", "4.5 − 0.5 = 4.0 billion years ago"],
  "Origin of life",
  at="A", correct="4 billion years ago",
  wrong=["5 billion years ago", "4.45 billion years ago", "2 billion years ago"],
  why="5 billion adds instead of subtracting; 4.45 billion treats 500 million as 50 million; 2 billion (2000 mya) is "
      "when the first cellular forms appeared.", secs=30, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, NUM,
  "In a population of 10,000 individuals in Hardy-Weinberg equilibrium, a trait is controlled by one gene with two "
  "alleles, A (dominant) and a (recessive). If 9,100 individuals show the dominant phenotype, how many individuals "
  "are expected to be homozygous dominant (AA)?",
  "Hardy-Weinberg principle: from phenotype to genotype",
  "Only aa individuals show the recessive phenotype, so q² = (10,000 − 9,100)/10,000 = 0.09 and q = 0.3. Then "
  "p = 1 − q = 0.7 and the frequency of AA = p² = 0.49. Number of AA = 0.49 × 10,000 = 4,900.",
  ["Recessive phenotype = 900 → q² = 0.09", "q = 0.3, p = 0.7", "AA = p² × N = 0.49 × 10,000 = 4,900"],
  "Hardy-Weinberg principle",
  at="B", correct="4,900", wrong=["4,200", "8,281", "7,000"],
  short="Always start from the recessive class: q² is the only frequency read directly from phenotypes.",
  why="4,200 is the number of heterozygotes (2pq × N); 8,281 squares the dominant-phenotype frequency (0.91²); "
      "7,000 uses p instead of p².", secs=75, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population in Hardy-Weinberg equilibrium for a gene with two alleles A and a, the frequency of heterozygotes "
  "(Aa) is 0.48, and allele A is more common than allele a. What is the expected frequency of the homozygous "
  "recessive genotype (aa)?",
  "Hardy-Weinberg principle: solving for allele frequencies",
  "2pq = 0.48 with p + q = 1 gives pq = 0.24, so p and q are 0.6 and 0.4. Since A is more common, p = 0.6 and "
  "q = 0.4. Frequency of aa = q² = 0.16.",
  ["2pq = 0.48 → pq = 0.24", "p + q = 1 → p = 0.6, q = 0.4 (A more common)", "aa = q² = 0.16"],
  "Hardy-Weinberg principle",
  at="C", correct="0.16", wrong=["0.36", "0.24", "0.52"],
  why="0.36 is p² (the larger root squared); 0.24 is pq (2pq halved); 0.52 is p² + q², the total of both homozygotes.",
  secs=90, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", I, STP,
  SP("The eye of the octopus and the eye of mammals are analogous structures.",
     "Sweet potato (a root modification) and potato (a stem modification) are homologous structures."),
  "Analogy",
  "The eye of the octopus and of mammals, and the flippers of penguins and dolphins, are analogous: they perform "
  "similar functions but are not anatomically similar. Sweet potato (root modification) and potato (stem "
  "modification) also perform the same function (storage) but differ in origin, so they are ANALOGOUS, not "
  "homologous.",
  ["Statement I: true", "Statement II: false (they are analogous)"],
  "Evidences for evolution (comparative anatomy and morphology)", ans="C",
  why="Different origin with similar function is analogy, so Statement II is false and options A and D are wrong; "
      "Statement I is an NCERT example, so B is wrong.", secs=35)

Z(EVO, "Evidences of evolution", I, ASR,
  AR("Homologous structures indicate common ancestry.",
     "Homologous structures result from divergent evolution, in which the same structure develops along different "
     "directions due to adaptations to different needs."),
  "Homology and divergent evolution",
  "Structures such as the forelimbs of whales, bats, cheetahs and humans share the same basic plan because they were "
  "inherited from a common ancestor and then modified for different needs (divergent evolution). Because homologous "
  "structures arise by divergence from a common ancestral structure, they indicate common ancestry.",
  ["A: true", "R: true", "Divergence from one ancestral structure is why homology shows common ancestry"],
  "Evidences for evolution (comparative anatomy and morphology)", ans="A",
  why="R gives the origin of homology, which is the reason it points to common ancestry, so B is wrong; both "
      "statements are true, so C and D are wrong.", secs=40)

Z(EVO, "Origin of life", I, MAT,
  ML(("event", "approximate time (NCERT)"),
     ["Invertebrates were formed and active", "First cellular forms of life appeared on earth",
      "Dinosaurs suddenly disappeared from the earth", "Pre-historic cave art developed"],
     ["About 2000 million years ago", "By about 500 million years ago", "About 65 million years ago",
      "About 18,000 years ago"]),
  "A brief account of evolution",
  "NCERT: the first cellular forms of life appeared about 2000 mya; invertebrates were formed and active by 500 mya; "
  "dinosaurs suddenly disappeared about 65 mya; pre-historic cave art developed about 18,000 years ago.",
  ["Invertebrates → II", "First cells → I", "Dinosaurs disappeared → III", "Cave art → IV"],
  "A brief account of evolution; Origin and evolution of man",
  at="D", match=({"A": "II", "B": "I", "C": "III", "D": "IV"},
                 [{"A": "I", "B": "II", "C": "III", "D": "IV"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"}]),
  why="The trap codes swap the two oldest events (cells must come before invertebrates), swap dinosaurs with cave "
      "art, or place invertebrates after the dinosaurs vanished.", secs=50)

Z(EVO, "Natural selection", I, MUL,
  MS("Which of the following statements about natural selection are correct?",
     ["In stabilising selection, more individuals acquire the mean character value.",
      "In directional selection, more individuals acquire the mean character value.",
      "Excess use of herbicides and pesticides has resulted in the selection of resistant varieties in a much lesser "
      "time scale.",
      "Microbes becoming resistant to the antibiotics or drugs used against them is an example of evolution by "
      "anthropogenic action.",
      "According to Darwin, evolution takes place by single-step large mutations (saltation)."]),
  "Types of natural selection and evolution by anthropogenic action",
  "Natural selection can be stabilising (more individuals acquire the mean character value), directional (more "
  "individuals acquire a value OTHER than the mean) or disruptive. Excess use of herbicides and pesticides has "
  "selected resistant varieties quickly, and microbes have become resistant to antibiotics and drugs: evolution by "
  "anthropogenic action. Saltation (single-step large mutation) is de Vries's idea, not Darwin's.",
  ["(a) True", "(b) False: directional selection shifts the value away from the mean", "(c) True", "(d) True",
   "(e) False: saltation is de Vries's idea"],
  "Evidences for evolution; Mechanism of evolution",
  at="B", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"],
  why="Options with (b) give directional selection the definition of stabilising selection; options with (e) give "
      "de Vries's saltation to Darwin.", secs=60)

Z(EVO, "Origin of life", I, MUL,
  MS("Which of the following statements about the early earth and the origin of life are correct?",
     ["UV rays from the sun broke up water into hydrogen and oxygen, and the lighter hydrogen escaped.",
      "Oxygen combined with ammonia and methane to form water, carbon dioxide and other compounds.",
      "The early earth had a thick, oxygen-rich atmosphere from the very beginning.",
      "In experiments similar to Miller's, others observed the formation of sugars, nitrogen bases, pigments and "
      "fats.",
      "In Miller's experiment, the temperature inside the closed flask was kept at 0 °C."]),
  "Conditions on the early earth",
  "The early earth had no atmosphere. Water vapour, methane, carbon dioxide and ammonia released from the molten mass "
  "covered the surface. UV rays broke up water into H₂ and O₂; the lighter H₂ escaped. Oxygen combined with ammonia "
  "and methane to form water, CO₂ and others, and the ozone layer formed. Miller's flask was kept at 800 °C; others "
  "later observed sugars, nitrogen bases, pigments and fats in similar experiments.",
  ["(a) True", "(b) True", "(c) False: early earth had no atmosphere", "(d) True", "(e) False: Miller used 800 °C"],
  "Origin of life",
  at="A", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="Options with (c) give the early earth an oxygen-rich atmosphere; options with (e) get Miller's temperature "
      "wrong.", secs=60)

Z(EVO, "Evidences of evolution", I, ASR,
  AR("The first organisms that invaded land were animals.",
     "Fish with stout and strong fins could move on land and go back to water; this was about 350 million years "
     "ago."),
  "Colonisation of land",
  "NCERT states that the first organisms that invaded land were PLANTS; they were widespread on land when animals "
  "invaded it. It also states that fish with stout and strong fins could move on land and go back to water, about "
  "350 mya.",
  ["A: false (plants invaded land first)", "R: true"],
  "A brief account of evolution", ans="D",
  why="A is false, so options A, B and C, which all need A to be true, are wrong.", secs=40)

Z(EVO, "Adaptive radiation", A, ASR,
  AR("The marsupials of Australia are an example of adaptive radiation.",
     "A number of marsupials, each different from the other, evolved from an ancestral stock, all within the "
     "Australian island continent."),
  "Adaptive radiation in Australian marsupials",
  "Adaptive radiation is the evolution of different species in a given geographical area starting from one point "
  "and radiating to other areas of geography (habitats). In Australia, many different marsupials evolved from a "
  "common ancestral stock within the island continent; this is exactly what makes them an example of adaptive "
  "radiation.",
  ["A: true", "R: true", "R describes the radiation from a single ancestral stock, which is the definition applied"],
  "Adaptive radiation", ans="A",
  why="R is the very evidence that makes the marsupials an example of adaptive radiation, so B is wrong; both "
      "statements are NCERT facts, so C and D are wrong.", secs=45)

Z(EVO, "Evidences of evolution", A, STP,
  SP("In 1938, a fish caught in South Africa happened to be a coelacanth, which was thought to be extinct.",
     "Giant ferns (pteridophytes) were present in the past, but they slowly fell to form coal deposits."),
  "A brief account of evolution",
  "NCERT records that in 1938 a fish caught in South Africa happened to be a coelacanth, thought to be extinct; such "
  "lobefins evolved into the first amphibians. It also notes that giant ferns (pteridophytes) were present but they "
  "all fell to form coal deposits slowly.",
  ["Statement I: true", "Statement II: true"],
  "A brief account of evolution", ans="A",
  why="Both are NCERT statements; neither 'false' option holds.", secs=35)

Z(EVO, "Evidences of evolution", A, MAT,
  ML(("group", "feature in the history of life"),
     ["Lobefins", "Ichthyosaurs", "First mammals", "Reptiles"],
     ["Shrew-like animals, whose fossils are small-sized",
      "Evolved into the first amphibians",
      "Lay thick-shelled eggs that do not dry up in the sun",
      "Fish-like reptiles that went back into water about 200 million years ago"]),
  "Vertebrate history",
  "Lobefins (like the coelacanth) evolved into the first amphibians. Reptiles lay thick-shelled eggs which, unlike "
  "amphibian eggs, do not dry up in the sun. Some land reptiles went back into water about 200 mya and evolved into "
  "fish-like reptiles (Ichthyosaurs). The first mammals were like shrews, and their fossils are small-sized.",
  ["Lobefins → II", "Ichthyosaurs → IV", "First mammals → I", "Reptiles → III"],
  "A brief account of evolution",
  at="C", match=({"A": "II", "B": "IV", "C": "I", "D": "III"},
                 [{"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="The trap codes treat Ichthyosaurs (reptiles) as the ancestors of amphibians, give the mammals reptilian eggs, "
      "or make Ichthyosaurs shrew-like.", secs=55)

Z(EVO, "Human evolution", A, MUL,
  MS("Which of the following statements about human evolution are correct?",
     ["Dryopithecus and Ramapithecus were hairy and walked like gorillas and chimpanzees.",
      "A few fossils of man-like bones have been discovered in Ethiopia and Tanzania.",
      "Homo sapiens arose in Asia and later moved to Africa.",
      "The fossils of man-like bones found in eastern Africa revealed hominid features, and the man-like primates "
      "they belonged to walked upright.",
      "Agriculture came around 10,000 years back, and human settlements started."]),
  "Origin and evolution of man",
  "Dryopithecus and Ramapithecus were hairy and walked like gorillas and chimpanzees. A few fossils of man-like "
  "bones have been found in Ethiopia and Tanzania; they revealed hominid features, and these man-like primates of "
  "eastern Africa walked upright. Homo sapiens arose in AFRICA and moved across continents, developing into distinct "
  "races. Agriculture came around 10,000 years back and human settlements started.",
  ["(a) True", "(b) True", "(c) False: Homo sapiens arose in Africa", "(d) True", "(e) True"],
  "Origin and evolution of man",
  at="D", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"],
  why="Options with (c) reverse the African origin of Homo sapiens; (a), (d) and (e) only leaves out the true "
      "statement (b).", secs=65)

# ================================================================ Human Health and Disease (7/9/7)
Z(HHD, "Pathogens and diseases", B, D,
  "The 'good humor' hypothesis of health was disproved partly by the discovery of blood circulation using the "
  "experimental method. This discovery was made by:",
  "History of ideas about health",
  "Hippocrates and the Indian Ayurveda system held that health is a state of balance of certain 'humors'. The "
  "discovery of blood circulation by William Harvey using the experimental method, and the demonstration of normal "
  "body temperature in persons with 'good humor' using a thermometer, disproved the 'good humor' hypothesis.",
  ["'Good humor' hypothesis → Hippocrates, Ayurveda", "Disproved by William Harvey's experimental method"],
  "Human health and disease (introduction)",
  at="B", correct="William Harvey", wrong=["Hippocrates", "Louis Pasteur", "Alfred Wallace"],
  why="Hippocrates held the humor idea itself; Pasteur disproved spontaneous generation; Wallace was a naturalist "
      "who studied evolution.", secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "Which of the following is an auto-immune disease?",
  "Auto-immunity",
  "Sometimes, due to genetic and other unknown reasons, the body attacks self-cells. This results in damage to the "
  "body and is called auto-immune disease. Rheumatoid arthritis, which affects many people, is an example.",
  ["Body attacks self-cells → auto-immune disease", "Example: rheumatoid arthritis"],
  "Immunity (auto-immunity)",
  at="C", correct="Rheumatoid arthritis", wrong=["AIDS", "Typhoid", "Ascariasis"],
  why="AIDS is an immunodeficiency caused by HIV; typhoid is a bacterial infection; ascariasis is caused by a "
      "helminth.", secs=20)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Tobacco chewing is associated with an increased risk of:",
  "Effects of tobacco",
  "Smoking is associated with cancers of the lung, urinary bladder and throat, bronchitis, emphysema, coronary heart "
  "disease and gastric ulcer. Tobacco CHEWING is associated with an increased risk of cancer of the oral cavity.",
  ["Tobacco chewing → cancer of the oral cavity"],
  "Drugs and alcohol abuse (tobacco)",
  at="D", correct="Cancer of the oral cavity", wrong=["Elephantiasis", "Typhoid", "Diabetes insipidus"],
  why="Elephantiasis is caused by filarial worms, typhoid by Salmonella typhi, and diabetes insipidus by an ADH "
      "problem.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "Mary Mallon, nicknamed 'Typhoid Mary', is a famous case in medicine because she:",
  "Carriers of typhoid",
  "Mary Mallon was a cook and a typhoid carrier. She continued to spread typhoid for several years through the food "
  "she prepared.",
  ["Cook + typhoid carrier → spread typhoid through food for years"],
  "Common diseases in humans (typhoid)",
  at="B", correct="Was a cook and a typhoid carrier who spread typhoid for several years through the food she "
                  "prepared",
  wrong=["Developed the Widal test to confirm typhoid",
         "Was the first person to be vaccinated against typhoid",
         "Discovered that houseflies carry the typhoid bacterium"],
  why="She was a carrier, not a scientist; NCERT does not credit her with any test, vaccine or discovery.", secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "The colostrum secreted by the mother during the initial days of lactation protects the infant because it has "
  "abundant antibodies of the type:",
  "Passive immunity through colostrum",
  "The yellowish fluid colostrum, secreted by the mother during the initial days of lactation, has abundant "
  "antibodies (IgA) that protect the infant. This is an example of passive immunity.",
  ["Colostrum → abundant IgA", "Ready-made antibodies → passive immunity"],
  "Immunity (active and passive immunity)",
  at="A", correct="IgA", wrong=["IgE", "IgM", "IgD"],
  why="IgE is linked with allergies; IgM is another class NCERT lists but not the one it names for colostrum; IgD is "
      "not mentioned in this context.", secs=20)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Which of the following drugs are normally used as medicines to help patients cope with mental illnesses such as "
  "depression and insomnia, but are often abused?",
  "Drugs used as medicines",
  "NCERT lists barbiturates, amphetamines, benzodiazepines and other similar drugs as medicines normally used to help "
  "patients cope with mental illnesses like depression and insomnia; they are often abused.",
  ["Barbiturates, amphetamines, benzodiazepines → medicines for depression and insomnia, often abused"],
  "Drugs and alcohol abuse",
  at="B", correct="Barbiturates, amphetamines and benzodiazepines",
  wrong=["Interferons, antihistamines and antitoxins", "Cannabinoids, cocaine and heroin",
         "Nicotine, haemozoin and histamine"],
  why="Interferons and antitoxins are not drugs for depression; cannabinoids, cocaine and heroin are not used as "
      "medicines for these illnesses; haemozoin and histamine are not drugs at all.", secs=30)

Z(HHD, "HIV and AIDS", B, D,
  "AIDS (Acquired Immuno Deficiency Syndrome) was first reported in the year:",
  "History of AIDS",
  "AIDS was first reported in 1981; in the years since, it has spread all over the world, killing millions of "
  "people.",
  ["AIDS first reported → 1981"],
  "AIDS",
  at="B", correct="1981", wrong=["1971", "1990", "1997"],
  why="1971, 1990 and 1997 are not the year NCERT gives; 1990 is linked with the first gene therapy and 1997 with "
      "the Basmati patent and Rosie the cow.", secs=20)

Z(HHD, "Pathogens and diseases", I, MAT,
  ML(("disease", "causative organism"), ["Pneumonia", "Filariasis", "Amoebiasis", "Ringworm"],
     ["Entamoeba histolytica",
      "Microsporum, Trichophyton and Epidermophyton",
      "Streptococcus pneumoniae and Haemophilus influenzae",
      "Wuchereria bancrofti and W. malayi"]),
  "Pathogens of common human diseases",
  "Pneumonia is caused by the bacteria Streptococcus pneumoniae and Haemophilus influenzae. Filariasis "
  "(elephantiasis) is caused by the filarial worms Wuchereria bancrofti and W. malayi. Amoebiasis (amoebic "
  "dysentery) is caused by the protozoan Entamoeba histolytica. Ringworm is caused by fungi of the genera "
  "Microsporum, Trichophyton and Epidermophyton.",
  ["Pneumonia → III", "Filariasis → IV", "Amoebiasis → I", "Ringworm → II"],
  "Common diseases in humans",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The wrong codes give pneumonia the filarial worms, swap the protozoan with the fungi, or give pneumonia the "
      "amoeba.", secs=45)

Z(HHD, "Pathogens and diseases", I, STP,
  SP("The sexual stages (gametocytes) of Plasmodium develop in the red blood cells of the infected human.",
     "The sporozoites of Plasmodium are stored in the salivary glands of the female Anopheles mosquito."),
  "Life cycle of Plasmodium",
  "In humans, Plasmodium multiplies first in liver cells and then in RBCs; the sexual stages (gametocytes) develop "
  "in the RBCs. A female Anopheles takes up the gametocytes with a blood meal; fertilisation and development take "
  "place in the mosquito's stomach, and the sporozoites formed are stored in its salivary glands, ready to be "
  "injected at the next bite.",
  ["Statement I: true", "Statement II: true"],
  "Common diseases in humans (malaria)", ans="A",
  why="Both are NCERT facts; gametocytes FORM in human RBCs even though fertilisation happens in the mosquito.",
  secs=35)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("Active immunity is slow and takes time to give its full effective response.",
     "In active immunity, the host is exposed to antigens and has to produce its own antibodies."),
  "Active immunity",
  "When a host is exposed to antigens (living or dead microbes or other proteins), antibodies are produced in the "
  "host body; this is active immunity. Because the body must itself respond to the antigen and produce antibodies, "
  "active immunity is slow and takes time to give its full effective response. Passive immunity, with ready-made "
  "antibodies, acts at once.",
  ["A: true", "R: true", "The need to make its own antibodies is why active immunity is slow"],
  "Immunity (active and passive immunity)", ans="A",
  why="R gives the cause of the delay, so B is wrong; both statements are NCERT facts, so C and D are wrong.",
  secs=40)

Z(HHD, "Immunity and vaccines", I, MUL,
  MS("Which of the following statements about allergies are correct?",
     ["Allergy is the exaggerated response of the immune system to certain antigens present in the environment.",
      "In allergic reactions, chemicals such as histamine and serotonin are released from mast cells.",
      "Drugs such as anti-histamine, adrenalin and steroids quickly reduce the symptoms of allergy.",
      "In an allergy, the immune system attacks the body's own (self) cells.",
      "Modern-day life style has resulted in lowering of immunity and more sensitivity to allergens."]),
  "Allergies",
  "Allergy is the exaggerated response of the immune system to certain antigens (allergens) in the environment. "
  "Mast cells release chemicals like histamine and serotonin. Anti-histamine, adrenalin and steroids quickly reduce "
  "the symptoms. Modern-day life style has lowered immunity and increased sensitivity to allergens. An immune attack "
  "on self-cells is AUTO-IMMUNITY, not allergy.",
  ["(a) True", "(b) True", "(c) True", "(d) False: that is auto-immunity", "(e) True"],
  "Immunity (allergies)",
  at="C", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="Options with (d) confuse allergy with auto-immunity.", secs=55)

Z(HHD, "Cancer", I, STP,
  SP("Cancer cells actively divide and grow and starve the normal cells by competing for vital nutrients.",
     "Malignant tumours grow slowly and do not damage the surrounding normal tissues."),
  "Malignant tumours",
  "Malignant tumours are masses of proliferating cells (neoplastic or tumour cells) that grow very rapidly, invading "
  "and damaging the surrounding normal tissues. Being actively dividing and growing, cancer cells also starve normal "
  "cells by competing for vital nutrients.",
  ["Statement I: true", "Statement II: false (malignant tumours grow rapidly and damage surrounding tissues)"],
  "Cancer", ans="C",
  why="Statement II contradicts NCERT's description of malignant tumours (rapid, invasive growth), so A and D are "
      "wrong; Statement I is an NCERT line, so B is wrong.", secs=35)

Z(HHD, "Cancer", I, D,
  "In a suspected case of leukaemia, NCERT states that cancer can be detected by:",
  "Detection of leukaemias",
  "Cancer detection is based on biopsy and histopathological studies of the tissue, and on blood and bone marrow "
  "tests for increased cell counts in the case of leukaemias.",
  ["Leukaemias → blood and bone marrow tests for increased cell counts"],
  "Cancer (cancer detection and diagnosis)",
  at="D", correct="Blood and bone marrow tests for increased cell counts",
  wrong=["The Widal test", "ELISA for antibodies against HIV", "Testing the urine for ketone bodies"],
  why="The Widal test confirms typhoid; ELISA is a diagnostic test for AIDS; ketone bodies in urine indicate "
      "diabetes mellitus.", secs=30)

Z(HHD, "Drug and alcohol abuse", I, MAT,
  ML(("drug", "plant source"), ["Heroin (from morphine)", "Marijuana, hashish, charas and ganja", "Cocaine",
                                "Drugs with hallucinogenic properties"],
     ["Erythroxylum coca", "Atropa belladonna and Datura", "Latex of the poppy plant Papaver somniferum",
      "Inflorescences of Cannabis sativa"]),
  "Sources of commonly abused drugs",
  "Morphine is extracted from the latex of the poppy plant Papaver somniferum; heroin is its acetylated form. "
  "Cannabinoids (marijuana, hashish, charas, ganja) come from the inflorescences of Cannabis sativa. Cocaine comes "
  "from the coca plant Erythroxylum coca, native to South America. Atropa belladonna and Datura are plants with "
  "hallucinogenic properties.",
  ["Heroin → III", "Cannabinoids → IV", "Cocaine → I", "Hallucinogens → II"],
  "Drugs and alcohol abuse",
  at="A", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The trap codes swap poppy and Cannabis, swap coca with Datura, or give heroin the coca plant.", secs=45)

Z(HHD, "HIV and AIDS", I, ASR,
  AR("HIV is a member of the retrovirus group.",
     "HIV has an envelope enclosing a DNA genome."),
  "Nature of HIV",
  "AIDS is caused by HIV, a member of the retrovirus group, which has an envelope enclosing an RNA genome. Being a "
  "retrovirus, it uses reverse transcriptase to copy its RNA into viral DNA inside the host cell.",
  ["A: true", "R: false, because the HIV genome is RNA"],
  "AIDS", ans="C",
  why="R is false, so options A and B fail; A is true, so D is wrong.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Repeated use of drugs decreases the tolerance level of the receptors present in the body, so that they respond "
     "to even lower doses of the drug.",
     "The withdrawal syndrome is characterised by anxiety, shakiness, nausea and sweating."),
  "Addiction and dependence",
  "Repeated use of drugs INCREASES the tolerance level of the receptors, so the receptors respond only to higher "
  "doses; this leads to greater intake and addiction. If regular dosing is abruptly stopped, the withdrawal syndrome "
  "appears, with anxiety, shakiness, nausea and sweating.",
  ["Statement I: false (tolerance increases; higher doses are needed)", "Statement II: true"],
  "Addiction and dependence", ans="D",
  why="Statement I reverses the NCERT statement, so options A and C are wrong; Statement II is an NCERT line, so B "
      "is wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", A, MUL,
  MS("Which of the following are listed in NCERT as side-effects of the misuse of anabolic steroids?",
     ["In females: masculinisation, increased aggressiveness, mood swings and depression.",
      "In females: shrinkage of the clitoris.",
      "In males: reduction in the size of the testicles and decreased sperm production.",
      "In males: decrease in the size of the prostate gland.",
      "In males: breast enlargement and premature baldness."]),
  "Effects of anabolic steroid misuse",
  "In females, misuse of anabolic steroids causes masculinisation, increased aggressiveness, mood swings, "
  "depression, abnormal menstrual cycles, excessive hair growth on the face and body, ENLARGEMENT of the clitoris and "
  "deepening of the voice. In males it causes acne, increased aggressiveness, mood swings, depression, reduction in "
  "the size of the testicles, decreased sperm production, possible kidney and liver dysfunction, breast "
  "enlargement, premature baldness and ENLARGEMENT of the prostate gland.",
  ["(a) True", "(b) False: the clitoris enlarges", "(c) True", "(d) False: the prostate enlarges", "(e) True"],
  "Effects of drug and alcohol abuse",
  at="B", correct="(a), (c) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"],
  why="Options with (b) or (d) reverse the direction of change; NCERT lists ENLARGEMENT of both the clitoris and the "
      "prostate.", secs=65)

Z(HHD, "Cancer", A, MUL,
  MS("Which of the following statements about the detection and treatment of cancer are correct?",
     ["Biopsy and histopathological studies of the tissue are used to detect cancer.",
      "Antibodies against cancer-specific antigens are also used for the detection of certain cancers.",
      "Chemotherapeutic drugs used against cancer have no side effects.",
      "Tumour cells are easily detected and destroyed by the patient's immune system.",
      "Techniques of molecular biology can detect genes in individuals with an inherited susceptibility to certain "
      "cancers."]),
  "Cancer detection and treatment",
  "Cancer is detected by biopsy and histopathological study, blood and bone-marrow tests (for leukaemias), "
  "radiography, CT, MRI, antibodies against cancer-specific antigens, and molecular techniques that detect genes "
  "of inherited susceptibility. Most chemotherapeutic drugs have side effects such as hair loss and anaemia. Tumour "
  "cells have been shown to AVOID detection and destruction by the immune system, which is why biological response "
  "modifiers such as α-interferon are given.",
  ["(a) True", "(b) True", "(c) False: hair loss, anaemia", "(d) False: tumour cells evade the immune system",
   "(e) True"],
  "Cancer (detection, diagnosis and treatment)",
  at="D", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="Options with (c) deny the known side effects of chemotherapy; options with (d) ignore that tumour cells evade "
      "the immune system.", secs=65)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Lymph nodes trap micro-organisms or other antigens that happen to get into the lymph and tissue fluid.",
     "Mucosa-associated lymphoid tissue (MALT) is located within the lining of the major tracts: the respiratory, "
     "digestive and urogenital tracts."),
  "Secondary lymphoid organs",
  "Lymph nodes are small solid structures along the lymphatic system; they trap micro-organisms or antigens in the "
  "lymph and tissue fluid, and the trapped antigens activate lymphocytes there. MALT, located in the lining of the "
  "major tracts, is another lymphoid tissue. Both statements are true, but the location of MALT has nothing to do "
  "with why lymph nodes trap antigens.",
  ["A: true", "R: true", "R is about a different lymphoid tissue; it cannot explain A"],
  "Immunity (lymphoid organs)", ans="B",
  why="R concerns MALT, not lymph nodes, so it cannot be the explanation (option A is wrong); both statements are "
      "true, so C and D are wrong.", secs=40)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("disease", "symptoms"), ["Common cold", "Typhoid", "Ringworm", "Pneumonia"],
     ["Dry, scaly lesions on the skin, nails and scalp, with intense itching",
      "Infection of the alveoli of the lungs, with fever, chills, cough and headache",
      "Nasal congestion and discharge, sore throat, hoarseness and cough, lasting 3–7 days",
      "Sustained high fever (39–40 °C), weakness, stomach pain and constipation; intestinal perforation in severe "
      "cases"]),
  "Symptoms of common human diseases",
  "The common cold (rhinoviruses) causes nasal congestion and discharge, sore throat, hoarseness, cough, headache "
  "and tiredness, usually lasting 3–7 days. Typhoid causes sustained high fever (39–40 °C), weakness, stomach pain, "
  "constipation, headache and loss of appetite, with intestinal perforation in severe cases. Ringworm causes dry, "
  "scaly lesions with intense itching. Pneumonia infects the alveoli and causes fever, chills, cough and headache.",
  ["Common cold → III", "Typhoid → IV", "Ringworm → I", "Pneumonia → II"],
  "Common diseases in humans",
  at="A", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The trap codes give the common cold the alveolar (lung) infection, which NCERT says it does not cause, or "
      "swap typhoid with pneumonia or with the common cold.", secs=55)

Z(HHD, "HIV and AIDS", A, STP,
  SP("A person infected with HIV shows the symptoms of AIDS within a few days of infection.",
     "Anti-retroviral drugs completely cure AIDS."),
  "Course and treatment of AIDS",
  "The time lag between HIV infection and the appearance of AIDS symptoms may vary from a few months to many years "
  "(usually 5–10 years). Treatment with anti-retroviral drugs is only partially effective: it can prolong the life "
  "of the patient but cannot prevent death.",
  ["Statement I: false (time lag of months to years, usually 5–10 years)",
   "Statement II: false (anti-retroviral drugs only prolong life)"],
  "AIDS", ans="B",
  why="Both statements contradict NCERT, so every option that calls either one true is wrong.", secs=40)

Z(HHD, "Immunity and vaccines", A, D,
  "A person bitten by a poisonous snake is given an injection to neutralise the venom quickly. The immunity provided "
  "by this injection is:",
  "Passive immunisation with antitoxin",
  "The injection given to people bitten by snakes contains preformed antibodies against the snake venom. Because "
  "ready-made antibodies are given, this is passive immunisation; it acts at once, while active immunity would take "
  "too long.",
  ["Injection contains preformed antibodies against venom", "Ready-made antibodies → passive immunity"],
  "Immunity (vaccination and immunisation)",
  at="C", correct="Passive immunity, because preformed antibodies against the venom are injected",
  wrong=["Active immunity, because a weakened form of the venom makes the body produce memory cells",
         "Innate immunity, because the injection strengthens physical barriers such as the skin",
         "Active immunity, because the injection contains the snake's antigens"],
  why="Active immunity needs the body to make its own antibodies and is slow; innate immunity is non-specific and is "
      "not given by injection.", secs=40)

Z(HHD, "Drug and alcohol abuse", A, MUL,
  MS("Which of the following statements about drug and alcohol abuse are correct?",
     ["Use of drugs and alcohol during pregnancy is known to adversely affect the foetus.",
      "Those who take drugs intravenously are much more likely to acquire serious infections like AIDS and "
      "hepatitis B.",
      "Morphine is a very effective sedative and painkiller and is very useful in patients who have undergone "
      "surgery.",
      "Smoking is associated with increased incidence of cancers of the lung, urinary bladder and throat.",
      "Heroin is a stimulant that speeds up body functions."]),
  "Effects of drugs and alcohol",
  "NCERT states that drugs and alcohol during pregnancy adversely affect the foetus; intravenous drug users are more "
  "likely to get AIDS and hepatitis B; morphine is a very effective sedative and painkiller useful after surgery; and "
  "smoking increases the incidence of cancers of the lung, urinary bladder and throat. Heroin is a DEPRESSANT that "
  "slows down body functions.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: heroin is a depressant"],
  "Drugs and alcohol abuse; Effects of drug and alcohol abuse",
  at="A", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="Every option with (e) calls heroin a stimulant; NCERT calls it a depressant.", secs=60)

# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Restriction enzymes", B, D,
  "The construction of the first recombinant DNA, by linking a gene encoding antibiotic resistance with a native "
  "plasmid of Salmonella typhimurium, was accomplished in 1972 by:",
  "First recombinant DNA",
  "The construction of the first recombinant DNA emerged from the possibility of linking a gene encoding antibiotic "
  "resistance with a native plasmid (autonomously replicating circular extra-chromosomal DNA) of Salmonella "
  "typhimurium. Stanley Cohen and Herbert Boyer accomplished this in 1972.",
  ["First recombinant DNA → 1972", "Stanley Cohen and Herbert Boyer"],
  "Principles of biotechnology",
  at="B", correct="Stanley Cohen and Herbert Boyer", wrong=["Watson and Crick", "Meselson and Stahl",
                                                         "Oparin and Haldane"],
  why="Watson and Crick proposed the double helix; Meselson and Stahl proved semi-conservative replication; Oparin "
      "and Haldane proposed chemical evolution.", secs=25)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "In agarose gel electrophoresis, DNA fragments move through the gel towards the:",
  "Direction of DNA movement in gel electrophoresis",
  "DNA fragments are negatively charged molecules, so in an electric field they move towards the anode (positive "
  "electrode) through the agarose matrix.",
  ["DNA → negatively charged (phosphate backbone)", "Moves towards the anode (positive electrode)"],
  "Separation and isolation of DNA fragments",
  at="A", correct="Anode (positive electrode), because DNA is negatively charged",
  wrong=["Cathode (negative electrode), because DNA is positively charged",
         "Cathode, because larger fragments are heavier",
         "Neither electrode, because DNA is uncharged"],
  why="DNA is negatively charged, so it cannot move to the cathode; size decides how far fragments move, not their "
      "direction.", secs=25)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "Agarose, the matrix most commonly used in gel electrophoresis of DNA, is a natural polymer extracted from:",
  "Agarose gel",
  "The most commonly used matrix for separating DNA fragments is agarose, a natural polymer extracted from sea "
  "weeds. It separates fragments by size through a sieving effect.",
  ["Agarose → natural polymer from sea weeds"],
  "Separation and isolation of DNA fragments",
  at="C", correct="Sea weeds", wrong=["Bacterial cell walls", "Fungal hyphae", "Insect exoskeletons"],
  why="NCERT names sea weeds as the source; the other sources (bacterial walls, fungi, insect chitin) are wrong.",
  secs=20)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "After agarose gel electrophoresis, the separated bands of DNA are cut out from the gel and extracted from the gel "
  "piece. This step is called:",
  "Elution",
  "The separated DNA bands are cut out from the agarose gel and extracted from the gel piece. This step is known as "
  "elution. The purified DNA fragments are then used to construct recombinant DNA by joining them with cloning "
  "vectors.",
  ["Cut out band → extract DNA from gel piece = elution"],
  "Separation and isolation of DNA fragments",
  at="D", correct="Elution", wrong=["Annealing", "Spooling", "Transformation"],
  why="Annealing is primer binding in PCR; spooling is collecting precipitated DNA threads; transformation is "
      "introduction of DNA into a host bacterium.", secs=20)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "In each cycle of the polymerase chain reaction (PCR), the step in which the primers bind to the complementary "
  "regions of the single-stranded template DNA is called:",
  "Steps of PCR",
  "Each PCR cycle has three steps: denaturation (high temperature separates the two DNA strands), annealing (two sets "
  "of primers bind to complementary regions of the template) and extension (DNA polymerase extends the primers using "
  "the nucleotides provided).",
  ["Denaturation → strands separate", "Annealing → primers bind", "Extension → polymerase extends primers"],
  "Amplification of gene of interest using PCR",
  at="B", correct="Annealing", wrong=["Denaturation", "Extension", "Elution"],
  why="Denaturation separates the strands; extension synthesises new DNA; elution is extraction of DNA from a gel.",
  secs=20)

Z(BPP, "Restriction enzymes", I, NUM,
  "A circular plasmid of 6,000 bp has two recognition sites for a restriction enzyme, at positions 1,000 bp and "
  "2,500 bp on its map. If the plasmid is completely digested with this enzyme, the fragments obtained will be:",
  "Restriction digestion of circular DNA",
  "A circular molecule cut at n sites gives n fragments. The two sites divide the circle into the stretch between "
  "them (2,500 − 1,000 = 1,500 bp) and the rest of the circle (6,000 − 1,500 = 4,500 bp).",
  ["Circular DNA, 2 sites → 2 fragments", "Between the sites: 2,500 − 1,000 = 1,500 bp",
   "Rest of the circle: 6,000 − 1,500 = 4,500 bp (check: 1,500 + 4,500 = 6,000)"],
  "Tools of recombinant DNA technology (restriction enzymes)",
  at="B", correct="Two fragments, of 1,500 bp and 4,500 bp",
  wrong=["Three fragments, of 1,000 bp, 1,500 bp and 3,500 bp",
         "Two fragments, of 2,500 bp and 3,500 bp",
         "Two fragments, of 1,000 bp and 5,000 bp"],
  short="Circle: n cuts → n pieces; the pieces must add up to the plasmid size.",
  why="Three fragments treats the plasmid as linear; 2,500 + 3,500 uses a site position as a fragment length; "
      "1,000 + 5,000 ignores the second site.", secs=60, vb=RECOMPUTED)

Z(BPP, "Competent hosts and transformation", I, ASR,
  AR("DNA cannot pass through the cell membrane of a host bacterium on its own.",
     "DNA is a hydrophilic molecule."),
  "Need for competent host cells",
  "Since DNA is a hydrophilic molecule, it cannot pass through cell membranes. Bacterial cells must therefore first "
  "be made 'competent', for example by treating them with a specific concentration of a divalent cation such as "
  "calcium, which increases the efficiency with which DNA enters through pores in the cell wall.",
  ["A: true", "R: true", "Being hydrophilic is the stated reason DNA cannot cross the lipid membrane"],
  "Processes of recombinant DNA technology (insertion of recombinant DNA into the host)", ans="A",
  why="NCERT gives R as the reason for A, so B is wrong; both statements are true, so C and D are wrong.", secs=35)

Z(BPP, "Competent hosts and transformation", I, STP,
  SP("After treatment with calcium, bacterial cells are incubated with recombinant DNA on ice, then placed briefly "
     "at 42 °C (heat shock), and then put back on ice.",
     "A protein-encoding gene expressed in a heterologous host gives a protein called a recombinant protein."),
  "Transformation by heat shock; recombinant protein",
  "Recombinant DNA can be forced into calcium-treated cells by incubating them with the DNA on ice, then placing them "
  "briefly at 42 °C (heat shock) and putting them back on ice; this lets the bacteria take up the DNA. When a "
  "protein-encoding gene is expressed in a heterologous host, the protein produced is called a recombinant protein.",
  ["Statement I: true", "Statement II: true"],
  "Competent host; Obtaining the foreign gene product", ans="A",
  why="Both statements are NCERT facts, so the options calling either false are wrong.", secs=40)

Z(BPP, "Cloning vectors", I, MUL,
  MS("Which of the following statements about cloning vectors are correct?",
     ["Some plasmids have only one or two copies per cell, whereas others may have 15–100 copies per cell.",
      "Bacteriophages have very high copy numbers of their genome within bacterial cells.",
      "A vector needs very few, preferably single, recognition sites for the commonly used restriction enzymes.",
      "Selection of recombinants by inactivation of an antibiotic resistance gene is cumbersome because it requires "
      "simultaneous plating on two plates having different antibiotics.",
      "The Ti plasmid of Agrobacterium tumefaciens, modified into a cloning vector, is still pathogenic to "
      "plants."]),
  "Features of cloning vectors",
  "Bacteriophages have very high copy numbers; plasmids vary from 1–2 to 15–100 copies per cell. A vector needs very "
  "few, preferably single, recognition sites for the commonly used restriction enzymes, because several sites "
  "would produce several fragments. Selection by antibiotic-resistance inactivation is cumbersome (two plates), so "
  "chromogenic substrates are used. The Ti plasmid has been modified into a vector that is NO MORE pathogenic to "
  "plants but can still deliver genes.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: the modified Ti plasmid is not pathogenic"],
  "Cloning vectors",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (e) only", "(b), (d) and (e) only"],
  why="Every option with (e) treats the disarmed Ti plasmid vector as still pathogenic.", secs=60)

Z(BPP, "Restriction enzymes", I, MAT,
  ML(("agent used in recombinant DNA work", "purpose"),
     ["Ribonuclease", "Chilled ethanol", "Restriction enzyme", "Agarose gel electrophoresis"],
     ["Precipitates the purified DNA, which appears as fine threads in suspension",
      "Removes RNA from the DNA preparation",
      "Checks the progression of a restriction enzyme digestion",
      "Cuts DNA at a specific recognition sequence"]),
  "Isolating and cutting DNA",
  "During isolation of DNA, RNA is removed by treatment with ribonuclease, and the purified DNA finally precipitates "
  "out after addition of chilled ethanol (seen as fine threads). Purified DNA is then incubated with a restriction "
  "enzyme, which cuts it at specific recognition sequences; agarose gel electrophoresis is used to check the "
  "progression of the digestion.",
  ["Ribonuclease → II", "Chilled ethanol → I", "Restriction enzyme → IV", "Agarose gel → III"],
  "Processes of recombinant DNA technology (isolation and cutting of DNA)",
  at="B", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"}]),
  why="The wrong codes swap the roles of ribonuclease and ethanol, swap the enzyme with the gel, or make "
      "ribonuclease cut DNA.", secs=45)

Z(BPP, "Bioreactors and downstream processing", I, D,
  "Which of the following is a part of downstream processing?",
  "Downstream processing",
  "After biosynthesis, the product undergoes downstream processing: separation and purification, followed by "
  "formulation with suitable preservatives. For drugs, the formulation must undergo clinical trials, and strict "
  "quality control testing is required for every product.",
  ["Downstream processing → separation and purification", "→ formulation with preservatives",
   "→ clinical trials (drugs) and quality control"],
  "Processes of recombinant DNA technology (downstream processing)",
  at="D", correct="Separation and purification of the product, followed by formulation with suitable preservatives",
  wrong=["Making bacterial cells competent with calcium ions",
         "Amplifying the gene of interest by PCR",
         "Cutting the vector DNA with a restriction enzyme"],
  why="Making cells competent, PCR and cutting the vector are all upstream steps of making the recombinant organism.",
  secs=30)

Z(BPP, "PCR and gel electrophoresis", I, ASR,
  AR("In agarose gel electrophoresis, larger DNA fragments move farther from the well than smaller fragments.",
     "DNA fragments separate according to their size through the sieving effect of the agarose gel."),
  "Separation of DNA fragments by size",
  "Agarose gel separates DNA fragments by size through a sieving effect: the SMALLER the fragment, the FARTHER it "
  "moves. So larger fragments stay nearer the well.",
  ["A: false (smaller fragments move farther)", "R: true"],
  "Separation and isolation of DNA fragments", ans="D",
  why="A is false, so options A, B and C, which all need A to be true, are wrong.", secs=35)

Z(BPP, "PCR and gel electrophoresis", A, NUM,
  "A linear DNA molecule of 10 kb has EcoRI sites at 2 kb and 7 kb from its left end and a BamHI site at 5 kb from "
  "its left end. It is completely digested with both EcoRI and BamHI together, and the products are run on an "
  "agarose gel and stained. How many distinct bands will be seen?",
  "Double digestion and band pattern",
  "Three cuts (at 2, 5 and 7 kb) on a linear molecule give four fragments: 0–2 = 2 kb, 2–5 = 3 kb, 5–7 = 2 kb and "
  "7–10 = 3 kb. Fragments of the same size move the same distance, so the two 2 kb pieces form one band and the two "
  "3 kb pieces form another band.",
  ["Cut positions: 2, 5, 7 kb → 4 fragments on a linear molecule", "Sizes: 2, 3, 2, 3 kb (total 10 kb)",
   "Same size → same band → 2 distinct bands"],
  "Separation and isolation of DNA fragments",
  at="A", correct="2", wrong=["4", "3", "1"],
  short="Bands = number of DIFFERENT fragment sizes, not the number of fragments.",
  why="4 counts each fragment as a separate band; 3 is the number of cuts (or the EcoRI-only digest, 2 + 5 + 3 kb); "
      "1 would need all four fragments to be the same size.", secs=90, vb=RECOMPUTED)

Z(BPP, "Cloning vectors", A, MAT,
  ML(("term", "meaning"), ["Transformation", "Palindromic sequence", "Primers", "DNA ligase"],
     ["Small, chemically synthesised oligonucleotides complementary to regions of the template DNA",
      "Enzyme that joins the cut ends of the vector and the foreign DNA",
      "Procedure through which a piece of DNA is introduced into a host bacterium",
      "Base sequence that reads the same on the two strands when the orientation of reading is kept the same"]),
  "Key terms of recombinant DNA technology",
  "Transformation is the procedure by which a piece of DNA is introduced into a host bacterium. A palindromic "
  "sequence reads the same on the two strands when both are read in the same orientation (5'→3'). Primers are small "
  "chemically synthesised oligonucleotides complementary to regions of DNA, used in PCR. DNA ligase joins the cut "
  "ends of the vector and the foreign DNA.",
  ["Transformation → III", "Palindrome → IV", "Primers → I", "DNA ligase → II"],
  "Tools of recombinant DNA technology; Amplification using PCR",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The wrong codes swap transformation and palindrome, swap primers with ligase, or swap primers with "
      "transformation.", secs=50)

Z(BPP, "Bioreactors and downstream processing", A, MUL,
  MS("Which of the following statements about bioreactors are correct?",
     ["A bioreactor provides the optimal growth conditions (temperature, pH, substrate, salts, vitamins, oxygen) for "
      "achieving the desired product.",
      "In a bioreactor, air is never bubbled through the culture; oxygen is supplied only by the stirrer.",
      "In a stirred-tank bioreactor, the stirrer facilitates even mixing and oxygen availability throughout the "
      "bioreactor.",
      "A bioreactor has a foam control system, a pH control system and sampling ports."]),
  "Bioreactors",
  "Bioreactors provide optimal temperature, pH, substrate, salts, vitamins and oxygen. In the stirred-tank type, the "
  "stirrer facilitates even mixing and oxygen availability; ALTERNATIVELY, air can be bubbled through the reactor. A "
  "bioreactor has an agitator system, an oxygen delivery system, a foam control system, a temperature control "
  "system, a pH control system and sampling ports.",
  ["(a) True", "(b) False: air can be bubbled through the reactor", "(c) True", "(d) True"],
  "Processes of recombinant DNA technology (bioreactors)",
  at="B", correct="(a), (c) and (d) only",
  wrong=["(a), (b), (c) and (d)", "(b), (c) and (d) only", "(a) and (c) only"],
  why="Options with (b) deny air bubbling, which NCERT gives as an alternative; (a) and (c) only leaves out (d), "
      "which lists components NCERT names.", secs=50)

Z(BPP, "Cloning vectors", A, ASR,
  AR("When a vector carrying the ampicillin resistance gene is transferred into E. coli and the cells are spread on "
     "agar plates containing ampicillin, only the transformants grow.",
     "Normal E. coli cells do not carry resistance against ampicillin."),
  "Selectable markers",
  "Normal E. coli cells carry no resistance to ampicillin, chloramphenicol, tetracycline or kanamycin. Cells that "
  "take up a vector with the ampicillin resistance gene become ampicillin-resistant. On ampicillin plates the "
  "untransformed cells die, so only transformants grow; the ampicillin resistance gene acts as a selectable "
  "marker.",
  ["A: true", "R: true", "Untransformed cells lack resistance and die, which is why only transformants grow"],
  "Cloning vectors (selectable marker); Insertion of recombinant DNA into the host", ans="A",
  why="R is exactly why untransformed cells fail to grow, so B is wrong; both statements are true, so C and D are "
      "wrong.", secs=45)

Z(BPP, "Restriction enzymes", A, STP,
  SP("Fewer than 50 restriction enzymes have been isolated so far, all of them from Escherichia coli.",
     "Restriction enzymes belong to a larger class of enzymes called nucleases."),
  "Restriction enzymes as nucleases",
  "Today more than 900 restriction enzymes have been isolated from over 230 strains of bacteria, each recognising "
  "different sequences. Restriction enzymes belong to the larger class of nucleases, which are of two kinds: "
  "exonucleases and endonucleases.",
  ["Statement I: false (more than 900 enzymes from over 230 bacterial strains)", "Statement II: true"],
  "Tools of recombinant DNA technology (restriction enzymes)", ans="D",
  why="Statement I is wrong on both the number and the source, so A and C are wrong; Statement II is an NCERT line, "
      "so B is wrong.", secs=40)

# ================================================================ Biotechnology and its Applications (5/7/5)
Z(BTA, "Bt crops and RNAi", B, D,
  "Genetically modified (GM) plants have increased the efficiency of mineral usage by plants. According to NCERT, "
  "this helps to:",
  "Benefits of GM plants",
  "Among the uses of genetic modification listed by NCERT: GM plants have increased the efficiency of mineral usage "
  "by plants, and this prevents early exhaustion of the fertility of the soil.",
  ["Better mineral-use efficiency → less drain on soil nutrients → soil fertility not exhausted early"],
  "Biotechnological applications in agriculture",
  at="C", correct="Prevent early exhaustion of the fertility of the soil",
  wrong=["Increase the use of chemical fertilisers", "Make the plants resistant to insect pests",
         "Enrich the grain with vitamin A"],
  why="Better mineral use reduces, not increases, the need for fertilisers; insect resistance comes from Bt genes; "
      "vitamin A enrichment is the golden rice example of enhanced nutritional value.", secs=25)

Z(BTA, "Human insulin", B, D,
  "The American company Eli Lilly prepared two DNA sequences corresponding to the A and B chains of human insulin "
  "and introduced them into plasmids of E. coli to produce insulin chains. This was done in the year:",
  "Genetically engineered insulin",
  "In 1983, Eli Lilly, an American company, prepared two DNA sequences corresponding to the A and B chains of human "
  "insulin and introduced them into plasmids of E. coli to produce the insulin chains.",
  ["Eli Lilly → 1983"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="B", correct="1983", wrong=["1963", "1972", "1997"],
  why="1963 is when the first two restriction-related enzymes were isolated; 1972 is the first recombinant DNA "
      "(Cohen and Boyer); 1997 is the year of Rosie the transgenic cow and the Basmati patent.", secs=25)

Z(BTA, "Transgenic animals", B, D,
  "According to NCERT, attempts are being made to use transgenic animals and their products in the treatment of:",
  "Biological products from transgenic animals",
  "Transgenic animals that produce useful biological products can be created by introducing the portion of DNA (or "
  "genes) that codes for a particular product. Besides α-1-antitrypsin (for emphysema), similar attempts are being "
  "made for the treatment of phenylketonuria (PKU) and cystic fibrosis.",
  ["Transgenic animals → useful biological products", "Attempts underway: phenylketonuria (PKU), cystic fibrosis"],
  "Transgenic animals",
  at="C", correct="Phenylketonuria (PKU) and cystic fibrosis",
  wrong=["Typhoid and pneumonia", "Malaria and filariasis", "Common cold and ringworm"],
  why="The other pairs are infectious diseases that NCERT does not link with products of transgenic animals.",
  secs=25)

Z(BTA, "Transgenic animals", B, D,
  "Animals that have had their DNA manipulated to possess and express an extra (foreign) gene are known as:",
  "Transgenic animals",
  "Animals that have had their DNA manipulated to possess and express an extra (foreign) gene are called transgenic "
  "animals. Transgenic rats, rabbits, pigs, sheep, cows and fish have been produced, although over 95 per cent of "
  "existing transgenic animals are mice.",
  ["Extra (foreign) gene inserted and expressed → transgenic animal"],
  "Transgenic animals",
  at="D", correct="Transgenic animals", wrong=["Hybrid animals", "Polyploid animals", "Inbred animals"],
  why="Hybrids come from crossing two varieties; polyploids have extra chromosome sets; inbreds come from mating "
      "closely related individuals. None of these involves inserting a foreign gene.", secs=20)

Z(BTA, "Biosafety, biopiracy and patents", B, D,
  "Besides the Basmati patent, NCERT notes that attempts have been made to patent uses, products and processes based "
  "on Indian traditional herbal medicines. Which two examples does it give?",
  "Patents on Indian bio-resources",
  "After describing the 1997 US patent on Basmati, NCERT notes that several attempts have also been made to patent "
  "uses, products and processes based on Indian traditional herbal medicines, giving turmeric and neem as examples.",
  ["Attempts to patent products of Indian traditional herbal medicines → turmeric, neem"],
  "Ethical issues",
  at="C", correct="Turmeric and neem", wrong=["Tea and coffee", "Cotton and jute", "Wheat and maize"],
  why="NCERT names only turmeric and neem in this context; the other pairs are not herbal medicines it mentions.",
  secs=20)

Z(BTA, "Bt crops and RNAi", I, MUL,
  MS("Which of the following statements about genetically modified (GM) plants are correct?",
     ["Genetic modification has made crops more tolerant to abiotic stresses such as cold, drought, salt and heat.",
      "GM plants have helped to reduce post-harvest losses.",
      "Genetic modification has enhanced the nutritional value of food.",
      "Genetically modified organisms (GMOs) can only be plants; bacteria, fungi and animals cannot be "
      "genetically modified.",
      "GM crops have increased the reliance on chemical pesticides."]),
  "Uses of genetically modified plants",
  "Plants, bacteria, fungi and animals whose genes have been altered by manipulation are all GMOs. GM plants are more "
  "tolerant to abiotic stresses, have REDUCED reliance on chemical pesticides (pest-resistant crops), help reduce "
  "post-harvest losses, increase the efficiency of mineral usage and enhance the nutritional value of food (e.g. "
  "golden rice).",
  ["(a) True", "(b) True", "(c) True", "(d) False: GMOs include bacteria, fungi and animals too",
   "(e) False: pest-resistant GM crops reduce reliance on pesticides"],
  "Biotechnological applications in agriculture",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="Options with (d) restrict GMOs to plants; options with (e) reverse the effect of pest-resistant crops.",
  secs=55)

Z(BTA, "Bt crops and RNAi", I, STP,
  SP("The nematode Meloidegyne incognitia infects the leaves of tobacco plants.",
     "Tailor-made GM plants cannot be used to supply alternative resources such as starches, fuels and "
     "pharmaceuticals to industries."),
  "Pest resistance and tailor-made plants",
  "NCERT states that the nematode Meloidegyne incognitia infects the ROOTS of tobacco plants and causes a great "
  "reduction in yield. It also states that GM has been used to create tailor-made plants that supply alternative "
  "resources to industries in the form of starches, fuels and pharmaceuticals.",
  ["Statement I: false (the nematode infects the roots)",
   "Statement II: false (tailor-made plants do supply starches, fuels and pharmaceuticals)"],
  "Biotechnological applications in agriculture", ans="B",
  why="Both statements contradict NCERT, so every option that accepts either one is wrong.", secs=40)

Z(BTA, "Human insulin", I, ASR,
  AR("Recombinant DNA technology has made possible the mass production of safe and more effective therapeutic drugs.",
     "Recombinant therapeutics do not induce unwanted immunological responses, as is common with similar products "
     "isolated from non-human sources."),
  "Recombinant therapeutics",
  "NCERT: rDNA technology has enabled mass production of safe and more effective therapeutic drugs, because the "
  "recombinant therapeutics do not induce unwanted immunological responses, as is common in the case of similar "
  "products isolated from non-human sources (e.g. insulin from cattle and pigs).",
  ["A: true", "R: true", "Absence of unwanted immune reactions is why these drugs are called safe"],
  "Biotechnological applications in medicine", ans="A",
  why="R is the reason the drugs are safer, so B is wrong; both statements are NCERT facts, so C and D are wrong.",
  secs=40)

Z(BTA, "Biosafety, biopiracy and patents", I, D,
  "According to NCERT, how many documented varieties of Basmati rice are grown in India alone?",
  "Basmati diversity in India",
  "India has about 200,000 varieties of rice, and there are 27 documented varieties of Basmati grown in India alone. "
  "Basmati is distinct for its unique aroma and flavour.",
  ["Rice varieties in India → about 200,000", "Documented Basmati varieties in India → 27"],
  "Ethical issues",
  at="B", correct="27", wrong=["2", "270", "200,000"],
  why="200,000 is the number of rice varieties in India, not of Basmati; 2 and 270 are not NCERT figures.", secs=25)

Z(BTA, "Gene therapy", I, D,
  "According to NCERT, which of the following could be a permanent cure for adenosine deaminase (ADA) deficiency?",
  "Permanent cure through gene therapy",
  "Bone marrow transplantation and enzyme replacement therapy are not completely curative. In gene therapy with "
  "genetically engineered lymphocytes, the cells are not immortal, so periodic infusions are needed. NCERT states "
  "that if the gene isolated from marrow cells producing ADA is introduced into cells at early embryonic stages, it "
  "could be a permanent cure.",
  ["Bone marrow transplant, enzyme replacement → not completely curative",
   "Engineered lymphocytes → periodic infusions needed", "ADA gene into early embryonic cells → permanent cure"],
  "Biotechnological applications in medicine (gene therapy)",
  at="D", correct="Introducing the gene isolated from ADA-producing marrow cells into cells at early embryonic stages",
  wrong=["Periodic infusion of genetically engineered lymphocytes",
         "Enzyme replacement therapy with functional ADA",
         "A single infusion of mature lymphocytes from a healthy donor"],
  why="Engineered lymphocytes are not immortal, so infusions must be repeated; enzyme replacement is not completely "
      "curative; mature donor lymphocytes do not correct the patient's own gene.", secs=40)

Z(BTA, "Transgenic animals", I, STP,
  SP("Mice are the only animals that have been made transgenic so far.",
     "Transgenic animals can be specifically designed to allow the study of how genes are regulated and how they "
     "affect the normal functions of the body and its development."),
  "Transgenic animals and their uses",
  "Transgenic rats, rabbits, pigs, sheep, cows and fish have been produced, although over 95 per cent of all existing "
  "transgenic animals are mice. One use of transgenic animals is the study of normal physiology and development, for "
  "example the study of how genes are regulated and how they affect normal body functions and development.",
  ["Statement I: false (rats, rabbits, pigs, sheep, cows and fish have also been made transgenic)",
   "Statement II: true"],
  "Transgenic animals", ans="D",
  why="'Over 95 per cent are mice' does not mean 'only mice', so Statement I is false and options A and C are "
      "wrong; Statement II is an NCERT use, so B is wrong.", secs=40)

Z(BTA, "Biosafety, biopiracy and patents", I, MUL,
  MS("Which of the following statements are correct according to NCERT?",
     ["India has about 200,000 varieties of rice.",
      "A patent is a right granted to the general public to use an invention commercially without restriction.",
      "Basmati rice is distinct for its unique aroma and flavour.",
      "Traditional knowledge related to bio-resources can be used to save time, effort and expenditure during the "
      "commercialisation of products based on these bio-resources."]),
  "Patents and Indian bio-resources",
  "India has about 200,000 varieties of rice; Basmati is distinct for its unique aroma and flavour. A patent is the "
  "right granted by a government to an INVENTOR to prevent others from commercial use of the invention. NCERT also "
  "notes that traditional knowledge related to bio-resources can be exploited to develop modern applications and "
  "can be used to save time, effort and expenditure during their commercialisation.",
  ["(a) True", "(b) False: a patent protects the inventor and prevents others' commercial use", "(c) True",
   "(d) True"],
  "Ethical issues",
  at="D", correct="(a), (c) and (d) only",
  wrong=["(a), (b), (c) and (d)", "(b), (c) and (d) only", "(a) and (b) only"],
  why="Options with (b) reverse the meaning of a patent.", secs=50)

Z(BTA, "Bt crops and RNAi", A, MUL,
  MS("Which of the following statements are correct according to NCERT?",
     ["The three options for increasing food production are agro-chemical based agriculture, organic agriculture "
      "and genetically engineered crop-based agriculture.",
      "Although the Green Revolution succeeded in tripling the food supply, it was not enough to feed the growing "
      "human population.",
      "For farmers in the developing world, agrochemicals are often too expensive, and further increases in yield "
      "with existing varieties are not possible using conventional breeding.",
      "Biotechnology deals with providing the best catalyst, creating optimal conditions for it through "
      "engineering, and downstream processing technologies.",
      "The Green Revolution increased the food supply about ten-fold."]),
  "Need for genetically engineered crops",
  "NCERT lists three options for increasing food production: agro-chemical based, organic, and genetically "
  "engineered crop-based agriculture. The Green Revolution TRIPLED the food supply, which was still not enough. "
  "Agrochemicals are often too expensive for farmers in developing countries, and conventional breeding cannot "
  "raise yields of existing varieties further. Biotechnology works in three critical research areas: the best "
  "catalyst, optimal conditions through engineering, and downstream processing.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: the food supply tripled, not increased ten-fold"],
  "Biotechnological applications in agriculture; Biotechnology and its applications (introduction)",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (e) only", "(b), (d) and (e) only"],
  why="Every option with (e) contradicts the NCERT figure (tripling) given in (b).", secs=70)

Z(BTA, "Human insulin", A, ASR,
  AR("The main challenge in producing human insulin by recombinant DNA techniques was the synthesis of the A and B "
     "polypeptide chains.",
     "In the body, insulin is synthesised as a pro-hormone that needs to be processed before it becomes a fully "
     "mature and functional hormone."),
  "Challenge in producing recombinant insulin",
  "NCERT states that the main challenge for production of insulin using rDNA techniques was getting insulin "
  "ASSEMBLED INTO A MATURE FORM, not making the chains. In the body insulin is synthesised as a pro-hormone (with an "
  "extra stretch, the C peptide) that must be processed to become mature, functional insulin. Eli Lilly side-stepped "
  "this by producing chains A and B separately and joining them by disulphide bonds.",
  ["A: false (the challenge was assembling insulin into its mature form)", "R: true"],
  "Biotechnological applications in medicine (genetically engineered insulin)", ans="D",
  why="A misstates the challenge, so options A, B and C, which need A to be true, are wrong.", secs=50)

Z(BTA, "Bt crops and RNAi", A, STP,
  SP("The choice of Bt toxin genes to be introduced into a crop depends upon the crop and the targeted pest.",
     "Bt toxin genes have been expressed in crop plants such as cotton, corn, rice, tomato, potato and soyabean."),
  "Bt crops",
  "Most Bt toxins are insect-group specific, so the choice of genes depends on the crop and the targeted pest. The "
  "Bt toxin gene has been cloned from the bacterium and expressed in plants to give resistance to insects without "
  "insecticides: examples are Bt cotton, Bt corn, rice, tomato, potato and soyabean.",
  ["Statement I: true", "Statement II: true"],
  "Biotechnological applications in agriculture (Bt cotton)", ans="A",
  why="Both are NCERT statements, so options calling either one false are wrong.", secs=40)

Z(BTA, "Gene therapy", A, MUL,
  MS("Which of the following statements about gene therapy and ADA deficiency are correct?",
     ["In gene therapy, the defective gene must first be removed, because a delivered normal gene cannot compensate "
      "for a non-functional gene.",
      "ADA deficiency is caused by the deletion of the gene for adenosine deaminase.",
      "The enzyme adenosine deaminase is crucial for the immune system to function.",
      "Enzyme replacement therapy is completely curative for ADA deficiency.",
      "In gene therapy for ADA deficiency, lymphocytes from the patient's blood are grown in a culture outside the "
      "body."]),
  "Gene therapy for ADA deficiency",
  "Gene therapy corrects a gene defect by delivering a normal gene into the individual or embryo to TAKE OVER the "
  "function of, and compensate for, the non-functional gene; the defective gene is not removed. ADA deficiency is "
  "caused by deletion of the gene for adenosine deaminase, an enzyme crucial for the immune system. Bone marrow "
  "transplantation and enzyme replacement therapy are not completely curative. In gene therapy, the patient's "
  "lymphocytes are grown in culture outside the body before the functional ADA cDNA is introduced.",
  ["(a) False: the normal gene compensates; nothing is removed", "(b) True", "(c) True",
   "(d) False: not completely curative", "(e) True"],
  "Biotechnological applications in medicine (gene therapy)",
  at="C", correct="(b), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"],
  why="Options with (a) misdescribe how gene therapy works; options with (d) call enzyme replacement completely "
      "curative, which NCERT denies.", secs=65)

Z(BTA, "Biosafety, biopiracy and patents", A, ASR,
  AR("Some nations are developing laws to prevent unauthorised exploitation of their bio-resources and traditional "
     "knowledge.",
     "There is a growing realisation of the injustice, inadequate compensation and benefit sharing between developed "
     "and developing countries."),
  "Biopiracy and national laws",
  "NCERT states that there is a growing realisation of the injustice, inadequate compensation and benefit sharing "
  "between developed and developing countries; therefore, some nations are developing laws to prevent such "
  "unauthorised exploitation of their bio-resources and traditional knowledge.",
  ["A: true", "R: true", "NCERT links them with 'therefore': R is the reason for A"],
  "Ethical issues", ans="A",
  why="NCERT presents R as the cause of A, so B is wrong; both statements are true, so C and D are wrong.", secs=45)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 127
    ids = [x["question_id"] for x in QUESTIONS]
    assert ids[0] == pkg["question_ids"][0] and ids[-1] == pkg["question_ids"][1] and len(set(ids)) == len(ids)
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    assert all(x["subtopic"] in subtopics[x["topic"]] for x in QUESTIONS)
    assert all(x["solution"]["ncert_reference"] and x["solution"]["why_others_wrong"] for x in QUESTIONS)
    stems = [x["question_text"] for x in QUESTIONS]
    assert len(set(stems)) == len(stems), "duplicate stem"
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert max(keys.values()) - min(keys.values()) <= 3, keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    for f in (D, ASR, STP, MAT, MUL):
        assert fmts[f] >= 0.08 * len(QUESTIONS), (f, fmts)
    assert 0.03 * len(QUESTIONS) <= fmts[NUM] <= 0.08 * len(QUESTIONS), fmts
    assert all("script:recompute" in x["verification"]["verified_by"] for x in QUESTIONS if x["format"] == NUM)
    assert all("script:recompute" not in x["verification"]["verified_by"] for x in QUESTIONS if x["format"] != NUM)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "ZOO_002_p2: 127 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers re-derived in tools/batch_002/ZOO_002_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
    print("keys", dict(sorted(keys.items())))
    print("formats", dict(fmts))
