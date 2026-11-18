"""Builder for package ZOO_010_p2 of BATCH_010 (Zoology, 119 questions, NEET_ZOO_002382..NEET_ZOO_002500).

Topics: Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_010/ZOO_010_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_010_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_010_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_010_ZOO_p2.json"
FIRST_ID = 2382

CHECKED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

HR = "Human Reproduction"
RH = "Reproductive Health"
EVO = "Evolution"
HHD = "Human Health and Disease"
BPP = "Biotechnology: Principles and Processes"
BTA = "Biotechnology and its Applications"

REF = {
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




# ================================================================ Human Reproduction (7/9/7)
Z(HR, "Male and female reproductive systems", B, D,
  "Which of the following is NOT a part of the external genitalia of the human female?",
  "Female external genitalia",
  "NCERT: the female external genitalia include the mons pubis, labia majora, labia minora, hymen and clitoris. "
  "The cervix is part of the uterus: the uterus opens into the vagina through a narrow cervix, so it is an internal "
  "structure and not part of the external genitalia.",
  ["External genitalia = mons pubis, labia majora, labia minora, hymen, clitoris",
   "Cervix = narrow lower part of the uterus opening into the vagina (internal)"],
  "The Female Reproductive System",
  at="C", correct="Cervix",
  wrong=["Mons pubis", "Labia minora", "Clitoris"],
  why="The mons pubis (cushion of fatty tissue), the labia minora (paired folds under the labia majora) and the "
      "clitoris (tiny finger-like structure above the urethral opening) are all listed by NCERT among the female "
      "external genitalia.", secs=25)

Z(HR, "Gametogenesis", B, D,
  "In a human sperm, which part lies between the head and the middle piece?",
  "Parts of a human sperm",
  "NCERT: the sperm is a microscopic structure composed of a head, a neck, a middle piece and a tail. The neck "
  "joins the head to the middle piece; the middle piece carries numerous mitochondria and is followed by the tail.",
  ["Order of parts: head -> neck -> middle piece -> tail", "Between head and middle piece: neck"],
  "Gametogenesis",
  at="A", correct="Neck",
  wrong=["Acrosome", "Tail", "Nucleus"],
  why="The acrosome is the cap-like structure covering the anterior part of the head; the nucleus lies inside the "
      "head; the tail is the last part, behind the middle piece.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "According to NCERT, the secretions of certain male accessory ducts and glands are essential for the maturation "
  "and motility of sperms. Which of the following is NOT one of them?",
  "Secretions needed for sperm maturation and motility",
  "NCERT: the secretions of the epididymis, vas deferens, seminal vesicle and prostate are essential for the "
  "maturation and motility of sperms. The bulbourethral glands are not in this list; their secretions help in the "
  "lubrication of the penis.",
  ["Listed: epididymis, vas deferens, seminal vesicle, prostate", "Bulbourethral glands: lubrication of the penis"],
  "Gametogenesis",
  at="D", correct="Bulbourethral glands",
  wrong=["Epididymis", "Seminal vesicle", "Prostate"],
  why="The epididymis, the seminal vesicle and the prostate are each named by NCERT among the structures whose "
      "secretions are essential for sperm maturation and motility.", secs=30)

Z(HR, "Male and female reproductive systems", B, ASR,
  AR("The ovaries are the primary female sex organs.",
     "The ovaries produce the female gamete (ovum) and several steroid hormones (ovarian hormones)."),
  "Primary sex organs",
  "NCERT: ovaries are the primary female sex organs that produce the female gamete (ovum) and several steroid "
  "hormones. Primary sex organs (gonads) are the organs that produce the gametes and sex hormones, so the fact "
  "stated in R is exactly why the ovaries are called the primary female sex organs.",
  ["A: true", "R: true - the ovaries form the gamete and the ovarian hormones", "R explains A"],
  "The Female Reproductive System", ans="A",
  why="Both statements are NCERT's own; R gives the very function (gamete and hormone production) that makes the "
      "ovaries the primary sex organs, so 'R is not the explanation' is wrong, and neither statement is false.",
  secs=30)

Z(HR, "Male and female reproductive systems", B, STP,
  SP("The enlarged end of the penis, called the glans penis, is covered by a loose fold of skin called the foreskin.",
     "The seminal vesicles are paired, whereas the prostate is a single gland."),
  "Penis and male accessory glands",
  "NCERT: the enlarged end of the penis called the glans penis is covered by a loose fold of skin called foreskin. "
  "The male accessory glands include paired seminal vesicles, a prostate and paired bulbourethral glands. Both "
  "statements are true.",
  ["Statement I: true", "Statement II: true - paired seminal vesicles, a (single) prostate"],
  "The Male Reproductive System", ans="A",
  why="Statement I is NCERT's description of the glans penis; Statement II matches NCERT's list of accessory glands "
      "(paired seminal vesicles, a prostate, paired bulbourethral glands), so no option with a false statement is "
      "correct.", secs=30)

Z(HR, "Gametogenesis", B, D,
  "In the seminiferous tubules of the human testis, some of the spermatogonia periodically undergo meiosis. These "
  "cells are called:",
  "Primary spermatocytes",
  "NCERT: spermatogonia multiply by mitotic division. Some of the spermatogonia, called primary spermatocytes, "
  "periodically undergo meiosis. A primary spermatocyte completes the first meiotic division (reduction division) "
  "leading to the formation of two equal, haploid cells called secondary spermatocytes.",
  ["Spermatogonia that enter meiosis = primary spermatocytes", "Meiosis I product = secondary spermatocytes"],
  "Gametogenesis",
  at="B", correct="Primary spermatocytes",
  wrong=["Spermatids", "Sertoli cells", "Secondary spermatocytes"],
  why="Spermatids are formed after the second meiotic division and do not divide again; Sertoli cells are "
      "nourishing cells, not germ cells; secondary spermatocytes are the products of the first meiotic division.",
  secs=25)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "The glandular tissue of each human breast is divided into mammary lobes containing clusters of cells called "
  "alveoli. According to NCERT, the number of mammary lobes in each breast is:",
  "Mammary lobes",
  "NCERT: the glandular tissue of each breast is divided into 15-20 mammary lobes containing clusters of cells "
  "called alveoli. The cells of the alveoli secrete milk, which is stored in the cavities (lumens) of the alveoli.",
  ["Mammary lobes per breast = 15-20"],
  "The Female Reproductive System",
  at="D", correct="15-20",
  wrong=["About 250", "2-3", "60-80"],
  why="About 250 is the number of testicular lobules in each testis; 2-3 and 60-80 are not NCERT figures for the "
      "mammary gland.", secs=20)

Z(HR, "Male and female reproductive systems", I, MUL,
  MS("Which of the following structures of the human female reproductive system are paired?",
     ["Ovaries", "Uterus", "Oviducts (fallopian tubes)", "Mammary glands", "Vagina"]),
  "Paired and single female reproductive structures",
  "NCERT: the female reproductive system consists of a pair of ovaries along with a pair of oviducts, uterus, "
  "cervix, vagina and the external genitalia, together with a pair of mammary glands. The uterus is single (also "
  "called the womb), and there is a single vagina into which the uterus opens through the cervix.",
  ["Paired: ovaries, oviducts, mammary glands", "Single: uterus, vagina"],
  "The Female Reproductive System",
  at="B", correct="(a), (c) and (d) only",
  wrong=["(a) and (c) only", "(a), (b), (c) and (d) only", "(a), (c), (d) and (e) only"],
  why="'(a) and (c) only' leaves out the pair of mammary glands; options containing (b) or (e) are wrong because "
      "the uterus is single and so is the vagina.", secs=40)

Z(HR, "Gametogenesis", I, MAT,
  ML(("hormone", "cells or organ it acts on, as described in NCERT"),
     ["GnRH", "LH (in the male)", "FSH (in the male)", "Oxytocin (at parturition)"],
     ["Sertoli cells", "Uterine muscle", "Anterior pituitary", "Leydig cells"]),
  "Targets of reproductive hormones",
  "NCERT: at puberty the increased GnRH acts at the anterior pituitary and stimulates the secretion of two "
  "gonadotropins, LH and FSH. LH acts at the Leydig cells and stimulates the synthesis and secretion of androgens; "
  "FSH acts on the Sertoli cells and stimulates the secretion of some factors that help in spermiogenesis. At "
  "parturition, oxytocin acts on the uterine muscle and causes stronger uterine contractions.",
  ["A -> III", "B -> IV", "C -> I", "D -> II"],
  "Gametogenesis; Parturition and Lactation",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"}]),
  why="Swapping LH and FSH reverses NCERT's pairing (LH -> Leydig cells, FSH -> Sertoli cells); GnRH acts on the "
      "anterior pituitary, not on the uterus; the last code mismatches every hormone.", secs=50)

Z(HR, "Male and female reproductive systems", I, D,
  "Using the lengths given in NCERT, which option arranges the following human structures in DECREASING order of "
  "length?\n\nOviduct, testis, ovary",
  "Sizes of reproductive organs",
  "NCERT: each oviduct is about 10-12 cm long; each adult testis is about 4 to 5 cm long (2 to 3 cm wide); each "
  "ovary is about 2 to 4 cm in length. So the oviduct is the longest and the ovary the shortest.",
  ["Oviduct 10-12 cm", "Testis 4-5 cm", "Ovary 2-4 cm", "Oviduct > testis > ovary"],
  "The Male Reproductive System; The Female Reproductive System",
  at="A", correct="Oviduct > testis > ovary",
  wrong=["Testis > oviduct > ovary", "Oviduct > ovary > testis", "Ovary > testis > oviduct"],
  why="The testis (4-5 cm) is far shorter than the oviduct (10-12 cm); the ovary (2-4 cm) is not longer than the "
      "testis; the last option reverses the true order.", secs=40)

Z(HR, "Gametogenesis", I, STP,
  SP("A spermatid has the same number of chromosomes as the secondary spermatocyte from which it is formed.",
     "During spermiogenesis, the chromosome number of a spermatid is halved to form a spermatozoon."),
  "Chromosome number in the later stages of spermatogenesis",
  "NCERT: secondary spermatocytes have only 23 chromosomes each. They undergo the second meiotic division to "
  "produce four equal, haploid spermatids, which also have 23 chromosomes. Spermatids are then transformed into "
  "spermatozoa (sperms) by spermiogenesis, a transformation without any further reduction, so the sperm remains "
  "haploid with 23 chromosomes.",
  ["Secondary spermatocyte: 23 chromosomes", "Spermatid: 23 chromosomes -> Statement I true",
   "Spermiogenesis does not halve the number -> Statement II false"],
  "Gametogenesis", ans="C",
  why="Statement II is false because the sperm is haploid like the spermatid (23 chromosomes), so 'both true' and "
      "'Statement I false but II true' are wrong; Statement I is true, so 'both false' is wrong.", secs=45)

Z(HR, "Fertilisation and implantation", I, ASR,
  AR("The human sperm and the human ovum contribute equal numbers of chromosomes to the zygote.",
     "Both the sperm and the ovum are haploid, and their haploid nuclei fuse to form a diploid zygote."),
  "Contribution of gametes to the zygote",
  "NCERT: the sperm head contains an elongated haploid nucleus, and the ovum (ootid) formed after the second "
  "meiotic division is haploid. Fusion of the haploid nuclei of the sperm and the ovum forms a diploid zygote. "
  "Since each gamete is haploid (23 chromosomes), each contributes the same number, which is exactly what A says.",
  ["Sperm: haploid (23)", "Ovum: haploid (23)", "Zygote: 23 + 23 = 46 -> R explains A"],
  "Fertilisation and Implantation", ans="A",
  why="Both statements are true, and the haploid nature of both gametes is the direct reason they contribute equal "
      "chromosome numbers; so 'R is not the explanation' and the options calling either statement false are wrong.",
  secs=35)

Z(HR, "Male and female reproductive systems", I, D,
  "How many of the following cells of the human testis are present INSIDE the seminiferous tubules?\n\n"
  "Spermatogonia, Sertoli cells, Leydig cells, primary spermatocytes, spermatids, immunologically competent cells",
  "Inside versus outside the seminiferous tubules",
  "NCERT: each seminiferous tubule is lined on its inside by male germ cells (spermatogonia) and Sertoli cells, "
  "and spermatogenesis (primary spermatocytes -> secondary spermatocytes -> spermatids -> sperms) takes place in "
  "the tubules. The interstitial spaces outside the tubules contain small blood vessels, interstitial (Leydig) "
  "cells and some immunologically competent cells.",
  ["Inside: spermatogonia, Sertoli cells, primary spermatocytes, spermatids = 4",
   "Outside (interstitial spaces): Leydig cells, immunologically competent cells"],
  "The Male Reproductive System; Gametogenesis",
  at="D", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three leaves out one of the cells of the tubule (often the Sertoli cells or the spermatids); five or six add "
      "the Leydig cells and/or the immunologically competent cells, which NCERT places in the interstitial spaces.",
  secs=45)

Z(HR, "Gametogenesis", I, MAT,
  ML(("event", "when it takes place"),
     ["Formation of oogonia (gamete mother cells) in the ovary", "Start of spermatogenesis",
      "Completion of the second meiotic division of the secondary oocyte", "Cessation of menstrual cycles"],
     ["Around 50 years of age", "During embryonic (fetal) development", "At puberty",
      "On entry of a sperm into the oocyte"]),
  "Timing of reproductive events",
  "NCERT: oogenesis is initiated during embryonic development, when a couple of million oogonia are formed within "
  "each fetal ovary; no more oogonia are formed after birth. Spermatogenesis starts at puberty. The entry of the "
  "sperm into the ovum induces completion of the meiotic division of the secondary oocyte. In human beings, "
  "menstrual cycles cease around 50 years of age (menopause).",
  ["A -> II", "B -> III", "C -> IV", "D -> I"],
  "Gametogenesis; Menstrual Cycle; Fertilisation and Implantation",
  at="B", match=({"A": "II", "B": "III", "C": "IV", "D": "I"},
                 [{"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "II", "B": "III", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"}]),
  why="Oogonia are formed before birth while spermatogenesis begins at puberty, so swapping A and B is wrong; the "
      "second meiotic division is completed on sperm entry, not at 50 years; the last code puts oogonia formation at "
      "sperm entry.", secs=50)

Z(HR, "Fertilisation and implantation", I, STP,
  SP("The human embryo with 8 to 16 blastomeres is called a blastocyst.",
     "In the blastocyst, the blastomeres are arranged into an outer layer called the trophoblast and an inner group "
     "of cells attached to it called the inner cell mass."),
  "Morula and blastocyst",
  "NCERT: the embryo with 8 to 16 blastomeres is called a morula. The morula continues to divide and transforms "
  "into a blastocyst, in which the blastomeres are arranged into an outer layer called trophoblast and an inner "
  "group of cells attached to the trophoblast called the inner cell mass.",
  ["Statement I: false - 8-16 blastomeres = morula", "Statement II: true"],
  "Fertilisation and Implantation", ans="D",
  why="Statement I names the wrong stage (it is the morula), so options calling it true are wrong; Statement II is "
      "NCERT's description of the blastocyst, so 'both false' is wrong.", secs=35)

Z(HR, "Male and female reproductive systems", I, ASR,
  AR("In the human male, the sperms released from the seminiferous tubules are transported to the outside by the "
     "accessory ducts.",
     "The secretions of the bulbourethral glands help in the lubrication of the penis."),
  "Accessory ducts and glands",
  "NCERT: the male sex accessory ducts (rete testis, vasa efferentia, epididymis and vas deferens) store and "
  "transport the sperms from the testis to the outside through the urethra; the sperms released from the "
  "seminiferous tubules are transported by these ducts. Separately, NCERT states that the secretions of the "
  "bulbourethral glands help in the lubrication of the penis. Both are true, but lubrication of the penis has "
  "nothing to do with how sperms are carried out of the testis.",
  ["A: true", "R: true", "R describes a different structure and function -> not the explanation"],
  "The Male Reproductive System; Gametogenesis", ans="B",
  why="R concerns lubrication of the penis by a gland, while A concerns sperm transport by ducts, so R cannot "
      "explain A; both statements are NCERT's own, so the options calling either one false are wrong.", secs=35)

Z(HR, "Gametogenesis", A, NUM,
  "In a human male, a group of primary spermatocytes completes spermatogenesis and forms exactly 100 spermatozoa. "
  "In a human female, a group of primary oocytes completes oogenesis and forms exactly 100 ova; assume that every "
  "secondary oocyte is entered by a sperm and completes its second meiotic division, and that the first polar "
  "bodies do not divide. Counting each splitting of one cell into two as one division, how many meiotic divisions "
  "take place in all in the male and in the female, respectively?",
  "Counting meiotic divisions in spermatogenesis and oogenesis",
  "One primary spermatocyte undergoes one first meiotic division (giving two secondary spermatocytes) and then "
  "each secondary spermatocyte undergoes one second meiotic division: 3 divisions give 4 spermatids, i.e. 4 "
  "sperms. One primary oocyte undergoes the unequal first meiotic division (secondary oocyte + first polar body); "
  "only the secondary oocyte undergoes the second meiotic division (ovum + second polar body): 2 divisions give 1 "
  "ovum.",
  ["Male: 100 sperms / 4 = 25 primary spermatocytes", "Male divisions: 25 x (1 + 2) = 75",
   "Female: 100 ova = 100 primary oocytes", "Female divisions: 100 x (1 + 1) = 200"],
  "Gametogenesis",
  at="C", correct="75 and 200",
  wrong=["50 and 100", "100 and 200", "75 and 300"],
  why="'50 and 100' counts only one division per two gametes or per gamete, ignoring a meiotic step; '100 and 200' "
      "counts one division per sperm; '75 and 300' wrongly makes the first polar body divide, which the stem "
      "excludes.", secs=120, vb=RECOMPUTED)

Z(HR, "Pregnancy, parturition and lactation", A, D,
  "Which option arranges the following events of human foetal development in the correct order, from EARLIEST to "
  "LATEST, according to NCERT?\n\n(P) Eye-lids separate and eyelashes are formed\n(Q) The heart is formed\n"
  "(R) First movements of the foetus are usually observed\n(S) Most of the major organ systems are formed, with "
  "the limbs and external genital organs well developed\n(T) The foetus develops limbs and digits",
  "Timeline of foetal development",
  "NCERT: after one month of pregnancy the embryo's heart is formed (Q). By the end of the second month the foetus "
  "develops limbs and digits (T). By the end of 12 weeks (first trimester), most major organ systems are formed, "
  "the limbs and external genital organs being well developed (S). The first movements of the foetus and "
  "appearance of hair on the head are usually observed during the fifth month (R). By the end of about 24 weeks, "
  "the body is covered with fine hair, eye-lids separate and eyelashes are formed (P).",
  ["Q: 1 month", "T: end of month 2", "S: end of 12 weeks", "R: fifth month", "P: end of 24 weeks",
   "Order: Q -> T -> S -> R -> P"],
  "Pregnancy and Embryonic Development",
  at="D", correct="Q -> T -> S -> R -> P",
  wrong=["Q -> S -> T -> R -> P", "T -> Q -> S -> P -> R", "Q -> T -> R -> S -> P"],
  why="Limbs and digits (end of month 2) come before the first trimester ends (12 weeks), so S cannot precede T; "
      "the heart forms before the limbs; first movements (fifth month) come after 12 weeks and before 24 weeks, so R "
      "can neither precede S nor follow P.", secs=60)

Z(HR, "Fertilisation and implantation", A, D,
  "How many of the following normally take place in the human UTERUS?\n\n"
  "Fertilisation; implantation; start of cleavage of the zygote; formation of the placenta; completion of the "
  "second meiotic division of the secondary oocyte; breakdown of the endometrial lining in the menstrual phase",
  "Sites of reproductive events",
  "NCERT: fertilisation takes place in the ampullary region of the oviduct, and the second meiotic division of the "
  "secondary oocyte is completed there when the sperm enters it. Cleavage starts as the zygote moves through the "
  "isthmus of the oviduct towards the uterus. The blastocyst becomes embedded in the endometrium of the uterus "
  "(implantation); the chorionic villi and uterine tissue jointly form the placenta; in the menstrual phase the "
  "endometrial lining of the uterus breaks down.",
  ["In the uterus: implantation, placenta formation, endometrial breakdown = 3",
   "In the oviduct: fertilisation, completion of meiosis II, start of cleavage"],
  "Fertilisation and Implantation; Pregnancy and Embryonic Development; Menstrual Cycle",
  at="B", correct="Three",
  wrong=["Two", "Four", "Five"],
  why="Two omits either placenta formation or menstrual breakdown; four or five add events that NCERT places in the "
      "oviduct (fertilisation, completion of meiosis II, start of cleavage).", secs=60)

Z(HR, "Gametogenesis", A, ASR,
  AR("The first polar body and the secondary oocyte formed from a human primary oocyte have the same number of "
     "chromosomes.",
     "The first meiotic division of the primary oocyte divides its cytoplasm equally between the two cells "
     "formed."),
  "Unequal first meiotic division of the oocyte",
  "NCERT: the primary oocyte completes its first meiotic division, an unequal division, resulting in a large "
  "haploid secondary oocyte and a tiny first polar body; the secondary oocyte retains the bulk of the "
  "nutrient-rich cytoplasm. Both cells are haploid (23 chromosomes each), so A is true; the cytoplasm is divided "
  "unequally, so R is false.",
  ["Both cells haploid -> same chromosome number -> A true", "Cytoplasm divided unequally -> R false"],
  "Gametogenesis", ans="C",
  why="The division is unequal in cytoplasm but equal in chromosomes; so R is false and the two 'both true' options "
      "fail, and A is true so 'A is false but R is true' fails.", secs=45)

Z(HR, "Menstrual cycle", A, STP,
  SP("In a menstrual cycle, the LH surge takes place before the corpus luteum is formed.",
     "Progesterone secreted by the corpus luteum causes the rupture of the Graafian follicle at ovulation."),
  "Sequence of hormonal events around ovulation",
  "NCERT: the rapid secretion of LH reaching a maximum in the middle of the cycle (LH surge) induces rupture of the "
  "Graafian follicle and thereby the release of the ovum (ovulation). The ovulatory phase is followed by the luteal "
  "phase, during which the remaining parts of the Graafian follicle transform into the corpus luteum, which then "
  "secretes large amounts of progesterone. So the LH surge comes before the corpus luteum (I true), and ovulation is "
  "caused by the LH surge, not by progesterone, which comes only from the corpus luteum formed after ovulation "
  "(II false).",
  ["LH surge -> ovulation -> corpus luteum -> progesterone", "Statement I true", "Statement II false"],
  "Menstrual Cycle", ans="C",
  why="Statement II reverses cause and sequence: the corpus luteum (the source of progesterone) forms only after "
      "the follicle has ruptured, so options calling it true fail; Statement I is true, so 'both false' and "
      "'Statement I false' fail.", secs=50)

Z(HR, "Gametogenesis", A, MAT,
  ML(("cell", "description"),
     ["Spermatogonium", "Secondary spermatocyte", "Primary oocyte in the fetal ovary", "First polar body"],
     ["Haploid; tiny cell formed by an unequal meiotic division",
      "Diploid; temporarily arrested in prophase-I of meiosis",
      "Diploid; increases in number by mitotic division",
      "Haploid; undergoes the second meiotic division to form two equal cells"]),
  "Ploidy and fate of gametogenic cells",
  "NCERT: spermatogonia are diploid (46 chromosomes) and multiply by mitotic division. A primary spermatocyte "
  "completes the first meiotic division to form two equal haploid secondary spermatocytes, which undergo the second "
  "meiotic division to produce four equal haploid spermatids. In the fetal ovary, the oogonia enter prophase-I of "
  "meiosis and get temporarily arrested as (diploid) primary oocytes. The primary oocyte's unequal first meiotic "
  "division forms a large secondary oocyte and a tiny first polar body.",
  ["A -> III", "B -> IV", "C -> II", "D -> I"],
  "Gametogenesis",
  at="A", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="It is the primary oocyte, not the spermatogonium, that is arrested in prophase-I; the secondary spermatocyte "
      "divides into two equal cells, whereas the first polar body is the tiny product of an unequal division; the "
      "last code makes the diploid spermatogonium haploid.", secs=60)

Z(HR, "Fertilisation and implantation", A, MUL,
  MS("Which of the following are induced by a sperm when it contacts or enters the human secondary oocyte during "
     "fertilisation?",
     ["Changes in the membrane of the ovum that block the entry of additional sperms",
      "Completion of the meiotic division of the secondary oocyte",
      "Completion of the first meiotic division of the primary oocyte",
      "Formation of the second polar body",
      "Rupture of the Graafian follicle"]),
  "Events triggered by the sperm",
  "NCERT: during fertilisation a sperm comes in contact with the zona pellucida layer of the ovum and induces "
  "changes in the membrane that block the entry of additional sperms. The entry of the sperm into the ovum induces "
  "completion of the meiotic division of the secondary oocyte; this second meiotic division is unequal and forms "
  "the second polar body and a haploid ovum. The first meiotic division is completed in the tertiary follicle "
  "before ovulation, and the Graafian follicle ruptures under the LH surge.",
  ["(a) induced by sperm contact", "(b), (d) induced by sperm entry",
   "(c) before ovulation; (e) LH surge -> not induced by the sperm"],
  "Fertilisation and Implantation; Gametogenesis",
  at="D", correct="(a), (b) and (d) only",
  wrong=["(b) and (d) only", "(a), (b), (c) and (d) only", "(a), (d) and (e) only"],
  why="'(b) and (d) only' omits the block to additional sperms, which NCERT says the sperm's contact induces; (c) "
      "occurs before ovulation and (e) is caused by the LH surge, so options containing them are wrong.", secs=60)


# ================================================================ Reproductive Health (5/6/5)
Z(RH, "MTP and amniocentesis", B, D,
  "According to NCERT, the Government of India legalised medical termination of pregnancy (MTP), with some strict "
  "conditions to avoid its misuse, in the year:",
  "Legalisation of MTP in India",
  "NCERT: the Government of India legalised MTP in 1971 with some strict conditions to avoid its misuse. Such "
  "restrictions are all the more important to check indiscriminate and illegal female foeticides.",
  ["MTP legalised in India: 1971"],
  "Medical Termination of Pregnancy (MTP)",
  at="A", correct="1971",
  wrong=["1951", "1991", "2011"],
  why="1951 is the year in which the 'family planning' programmes were initiated in India; 1991 and 2011 are not "
      "the year NCERT gives for legalising MTP.", secs=20)

Z(RH, "Contraception", B, D,
  "Which of the following groups consists ONLY of barrier methods of contraception?",
  "Barrier methods",
  "NCERT: in barrier methods, ovum and sperms are prevented from physically meeting with the help of barriers. "
  "Such methods are available for both males and females: condoms, and diaphragms, cervical caps and vaults made "
  "of rubber that are inserted into the female reproductive tract to cover the cervix during coitus.",
  ["Barriers: condoms, diaphragms, cervical caps, vaults",
   "Not barriers: IUDs (CuT, Lippes loop), pills (Saheli), natural methods, surgical methods"],
  "Population Stabilisation and Birth Control",
  at="B", correct="Condoms, diaphragms, cervical caps and vaults",
  wrong=["Condoms, diaphragms, Lippes loop and vaults", "Cervical caps, vaults, Saheli and condoms",
         "Diaphragms, CuT, cervical caps and coitus interruptus"],
  why="Lippes loop and CuT are intra-uterine devices, Saheli is an oral pill, and coitus interruptus is a natural "
      "method, so every other group contains a non-barrier method.", secs=30)

Z(RH, "Contraception", B, ASR,
  AR("IUDs are ideal contraceptives for females who want to delay pregnancy and/or space children.",
     "IUDs are inserted by doctors or expert nurses in the uterus through the vagina."),
  "IUDs: suitability and insertion",
  "NCERT: IUDs are inserted by doctors or expert nurses in the uterus through the vagina. IUDs are ideal "
  "contraceptives for the females who want to delay pregnancy and/or space children; it is one of the most widely "
  "accepted methods of contraception in India. Both statements are true, but who inserts the device and by what "
  "route does not explain why it is suited for delaying or spacing pregnancies.",
  ["A: true", "R: true", "R describes the insertion procedure, not the reason for suitability -> not the explanation"],
  "Population Stabilisation and Birth Control", ans="B",
  why="R gives a procedural detail unrelated to the purpose described in A, so 'R is the correct explanation' is "
      "wrong; both statements are NCERT's own, so the options calling either false are wrong.", secs=30)

Z(RH, "Contraception", B, STP,
  SP("Surgical methods of contraception are highly effective.",
     "In the lactational amenorrhea method, no medicines or devices are used, and its chances of failure are "
     "almost nil."),
  "Effectiveness of surgical and natural methods",
  "NCERT: sterilisation techniques (vasectomy, tubectomy) are highly effective, but their reversibility is very "
  "poor. Lactational amenorrhea is a natural method; for such methods NCERT says that as no medicines or devices "
  "are used, side effects are almost nil, but the chances of failure are also high. So it is the side effects, not "
  "the chances of failure, that are almost nil.",
  ["Statement I: true", "Statement II: false - side effects almost nil, chances of failure high"],
  "Population Stabilisation and Birth Control", ans="C",
  why="Statement II confuses side effects with failure; natural methods have high chances of failure, so options "
      "calling it true are wrong. Statement I is NCERT's own statement, so 'both false' and 'Statement I false' are "
      "wrong.", secs=30)

Z(RH, "Contraception", B, D,
  "LNG-20 is an example of a:",
  "Types of intra-uterine devices",
  "NCERT classifies IUDs as non-medicated IUDs (e.g. Lippes loop), copper-releasing IUDs (CuT, Cu7, Multiload 375) "
  "and hormone-releasing IUDs (Progestasert, LNG-20).",
  ["Hormone-releasing IUDs: Progestasert, LNG-20"],
  "Population Stabilisation and Birth Control",
  at="D", correct="Hormone-releasing IUD",
  wrong=["Copper-releasing IUD", "Non-medicated IUD", "Barrier device that covers the cervix"],
  why="Copper-releasing IUDs are CuT, Cu7 and Multiload 375; the non-medicated IUD named by NCERT is Lippes loop; "
      "the barriers covering the cervix are diaphragms, cervical caps and vaults.", secs=20)

Z(RH, "Contraception", I, D,
  "How many of the following are intra-uterine devices (IUDs)?\n\n"
  "Lippes loop, CuT, Saheli, LNG-20, Multiload 375, vault, Progestasert",
  "Identifying IUDs",
  "NCERT's IUDs: non-medicated (Lippes loop), copper-releasing (CuT, Cu7, Multiload 375) and hormone-releasing "
  "(Progestasert, LNG-20). Saheli is an oral contraceptive pill, and the vault is a rubber barrier that covers the "
  "cervix.",
  ["IUDs: Lippes loop, CuT, LNG-20, Multiload 375, Progestasert = 5", "Not IUDs: Saheli (pill), vault (barrier)"],
  "Population Stabilisation and Birth Control",
  at="C", correct="Five",
  wrong=["Three", "Four", "Six"],
  why="Three or four leave out one or more of NCERT's IUDs (often the hormone-releasing ones); six counts the vault "
      "or Saheli, which are a barrier and a pill.", secs=40)

Z(RH, "Contraception", I, ASR,
  AR("Progestogens, progestogen-estrogen combinations or IUDs can be used to avoid a possible pregnancy following "
     "rape or casual unprotected intercourse.",
     "Such emergency contraceptives are very effective only if used within 24 hours of coitus."),
  "Emergency contraception",
  "NCERT: administration of progestogens or progestogen-estrogen combinations or IUDs within 72 hours of coitus "
  "has been found to be very effective as emergency contraceptives, as they could be used to avoid possible "
  "pregnancy due to rape or casual unprotected intercourse. A is true; R gives the wrong time limit (24 hours "
  "instead of 72 hours), so R is false.",
  ["A: true", "R: false - NCERT's window is 72 hours"],
  "Population Stabilisation and Birth Control", ans="C",
  why="R changes NCERT's 72-hour window to 24 hours, so options with R true are wrong; A is NCERT's own statement, "
      "so 'A is false' is wrong.", secs=35)

Z(RH, "Contraception", I, MUL,
  MS("According to NCERT, educating people, especially fertile couples and those in the marriageable age group, "
     "about which of the following would help in bringing up socially conscious healthy families of desired size?",
     ["Available birth control options", "Care of pregnant mothers and post-natal care of the mother and child",
      "Importance of breast feeding", "Equal opportunities for the male and the female child",
      "Methods of finding out the sex of the foetus"]),
  "Reproductive health strategies: education of couples",
  "NCERT: educating people, especially fertile couples and those in the marriageable age group, about available "
  "birth control options, care of pregnant mothers, post-natal care of the mother and child, importance of breast "
  "feeding, equal opportunities for the male and the female child, etc., would address the importance of bringing "
  "up socially conscious healthy families of desired size. Foetal sex determination is not among these; NCERT "
  "describes a statutory ban on amniocentesis for sex determination.",
  ["(a)-(d): listed by NCERT", "(e): not listed - sex determination of the foetus is banned"],
  "Reproductive Health - Problems and Strategies",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(a) and (b) only", "(a), (b), (c), (d) and (e)"],
  why="The shorter options leave out equal opportunities for the male and female child and/or the importance of "
      "breast feeding, both named by NCERT; the option with (e) includes foetal sex determination, which is "
      "legally banned and not part of this education.", secs=50)

Z(RH, "STDs and their prevention", I, MAT,
  ML(("strategy for reproductive health described in NCERT", "what it is meant to achieve"),
     ["Proper information about reproductive organs, adolescence and related changes, safe and hygienic sexual "
      "practices, STIs and AIDS",
      "Awareness of problems due to uncontrolled population growth and of social evils like sex-abuse and "
      "sex-related crimes",
      "Strong infrastructural facilities, professional expertise and material support",
      "Implementation of better techniques and new strategies from time to time"],
     ["To provide more efficient care and assistance to people",
      "To help people, especially those in the adolescent age group, lead a reproductively healthy life",
      "To provide medical assistance and care in problems like pregnancy, delivery, STDs, abortions, contraception, "
      "menstrual problems and infertility",
      "To enable people to take steps to prevent them and build a socially responsible and healthy society"]),
  "Strategies to attain reproductive health",
  "NCERT (Reproductive Health - Problems and Strategies): proper information about reproductive organs, adolescence "
  "and related changes, safe and hygienic sexual practices, STIs, AIDS, etc., would help people, especially those in "
  "the adolescent age group, to lead a reproductively healthy life. Awareness of problems due to uncontrolled "
  "population growth and social evils like sex-abuse and sex-related crimes needs to be created to enable people to "
  "take up necessary steps to prevent them and build a socially responsible and healthy society. Strong "
  "infrastructural facilities, professional expertise and material support are essential to provide medical "
  "assistance and care in reproduction-related problems like pregnancy, delivery, STDs, abortions, contraception, "
  "menstrual problems and infertility. Better techniques and new strategies from time to time are required to "
  "provide more efficient care and assistance.",
  ["A -> II", "B -> IV", "C -> III", "D -> I"],
  "Reproductive Health - Problems and Strategies",
  at="A", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"}]),
  why="Information on reproductive organs and safe practices is aimed at adolescents, while awareness of population "
      "growth and sex-related crimes is aimed at building a responsible society, so swapping A and B is wrong; "
      "infrastructure and expertise provide medical care, whereas new techniques make care more efficient, so swapping "
      "C and D is wrong; the last code mismatches every row.", secs=50)

Z(RH, "MTP and amniocentesis", I, STP,
  SP("According to NCERT, a society whose people have physically and functionally normal reproductive organs can be "
     "called reproductively healthy, even if emotional and behavioural interactions in sex-related aspects are not "
     "normal.",
     "Creating awareness among people about various reproduction-related aspects and providing facilities and "
     "support for building up a reproductively healthy society are the major tasks under the Reproductive and Child "
     "Health Care (RCH) programmes."),
  "Meaning of a reproductively healthy society",
  "NCERT: a society with people having physically and functionally normal reproductive organs AND normal emotional "
  "and behavioural interactions among them in all sex-related aspects might be called reproductively healthy; "
  "reproductive health means total well-being in all aspects of reproduction, i.e. physical, emotional, "
  "behavioural and social. Creating awareness about reproduction-related aspects and providing facilities and "
  "support for building up a reproductively healthy society are the major tasks under the RCH programmes.",
  ["Statement I: false - emotional and behavioural interactions must also be normal", "Statement II: true"],
  "Reproductive Health - Problems and Strategies", ans="D",
  why="Statement I drops the emotional and behavioural part of NCERT's description, so options calling it true are "
      "wrong; Statement II is NCERT's own description of the RCH programmes, so 'both false' is wrong.", secs=40)

Z(RH, "Contraception", I, D,
  "Which of the following correctly distinguishes vasectomy from tubectomy?",
  "Vasectomy versus tubectomy",
  "NCERT: in vasectomy, a small part of the vas deferens is removed or tied up through a small incision on the "
  "scrotum, whereas in tubectomy, a small part of the fallopian tube is removed or tied up through a small incision "
  "in the abdomen or through the vagina. Both are sterilisation (terminal) methods that block gamete transport; "
  "their reversibility is very poor.",
  ["Vasectomy: vas deferens, incision on the scrotum", "Tubectomy: fallopian tube, incision in the abdomen or via the vagina"],
  "Population Stabilisation and Birth Control",
  at="B",
  correct="In vasectomy the vas deferens is cut or tied through an incision on the scrotum; in tubectomy the fallopian "
          "tube is cut or tied through an incision in the abdomen or through the vagina",
  wrong=["In vasectomy the vas deferens is cut or tied through an incision in the abdomen; in tubectomy the fallopian "
         "tube is cut or tied through an incision on the scrotum",
         "Vasectomy is easily reversible, whereas tubectomy is a terminal method",
         "Vasectomy stops the production of sperms, whereas tubectomy stops ovulation"],
  why="The first wrong option swaps the incision sites (the scrotum belongs to the male); both methods have very "
      "poor reversibility; neither stops gamete formation, they only block gamete transport.", secs=40)

Z(RH, "Contraception", A, MAT,
  ML(("contraceptive method", "step of reproduction it prevents"),
     ["Coitus interruptus", "Lactational amenorrhea", "Vasectomy", "Condom"],
     ["Ovulation", "Transport of sperms from the testes through the vas deferens",
      "Ejaculated semen entering the female reproductive tract, by a thin rubber/latex sheath",
      "Deposition of semen in the vagina, by withdrawal of the penis just before ejaculation"]),
  "How different contraceptives act",
  "NCERT: in coitus interruptus the male partner withdraws his penis from the vagina just before ejaculation so as "
  "to avoid insemination. Lactational amenorrhea is based on the fact that ovulation and therefore the cycle do not "
  "occur during the period of intense lactation. In vasectomy a small part of the vas deferens is removed or tied "
  "up, blocking sperm transport. Condoms are barriers made of thin rubber/latex sheath that prevent the ejaculated "
  "semen from entering the female reproductive tract.",
  ["A -> IV", "B -> I", "C -> II", "D -> III"],
  "Population Stabilisation and Birth Control",
  at="D", match=({"A": "IV", "B": "I", "C": "II", "D": "III"},
                 [{"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Coitus interruptus uses no sheath (it is withdrawal), so swapping A and D is wrong; lactational amenorrhea "
      "acts on ovulation, not on the vas deferens; the last code mismatches every method.", secs=55)

Z(RH, "Contraception", A, D,
  "Two intra-uterine devices are named below as a pair (first; second). The FIRST is an IUD that releases no "
  "substance and acts only by increasing the phagocytosis of sperms within the uterus; the SECOND, in addition, "
  "releases ions that suppress sperm motility and the fertilising capacity of sperms. Which pair fits this "
  "description?",
  "Non-medicated versus copper-releasing IUDs",
  "NCERT: IUDs increase phagocytosis of sperms within the uterus, and the Cu ions released from copper-releasing "
  "IUDs suppress sperm motility and the fertilising capacity of sperms. Lippes loop is a non-medicated IUD; CuT, "
  "Cu7 and Multiload 375 are copper-releasing IUDs; Progestasert and LNG-20 are hormone-releasing IUDs.",
  ["First: non-medicated -> Lippes loop", "Second: copper-releasing -> Multiload 375"],
  "Population Stabilisation and Birth Control",
  at="A", correct="Lippes loop; Multiload 375",
  wrong=["Multiload 375; Lippes loop", "Progestasert; CuT", "Lippes loop; Progestasert"],
  why="Reversing the pair makes the copper IUD the one that releases nothing; Progestasert releases a hormone, so it "
      "cannot be the IUD that releases no substance, nor the one that releases copper ions.", secs=50)

Z(RH, "Contraception", A, MUL,
  MS("Which of the following contraceptive methods act, at least in part, at the level of the CERVIX, according to "
     "NCERT's description of how they work?",
     ["Cervical cap", "Diaphragm", "Hormone-releasing IUD", "Oral contraceptive pills", "Vasectomy"]),
  "Contraceptives acting at the cervix",
  "NCERT: diaphragms, cervical caps and vaults are inserted into the female reproductive tract to cover the cervix "
  "during coitus. Hormone-releasing IUDs make the uterus unsuitable for implantation and the cervix hostile to the "
  "sperms. Oral pills inhibit ovulation and implantation and also alter the quality of cervical mucus to prevent "
  "or retard the entry of sperms. Vasectomy acts on the vas deferens of the male.",
  ["(a), (b): cover the cervix", "(c): cervix hostile to sperms", "(d): alter cervical mucus",
   "(e): acts on the vas deferens"],
  "Population Stabilisation and Birth Control",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a) and (b) only", "(a), (b) and (c) only", "(a), (b), (d) and (e) only"],
  why="Stopping at the barriers misses the hormonal IUD (hostile cervix) and/or the pills (cervical mucus); vasectomy "
      "acts in the male duct system, so any option with (e) is wrong.", secs=60)

Z(RH, "Infertility and ART", A, STP,
  SP("Among the assisted reproductive technologies described in NCERT, GIFT is the one in which an ovum, rather "
     "than a zygote or an embryo, is transferred into the female.",
     "In artificial insemination, including intra-uterine insemination (IUI), fertilisation takes place inside the "
     "body of the female."),
  "What is transferred in different ARTs",
  "NCERT: in ZIFT the zygote or early embryo (up to 8 blastomeres) is transferred into the fallopian tube, and in "
  "IUT embryos with more than 8 blastomeres are transferred into the uterus. In GIFT an ovum collected from a donor "
  "is transferred into the fallopian tube of a female who cannot produce one but can provide a suitable "
  "environment for fertilisation. ICSI forms an embryo in the laboratory. In artificial insemination, semen is "
  "introduced into the vagina or into the uterus (IUI), so the gametes fuse within the female body.",
  ["GIFT: ovum transferred; ZIFT: zygote; IUT: embryo -> Statement I true",
   "AI/IUI: semen introduced, fertilisation in vivo -> Statement II true"],
  "Infertility", ans="A",
  why="Both statements follow from NCERT's descriptions of the techniques, so every option with a false statement "
      "is wrong.", secs=55)

Z(RH, "STDs and their prevention", A, D,
  "How many of the following does NCERT name as sexually transmitted infections (STIs)?\n\n"
  "Gonorrhoea, syphilis, typhoid, genital herpes, chlamydiasis, genital warts, filariasis, trichomoniasis, "
  "hepatitis-B, HIV infection",
  "STIs named in NCERT",
  "NCERT: diseases or infections transmitted through sexual intercourse are called STIs; gonorrhoea, syphilis, "
  "genital herpes, chlamydiasis, genital warts, trichomoniasis, hepatitis-B and HIV (leading to AIDS) are some of "
  "the common STIs. Typhoid (spread through contaminated food and water) and filariasis (spread by the bite of the "
  "female mosquito vector) are not STIs.",
  ["STIs: gonorrhoea, syphilis, genital herpes, chlamydiasis, genital warts, trichomoniasis, hepatitis-B, HIV = 8",
   "Not STIs: typhoid, filariasis"],
  "Sexually Transmitted Infections (STIs)",
  at="C", correct="Eight",
  wrong=["Six", "Seven", "Ten"],
  why="Six or seven omit NCERT STIs such as hepatitis-B or HIV (which also spread in other ways); ten counts typhoid "
      "and filariasis, which are not sexually transmitted.", secs=45)


# ================================================================ Evolution (6/8/6)
# recomputed keys: homozygotes = heterozygotes; p^2 - q^2 = 0.20; maximum of 2pq; HR meiotic divisions
_q = F(1, 2)
assert (1 - _q) ** 2 + _q ** 2 == 2 * (1 - _q) * _q and _q == F(1, 2)
assert all(((1 - F(k, 100)) ** 2 + F(k, 100) ** 2 == 2 * (1 - F(k, 100)) * F(k, 100)) == (k == 50) for k in range(101))
_p = (1 + F(1, 5)) / 2
assert _p == F(3, 5) and _p ** 2 - (1 - _p) ** 2 == F(1, 5) and 2 * _p * (1 - _p) == F(12, 25)
assert max(2 * F(k, 1000) * (1 - F(k, 1000)) for k in range(1001)) == F(1, 2)
assert (100 // 4) * (1 + 2) == 75 and 100 * (1 + 1) == 200
Z(EVO, "Evidences of evolution", B, D,
  "Fossils found in different-aged rock sediments are used as evidence for evolution. Which method does NCERT "
  "refer to for calculating the ages of fossils?",
  "Dating of fossils",
  "NCERT: fossils are remains of hard parts of life-forms found in rocks, and different-aged rock sediments contain "
  "fossils of different life-forms. While discussing palaeontological evidence, NCERT asks the reader to recall how "
  "the ages of fossils are calculated, i.e. the method of radioactive dating and the principles behind it.",
  ["Age of fossils -> radioactive dating"],
  "What are the Evidences for Evolution?",
  at="C", correct="Radioactive dating",
  wrong=["Comparing the similarities in proteins and genes", "Counting the number of sediment layers above them",
         "Measuring the size of the fossil"],
  why="Protein and gene similarities are biochemical evidence of common ancestry, not a way to date fossils; NCERT "
      "does not describe counting layers or measuring size as methods for calculating the age of fossils.", secs=25)

Z(EVO, "Origin of life", B, D,
  "S.L. Miller, an American scientist, created conditions similar to those of the early earth on a laboratory scale "
  "and observed the formation of amino acids. According to NCERT, he did this experiment in:",
  "Miller's experiment",
  "NCERT: in 1953, S.L. Miller, an American scientist, created electric discharge in a closed flask containing CH4, "
  "H2, NH3 and water vapour and observed the formation of amino acids.",
  ["Miller's experiment: 1953"],
  "Origin of Life",
  at="A", correct="1953",
  wrong=["1938", "1891", "1920"],
  why="1938 is the year a coelacanth was caught in South Africa; 1891 is when Homo erectus fossils were found in "
      "Java; 1920 is the year of the post-industrial moth collection in England.", secs=20)

Z(EVO, "Evidences of evolution", B, D,
  "NCERT notes that man's intensive breeding programmes have created breeds that differ from other breeds but still "
  "are of the same group. Which animal does NCERT give as the example?",
  "Artificial selection by man",
  "NCERT: man has bred selected plants and animals for agriculture, horticulture, sport and security, and has "
  "domesticated many wild animals and crops. This intensive breeding programme has created breeds that differ from "
  "other breeds (e.g., dogs) but still are of the same group.",
  ["Example given: breeds of dogs"],
  "What are the Evidences for Evolution?",
  at="D", correct="Dogs",
  wrong=["Moths", "Finches", "Marsupials"],
  why="Moths are NCERT's example of industrial melanism, finches of adaptive radiation in the Galapagos, and "
      "marsupials of adaptive radiation in Australia; none of these is an example of breeds made by man.", secs=20)

Z(EVO, "Natural selection", B, D,
  "According to NCERT, evolution by natural selection, in a true sense, would have started when:",
  "Beginning of evolution by natural selection",
  "NCERT (Biological Evolution): evolution by natural selection, in a true sense, would have started when cellular "
  "forms of life with differences in metabolic capability originated on earth. Selection needs differences among "
  "individuals that affect survival and reproduction.",
  ["Natural selection needs variation", "Start: cellular forms of life with differences in metabolic capability"],
  "Biological Evolution",
  at="B", correct="Cellular forms of life with differences in metabolic capability originated on earth",
  wrong=["The first giant molecules such as RNA and proteins formed in the oceans",
         "The first mammals appeared on land",
         "Human beings began agriculture and settlements"],
  why="NCERT links true natural selection to cellular life with metabolic differences, not to the earlier "
      "non-cellular giant molecules; mammals and agriculture came far later in the history of life.", secs=30)

Z(EVO, "Origin of life", B, D,
  "Early Greek thinkers thought that units of life called spores were transferred to different planets, including "
  "the earth. According to NCERT, this idea of 'panspermia' is still a favourite idea for:",
  "Panspermia",
  "NCERT: some scientists believe that life came from outer space. Early Greek thinkers thought units of life called "
  "spores were transferred to different planets including earth. 'Panspermia' is still a favourite idea for some "
  "astronomers.",
  ["Panspermia: spores transferred between planets", "Still favoured by some astronomers"],
  "Origin of Life",
  at="B", correct="Some astronomers",
  wrong=["Oparin and Haldane", "Louis Pasteur", "Most biologists"],
  why="Oparin and Haldane proposed chemical evolution from non-living organic molecules; Pasteur showed that life "
      "comes only from pre-existing life; NCERT says the majority accept that life arose through evolutionary forces "
      "from non-living molecules.", secs=25)

Z(EVO, "Natural selection", B, ASR,
  AR("In England, the collection of moths made in the 1850s had more dark-winged (melanised) moths than "
     "white-winged moths.",
     "The 1850s collection of moths was made before industrialisation set in."),
  "Industrial melanism: the 1850s collection",
  "NCERT: in a collection of moths made in the 1850s, i.e. before industrialisation set in, there were more "
  "white-winged moths on trees than dark-winged or melanised moths; in the collection from the same area after "
  "industrialisation (1920), there were more dark-winged moths. So A is false and R is true.",
  ["A: false - the 1850s collection had more white-winged moths", "R: true - it was pre-industrial"],
  "What are the Evidences for Evolution?", ans="D",
  why="A reverses NCERT's observation for the 1850s, so all options calling A true are wrong; R is correct, so "
      "'A is false but R is true' is the answer.", secs=30)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a. The combined frequency of the "
  "two homozygous genotypes (AA + aa) is exactly equal to the frequency of the heterozygous genotype (Aa). What is "
  "the frequency of allele a?",
  "Hardy-Weinberg: equating homozygotes and heterozygotes",
  "Under Hardy-Weinberg equilibrium the genotype frequencies are p² (AA), 2pq (Aa) and q² (aa), with p + q = 1 and "
  "p² + 2pq + q² = 1. If p² + q² = 2pq, then p² - 2pq + q² = 0, i.e. (p - q)² = 0, so p = q = 0.5.",
  ["p² + q² = 2pq", "(p - q)² = 0 -> p = q", "p + q = 1 -> q = 0.5"],
  "Hardy-Weinberg Principle",
  at="B", correct="0.5",
  wrong=["0.25", "0.71", "0.33"],
  why="0.25 is q² at p = q, not q; 0.71 comes from wrongly setting q² = 0.5; 0.33 comes from treating the three "
      "genotypes as equally frequent.", short="Homozygotes = heterozygotes = 0.5 each, which happens only when p = q.",
  secs=60, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", I, D,
  "The flippers of penguins (birds) and of dolphins (mammals) look alike and perform the same function. According to "
  "NCERT, which of the following best explains such similarity?",
  "Analogy and similar habitat",
  "NCERT: analogous structures are a result of convergent evolution - different structures evolving for the same "
  "function and hence having similarity; the flippers of penguins and dolphins are an example. One can say that it "
  "is the similar habitat that has resulted in selection of similar adaptive features in different groups of "
  "organisms, but towards the same function.",
  ["Flippers: analogous (convergent evolution)", "Cause: similar habitat selects similar adaptive features"],
  "What are the Evidences for Evolution?",
  at="A",
  correct="A similar habitat has resulted in the selection of similar adaptive features in different groups of "
          "organisms, towards the same function",
  wrong=["The same structure developed along different directions due to adaptations to different needs",
         "Penguins and dolphins arose from one ancestral stock within a single adaptive radiation",
         "The flippers were developed by use during the lives of the animals and passed on to the offspring"],
  why="Development of one structure in different directions describes homology (divergent evolution); penguins and "
      "dolphins belong to different groups and are not one adaptive radiation; inheritance of characters acquired by "
      "use is Lamarck's idea, not NCERT's explanation.", secs=40)

Z(EVO, "Evidences of evolution", I, ASR,
  AR("NCERT argues that nature could have created new types of organisms over millions of years.",
     "Within hundreds of years, man has been able to create new breeds of animals and plants by intensive breeding "
     "programmes."),
  "Argument from artificial selection",
  "NCERT: man has bred selected plants and animals and, by intensive breeding programmes, created breeds that differ "
  "from other breeds but still are of the same group. It is argued that if within hundreds of years man could create "
  "new breeds, could not nature have done the same over millions of years? The argument in A rests directly on the "
  "fact in R.",
  ["R: man-made breeds within hundreds of years", "A: inference - nature could do the same over millions of years",
   "R is the basis of A -> R explains A"],
  "What are the Evidences for Evolution?", ans="A",
  why="A is drawn by NCERT from R itself, so 'R is not the explanation' is wrong; both statements are NCERT's own, so "
      "the options calling either false are wrong.", secs=40)

Z(EVO, "Darwinism and modern synthesis", I, STP,
  SP("Although Mendel had talked of inheritable 'factors' influencing the phenotype, Darwin either ignored or kept "
     "silence on these aspects.",
     "Hugo de Vries believed that the minor heritable variations described by Darwin, rather than mutations, cause "
     "evolution."),
  "Source of variation: Darwin and de Vries",
  "NCERT (Mechanism of Evolution): even though Mendel had talked of inheritable 'factors' influencing phenotype, "
  "Darwin either ignored or kept silence on these aspects. The work of Hugo de Vries on evening primrose brought "
  "forth the idea of mutations; he believed that it is mutation which causes evolution and not the minor "
  "(heritable) variations that Darwin talked about.",
  ["Statement I: true", "Statement II: false - de Vries held the reverse"],
  "Mechanism of Evolution", ans="C",
  why="Statement II reverses de Vries' view, so options calling it true are wrong; Statement I is NCERT's own line, "
      "so 'both false' and 'Statement I false' are wrong.", secs=35)

Z(EVO, "Darwinism and modern synthesis", I, MAT,
  ML(("term", "description given in NCERT"),
     ["Darwinian variations", "Mutations (as proposed by de Vries)", "Evolution, as Darwin saw it",
      "Saltation"],
     ["Single-step large mutation", "Gradual", "Random and directionless", "Small and directional"]),
  "Darwin's and de Vries' views compared",
  "NCERT: mutations are random and directionless while Darwinian variations are small and directional. Evolution "
  "for Darwin was gradual, while de Vries believed mutation caused speciation and hence called it saltation "
  "(single-step large mutation).",
  ["A -> IV", "B -> III", "C -> II", "D -> I"],
  "Mechanism of Evolution",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="Swapping A and B gives Darwin's variations the features of mutations; swapping C and D makes Darwin's "
      "evolution saltatory; the last code mismatches every term.", secs=45)

Z(EVO, "Evidences of evolution", I, STP,
  SP("The study of fossils shows that every form of life has existed throughout the whole history of the earth.",
     "The study of fossils shows that certain life forms are restricted to certain geological time-spans, so new "
     "forms of life have arisen at different times in the history of the earth."),
  "What fossils show",
  "NCERT: the study of fossils in different sedimentary layers indicates the geological period in which they "
  "existed. The study showed that life-forms varied over time and certain life forms are restricted to certain "
  "geological time-spans. Hence new forms of life have arisen at different times in the history of the earth. This "
  "is palaeontological evidence.",
  ["Statement I: false - life forms varied over time", "Statement II: true"],
  "What are the Evidences for Evolution?", ans="D",
  why="Statement I contradicts the fossil record described by NCERT, so options calling it true are wrong; Statement "
      "II is NCERT's conclusion, so 'both false' is wrong.", secs=35)

Z(EVO, "Human evolution", I, D,
  "NCERT compares the skulls of an adult modern human being, a baby chimpanzee and an adult chimpanzee. What does "
  "this comparison show?",
  "Comparison of skulls",
  "NCERT (Origin and Evolution of Man) gives a comparison of the skulls of an adult modern human being, a baby "
  "chimpanzee and an adult chimpanzee, and notes that the skull of the baby chimpanzee is more like the adult human "
  "skull than the adult chimpanzee skull.",
  ["Baby chimpanzee skull resembles the adult human skull more than the adult chimpanzee skull"],
  "Origin and Evolution of Man",
  at="C",
  correct="The skull of the baby chimpanzee is more like the adult human skull than the adult chimpanzee skull",
  wrong=["The skull of the adult chimpanzee is more like the adult human skull than the baby chimpanzee skull",
         "The skulls of the baby and the adult chimpanzee are identical, and both differ from the human skull",
         "The skull of the baby chimpanzee resembles neither the adult chimpanzee skull nor the adult human skull"],
  why="NCERT's point is the reverse of the first option; baby and adult chimpanzee skulls are not identical; and the "
      "baby chimpanzee skull does resemble the adult human skull.", secs=30)

Z(EVO, "Natural selection", I, STP,
  SP("In rural areas of England where industrialisation had not occurred, the count of melanic (dark-winged) moths "
     "was low.",
     "According to NCERT, this observation supports the belief that, in a given background, moths that did not "
     "match the background were picked out by predators."),
  "Industrial melanism: evidence from rural areas",
  "NCERT: before industrialisation, thick growth of almost white-coloured lichen covered the trees and the "
  "white-winged moths survived while dark moths were picked out by predators; after industrialisation, the trunks "
  "became dark with smoke and the reverse happened. NCERT adds that this belief is supported by the fact that in "
  "rural areas where industrialisation had not occurred, the count of melanic moths was low.",
  ["Statement I: true (NCERT)", "Statement II: true - NCERT uses it as support for the predation explanation"],
  "What are the Evidences for Evolution?", ans="A",
  why="Both statements are NCERT's own, so each option with a false statement is wrong.", secs=35)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a, and allele A is the more "
  "common one. The frequency of the AA genotype exceeds that of the aa genotype by exactly 0.20. What is the "
  "frequency of heterozygotes (Aa)?",
  "Hardy-Weinberg: difference of homozygote frequencies",
  "p² - q² = (p + q)(p - q). Since p + q = 1, p² - q² = p - q. So p - q = 0.20 and p + q = 1, giving p = 0.6 and "
  "q = 0.4. The heterozygote frequency is 2pq = 2 x 0.6 x 0.4 = 0.48. Check: p² = 0.36, q² = 0.16, difference "
  "0.20.",
  ["p² - q² = (p + q)(p - q) = p - q = 0.20", "p = 0.6, q = 0.4", "2pq = 0.48"],
  "Hardy-Weinberg Principle",
  at="C", correct="0.48",
  wrong=["0.42", "0.32", "0.50"],
  why="0.42 uses p = 0.7 (taking the difference of allele frequencies as 0.4); 0.32 uses p = 0.8 (treating 0.2 as "
      "q); 0.50 assumes p = q, which would make the homozygote frequencies equal.",
  short="For two alleles, p² - q² always equals p - q.", secs=90, vb=RECOMPUTED)

Z(EVO, "Natural selection", A, MUL,
  MS("Which of the following statements about fitness are correct according to NCERT?",
     ["The so-called fitness is based on characteristics which are inherited.",
      "Adaptive ability is inherited; it has a genetic basis.",
      "Fitness is the end result of the ability to adapt and get selected by nature.",
      "According to Darwin, the fitness of an individual refers to its physical strength.",
      "Characters developed by the use of organs during an individual's life form the basis of fitness."]),
  "Fitness and its genetic basis",
  "NCERT: nature selects for fitness; the so-called fitness is based on characteristics which are inherited, so "
  "there must be a genetic basis for getting selected and to evolve. Some organisms are better adapted to survive "
  "in an otherwise hostile environment; adaptive ability is inherited and has a genetic basis. Fitness is the end "
  "result of the ability to adapt and get selected by nature. For Darwin, fitness ultimately and only refers to "
  "reproductive fitness. Use and disuse of organs is Lamarck's idea.",
  ["(a), (b), (c): NCERT's statements", "(d): false - reproductive fitness",
   "(e): false - acquired characters (Lamarck), not inherited ones"],
  "Biological Evolution; Evolution of Life Forms - A Theory",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only"],
  why="'(a) and (b) only' leaves out NCERT's description of fitness as the end result of adaptation and selection; "
      "fitness in Darwin's sense is reproductive, not physical strength, and fitness rests on inherited, not acquired, "
      "characters, so options with (d) or (e) are wrong.", secs=60)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "In a very large population with no migration, no new mutations and random mating, individuals of genotype aa "
  "consistently leave fewer surviving offspring than AA and Aa individuals in every generation, and the frequency of "
  "allele a falls steadily. Which of the factors that NCERT lists as affecting Hardy-Weinberg equilibrium is acting "
  "here?",
  "Identifying the factor disturbing Hardy-Weinberg equilibrium",
  "NCERT lists five factors that affect Hardy-Weinberg equilibrium: gene migration (gene flow), genetic drift, "
  "mutation, genetic recombination and natural selection. Natural selection is a process in which heritable "
  "variations enabling better survival are enabled to reproduce and leave a greater number of progeny. Here a "
  "genotype consistently leaves fewer offspring - a systematic, not chance, effect - in a very large population with "
  "no migration or mutation.",
  ["No migration -> not gene flow", "Very large population, consistent effect -> not chance (drift)",
   "Differential reproduction by genotype -> natural selection"],
  "Hardy-Weinberg Principle",
  at="B", correct="Natural selection",
  wrong=["Genetic drift", "Gene flow", "Founder effect"],
  why="Genetic drift and the founder effect are chance changes, typically in small samples, not a steady, "
      "genotype-linked difference in reproduction in a very large population; gene flow needs migration, which the "
      "stem excludes.", secs=50)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, STP,
  SP("If the allele frequencies of a population remain stable and constant from generation to generation, the "
     "population is undergoing evolution.",
     "A change in the frequency of alleles in a population, i.e. a disturbance of Hardy-Weinberg equilibrium, is "
     "interpreted as resulting in evolution."),
  "Genetic equilibrium and evolution",
  "NCERT: the Hardy-Weinberg principle says that allele frequencies in a population are stable and constant from "
  "generation to generation; the gene pool remains a constant (genetic equilibrium). Disturbance in genetic "
  "equilibrium, or Hardy-Weinberg equilibrium, i.e. a change of frequency of alleles in a population, is then "
  "interpreted as resulting in evolution. Stable allele frequencies therefore mean no evolution at that gene.",
  ["Statement I: false - stable frequencies = genetic equilibrium", "Statement II: true"],
  "Hardy-Weinberg Principle", ans="D",
  why="Statement I describes equilibrium as evolution, the opposite of NCERT, so options calling it true are wrong; "
      "Statement II is NCERT's interpretation, so 'both false' is wrong.", secs=45)

Z(EVO, "Human evolution", A, ASR,
  AR("Of the two early primates Dryopithecus and Ramapithecus, Ramapithecus was more man-like while "
     "Dryopithecus was more ape-like.",
     "Both Dryopithecus and Ramapithecus were hairy and walked like gorillas and chimpanzees."),
  "Dryopithecus and Ramapithecus",
  "NCERT describes the early primates Dryopithecus and Ramapithecus: they were hairy and walked like "
  "gorillas and chimpanzees. Ramapithecus was more man-like while Dryopithecus was more ape-like. R describes "
  "features the two shared, so it cannot explain how they differed.",
  ["A: true", "R: true", "R gives shared features; A is a difference -> R is not the explanation"],
  "Origin and Evolution of Man", ans="B",
  why="A shared feature cannot explain a difference between the two primates, so 'R is the correct explanation' is "
      "wrong; both statements are NCERT's, so the options calling either false are wrong.", secs=40)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "For a gene with two alleles, A (frequency p) and a (frequency q), in a population in Hardy-Weinberg equilibrium, "
  "which of the following is ALWAYS true, whatever the value of p?",
  "Limits of Hardy-Weinberg genotype frequencies",
  "Genotype frequencies are p², 2pq and q² with p + q = 1. The heterozygote frequency 2pq = 2p(1 - p) is largest when "
  "p = 0.5, where it equals 0.5; for any other p it is smaller. So 2pq can never exceed 0.5. The other statements "
  "fail for some value of p: for p = 0.5, AA (0.25) is less than Aa (0.5); for p = 0.9, 2pq = 0.18 is less than "
  "p² + q² = 0.82; q² equals q only when q is 0 or 1.",
  ["2pq = 2p(1 - p), maximum at p = 0.5", "Maximum value = 2 x 0.5 x 0.5 = 0.5",
   "Counter-examples rule out the other options"],
  "Hardy-Weinberg Principle",
  at="C", correct="The frequency of heterozygotes (2pq) can never exceed 0.5",
  wrong=["The frequency of genotype AA is always greater than that of genotype Aa",
         "The frequency of heterozygotes is always greater than the combined frequency of the two homozygotes",
         "The frequency of genotype aa is always equal to the frequency of allele a"],
  why="At p = 0.5, AA (0.25) is less than Aa (0.5); at p = 0.9, heterozygotes (0.18) are fewer than homozygotes "
      "(0.82); q² equals q only when q is 0 or 1.", secs=75, vb=RECOMPUTED)


# ================================================================ Human Health and Disease (7/9/7)
Z(HHD, "Immunity and vaccines", B, D,
  "Which of the following is NOT among the cells that NCERT lists as the cellular barriers of innate immunity?",
  "Cellular barriers of innate immunity",
  "NCERT: certain types of leukocytes of our body like polymorpho-nuclear leukocytes (PMNL - neutrophils), monocytes "
  "and natural killer cells (a type of lymphocyte) in the blood, as well as macrophages in tissues, can phagocytose "
  "and destroy microbes; these are the cellular barriers of innate immunity. B-lymphocytes belong to acquired "
  "immunity: they produce antibodies (humoral immune response).",
  ["Cellular barriers: neutrophils (PMNL), monocytes, NK cells, macrophages",
   "B-lymphocytes: acquired immunity (antibodies)"],
  "Immunity",
  at="A", correct="B-lymphocytes",
  wrong=["Neutrophils (PMNL)", "Natural killer cells", "Macrophages"],
  why="Neutrophils, natural killer cells and macrophages are all named by NCERT as phagocytic cells forming the "
      "cellular barrier of innate immunity.", secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "The thymus is quite large at the time of birth but keeps reducing in size with age. According to NCERT, it "
  "reduces to a very small size by the time:",
  "Thymus and age",
  "NCERT: the thymus is a lobed organ located near the heart and beneath the breastbone. It is quite large at the "
  "time of birth but keeps reducing in size with age, and by the time puberty is attained it reduces to a very "
  "small size.",
  ["Large at birth -> reduces with age -> very small by puberty"],
  "Immunity",
  at="C", correct="Puberty is attained",
  wrong=["The child is one year old", "Old age (about 60 years) is reached", "Menopause sets in"],
  why="NCERT names puberty as the stage by which the thymus becomes very small; the other stages are not given.",
  secs=20)

Z(HHD, "Pathogens and diseases", B, STP,
  SP("Ascaris, the common round worm, is an intestinal parasite that causes ascariasis.",
     "Wuchereria (W. bancrofti and W. malayi), the filarial worms, cause filariasis."),
  "Pathogenic helminths",
  "NCERT: many helminths are pathogenic for man. Ascaris, the common round worm, and Wuchereria, the filarial worm, "
  "are some of them. Ascaris, an intestinal parasite, causes ascariasis. Wuchereria (W. bancrofti and W. malayi), "
  "the filarial worms, cause a slowly developing chronic inflammation of the organs in which they live for many "
  "years, usually the lymphatic vessels of the lower limbs; the disease is called elephantiasis or filariasis.",
  ["Statement I: true", "Statement II: true"],
  "Common Diseases in Humans", ans="A",
  why="Both statements are NCERT's own descriptions, so every option calling one of them false is wrong.", secs=25)

Z(HHD, "Pathogens and diseases", B, ASR,
  AR("Typhoid fever can be confirmed by the Widal test.",
     "Salmonella typhi generally enters the small intestine through contaminated food and water."),
  "Typhoid: diagnosis and entry",
  "NCERT: Salmonella typhi is the pathogenic bacterium that causes typhoid fever in human beings. It generally "
  "enters the small intestine through food and water contaminated with it and migrates to other organs through "
  "blood. Typhoid fever could be confirmed by the Widal test. Both statements are true, but the route by which the "
  "pathogen enters the body does not explain how the disease is confirmed by a test.",
  ["A: true", "R: true", "R is about entry, A is about diagnosis -> not the explanation"],
  "Common Diseases in Humans", ans="B",
  why="R describes how the infection is acquired, which is unrelated to the diagnostic test in A, so 'R is the "
      "correct explanation' is wrong; both are NCERT statements, so the options with a false statement are wrong.",
  secs=30)

Z(HHD, "Pathogens and diseases", B, MAT,
  ML(("disease", "vector, carrier or mode of spread described in NCERT"),
     ["Malaria", "Dengue", "Amoebiasis", "Ringworm"],
     ["Houseflies acting as mechanical carriers", "Using towels, clothes or even the comb of infected individuals",
      "Female Anopheles mosquito", "Aedes mosquitoes"]),
  "How some diseases spread",
  "NCERT: malaria is transmitted by the bite of the infected female Anopheles mosquito; dengue and chikungunya are "
  "vector-borne diseases spread by Aedes mosquitoes; in amoebiasis, houseflies act as mechanical carriers and "
  "transmit the parasite from the faeces of infected persons to food; ringworms are generally acquired from soil or "
  "by using towels, clothes or even the comb of infected individuals.",
  ["A -> III", "B -> IV", "C -> I", "D -> II"],
  "Common Diseases in Humans",
  at="D", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "II", "C": "III", "D": "IV"}]),
  why="Swapping the two mosquitoes confuses the vectors of malaria (Anopheles) and dengue (Aedes); houseflies carry "
      "the amoebiasis parasite, not ringworm; the last code mismatches every disease.", secs=40)

Z(HHD, "Pathogens and diseases", B, D,
  "Which of the following pairs of human diseases are BOTH caused by protozoans?",
  "Protozoan diseases",
  "NCERT: malaria is caused by Plasmodium (P. vivax, P. malariae, P. falciparum), a tiny protozoan; amoebiasis "
  "(amoebic dysentery) is caused by Entamoeba histolytica, a protozoan parasite of the large intestine. Filariasis "
  "and ascariasis are caused by helminths, and typhoid by a bacterium.",
  ["Malaria: Plasmodium (protozoan)", "Amoebiasis: Entamoeba histolytica (protozoan)"],
  "Common Diseases in Humans",
  at="B", correct="Malaria and amoebiasis",
  wrong=["Malaria and filariasis", "Amoebiasis and ascariasis", "Typhoid and amoebiasis"],
  why="Filariasis (Wuchereria) and ascariasis (Ascaris) are helminth diseases, and typhoid is caused by the "
      "bacterium Salmonella typhi, so each other pair contains a non-protozoan disease.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Which of the following sets gives the features of the withdrawal syndrome, as described in NCERT, that appears "
  "when the regular dose of drugs or alcohol is abruptly discontinued?",
  "Withdrawal syndrome",
  "NCERT: dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal syndrome if "
  "the regular dose of drugs/alcohol is abruptly discontinued. This is characterised by anxiety, shakiness, nausea "
  "and sweating, which may be relieved when use is resumed again.",
  ["Withdrawal syndrome: anxiety, shakiness, nausea, sweating"],
  "Drugs and Alcohol Abuse",
  at="C", correct="Anxiety, shakiness, nausea and sweating",
  wrong=["A sense of euphoria, increased energy and hallucinations", "Reckless behaviour, vandalism and violence",
         "Hair loss and anaemia"],
  why="Euphoria, increased energy and (in excess) hallucinations are effects of cocaine; reckless behaviour, "
      "vandalism and violence are the immediate adverse effects of drug abuse; hair loss and anaemia are side effects "
      "of chemotherapeutic drugs.", secs=30)

Z(HHD, "Immunity and vaccines", I, D,
  "According to NCERT, which organ(s) provide the micro-environments for the development and maturation of "
  "T-lymphocytes?",
  "Primary lymphoid organs and T-lymphocytes",
  "NCERT: the bone marrow is the main lymphoid organ where all blood cells including lymphocytes are produced. The "
  "thymus is a lobed organ located near the heart beneath the breastbone. Both bone marrow and thymus provide "
  "micro-environments for the development and maturation of T-lymphocytes.",
  ["NCERT: 'Both bone marrow and thymus provide micro-environments' for T-lymphocyte development and maturation"],
  "Immunity",
  at="D", correct="Both the bone marrow and the thymus",
  wrong=["The thymus only", "The spleen and the lymph nodes", "The bone marrow only"],
  why="NCERT names both primary lymphoid organs, so either one alone is incomplete; the spleen and lymph nodes are "
      "secondary lymphoid organs, to which mature lymphocytes migrate.", secs=30)

Z(HHD, "Pathogens and diseases", I, D,
  "How many of the following diseases are caused by helminths?\n\n"
  "Ascariasis, filariasis, amoebiasis, ringworm, malaria, pneumonia",
  "Helminth diseases",
  "NCERT: Ascaris (common round worm) causes ascariasis and Wuchereria (filarial worm) causes filariasis; both are "
  "helminths. Amoebiasis (Entamoeba histolytica) and malaria (Plasmodium) are protozoan diseases, ringworm is "
  "caused by fungi, and pneumonia by bacteria (Streptococcus pneumoniae, Haemophilus influenzae).",
  ["Helminths: ascariasis, filariasis = 2", "Protozoa: amoebiasis, malaria", "Fungi: ringworm",
   "Bacteria: pneumonia"],
  "Common Diseases in Humans",
  at="A", correct="Two",
  wrong=["One", "Three", "Four"],
  why="One leaves out either ascariasis or filariasis; three or four wrongly add ringworm (a fungal disease) or the "
      "protozoan diseases, amoebiasis and malaria.", secs=35)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("Lymph nodes are secondary lymphoid organs.",
     "In the lymph nodes, immature lymphocytes differentiate into antigen-sensitive lymphocytes."),
  "Primary versus secondary lymphoid organs",
  "NCERT: the primary lymphoid organs are the bone marrow and thymus, where immature lymphocytes differentiate into "
  "antigen-sensitive lymphocytes. After maturation the lymphocytes migrate to secondary lymphoid organs like the "
  "spleen, lymph nodes, tonsils, Peyer's patches of the small intestine and appendix, which provide the sites for "
  "interaction of lymphocytes with the antigen. So A is true, and R describes a primary lymphoid organ, not a lymph "
  "node.",
  ["A: true - lymph nodes are secondary", "R: false - differentiation occurs in bone marrow and thymus"],
  "Immunity", ans="C",
  why="R attributes to lymph nodes the role of the primary lymphoid organs, so options calling R true are wrong; A "
      "is NCERT's own classification, so 'A is false' is wrong.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Cannabinoids are obtained from the inflorescences of the plant Cannabis sativa.",
     "The flower tops, leaves and resin of the cannabis plant are used in various combinations to produce "
     "marijuana, hashish, charas and ganja."),
  "Cannabinoids",
  "NCERT: cannabinoids are a group of chemicals which interact with cannabinoid receptors present principally in the "
  "brain. Natural cannabinoids are obtained from the inflorescences of the plant Cannabis sativa. The flower tops, "
  "leaves and the resin of the cannabis plant are used in various combinations to produce marijuana, hashish, "
  "charas and ganja.",
  ["Statement I: true", "Statement II: true"],
  "Drugs and Alcohol Abuse", ans="A",
  why="Both statements are NCERT's own, so every option calling one of them false is wrong.", secs=30)

Z(HHD, "Cancer", I, MAT,
  ML(("cancer detection or treatment", "NCERT description"),
     ["Detection of leukaemia", "Radiation therapy", "Chemotherapy", "Immunotherapy"],
     ["Biological response modifiers such as alpha-interferon activate the immune system",
      "Most of the drugs have side effects like hair loss and anaemia",
      "Tumour cells are irradiated lethally, taking proper care of the surrounding normal tissues",
      "Blood and bone marrow tests for increased cell counts"]),
  "Detection and treatment of cancer",
  "NCERT: in the case of leukaemia, blood and bone marrow tests for increased cell counts are done. In radiotherapy, "
  "tumour cells are irradiated lethally, taking proper care of the normal tissues surrounding the tumour mass. "
  "Several chemotherapeutic drugs are used to kill cancerous cells, and the majority have side effects like hair "
  "loss and anaemia. Patients are given substances called biological response modifiers such as alpha-interferon, "
  "which activate their immune system and help in destroying the tumour.",
  ["A -> IV", "B -> III", "C -> II", "D -> I"],
  "Cancer",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "I", "B": "II", "C": "IV", "D": "III"}]),
  why="Irradiation is a treatment, not the test for leukaemia, so swapping A and B is wrong; alpha-interferon is the "
      "basis of immunotherapy, while hair loss and anaemia are chemotherapy side effects, so swapping C and D is "
      "wrong; the last code mismatches every row.", secs=45)

Z(HHD, "Immunity and vaccines", I, MUL,
  MS("Which of the following are PHYSIOLOGICAL barriers of innate immunity, according to NCERT?",
     ["Acid in the stomach", "Saliva in the mouth", "Tears from the eyes",
      "Mucus coating of the epithelium lining the respiratory tract",
      "Interferons secreted by virus-infected cells"]),
  "Kinds of innate barriers",
  "NCERT: innate immunity has four types of barriers. Physical barriers: skin, and the mucus coating of the "
  "epithelium lining the respiratory, gastrointestinal and urogenital tracts. Physiological barriers: acid in the "
  "stomach, saliva in the mouth, tears from the eyes - all prevent microbial growth. Cellular barriers: PMNL "
  "(neutrophils), monocytes, natural killer cells and macrophages. Cytokine barriers: interferons secreted by "
  "virus-infected cells, which protect non-infected cells from further viral infection.",
  ["Physiological: (a), (b), (c)", "(d): physical barrier", "(e): cytokine barrier"],
  "Immunity",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(a) and (c) only", "(a), (b), (c) and (e) only"],
  why="The mucus coating of epithelia is a physical barrier and interferons are a cytokine barrier, so options with "
      "(d) or (e) are wrong; '(a) and (c) only' leaves out saliva, which NCERT lists as a physiological barrier.",
  secs=45)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Adolescence is accompanied by several biological and behavioural changes and is a very vulnerable phase of "
     "mental and psychological development of an individual.",
     "According to NCERT, adolescence may be thought of as the period between 18 and 25 years of age."),
  "Adolescence",
  "NCERT: adolescence means both 'a period' and 'a process' during which a child becomes mature in terms of his/her "
  "attitudes and beliefs for effective participation in society. The period between 12-18 years of age may be "
  "thought of as the adolescence period. Adolescence is accompanied by several biological and behavioural changes; "
  "it is thus a very vulnerable phase of mental and psychological development.",
  ["Statement I: true", "Statement II: false - NCERT gives 12-18 years"],
  "Drugs and Alcohol Abuse", ans="C",
  why="Statement II gives the wrong age range (NCERT: 12-18 years), so options calling it true are wrong; Statement I "
      "is NCERT's description, so 'both false' and 'Statement I false' are wrong.", secs=30)

Z(HHD, "Pathogens and diseases", I, ASR,
  AR("Ringworm is generally acquired by inhaling droplets or aerosols released by an infected person.",
     "Ringworm is caused by fungi belonging to the genera Microsporum, Trichophyton and Epidermophyton."),
  "Ringworm: cause and spread",
  "NCERT: many fungi belonging to the genera Microsporum, Trichophyton and Epidermophyton are responsible for "
  "ringworms, one of the most common infectious diseases in man. Ringworms are generally acquired from soil or by "
  "using towels, clothes or even the comb of infected individuals. Inhalation of droplets/aerosols is how pneumonia "
  "spreads. So A is false and R is true.",
  ["A: false - acquired from soil or shared towels, clothes, combs", "R: true"],
  "Common Diseases in Humans", ans="D",
  why="A describes the spread of pneumonia, not ringworm, so all options with A true are wrong; R is NCERT's list of "
      "ringworm fungi, so 'A is false but R is true' is correct.", secs=30)

Z(HHD, "HIV and AIDS", I, ASR,
  AR("Individuals who require repeated blood transfusions are at high risk of getting HIV infection.",
     "HIV can be transmitted by transfusion of contaminated blood and blood products."),
  "High-risk groups for HIV",
  "NCERT: HIV is transmitted generally by sexual contact with an infected person, by transfusion of contaminated "
  "blood and blood products, by sharing infected needles, and from an infected mother to her child through the "
  "placenta. So, people at high risk include individuals who require repeated blood transfusions. Since each "
  "transfusion is a possible route of entry, R directly explains A.",
  ["Route: contaminated blood transfusion (R)", "Repeated transfusions -> repeated exposure -> high risk (A)"],
  "AIDS", ans="A",
  why="R gives the very route that makes repeated transfusion risky, so 'R is not the explanation' is wrong; both "
      "statements are NCERT's own, so the options with a false statement are wrong.", secs=30)

Z(HHD, "Pathogens and diseases", A, D,
  "Which option arranges the following events in the life cycle of Plasmodium in the correct order, according to "
  "NCERT?\n\n(P) The parasites multiply within the liver cells of the human\n(Q) Sporozoites enter the human body "
  "through the bite of an infected female Anopheles mosquito\n(R) The parasites attack the red blood cells, which "
  "rupture and release haemozoin\n(S) A female Anopheles takes up gametocytes with the blood meal, and fertilisation "
  "and development take place in its stomach\n(T) Sporozoites formed in the mosquito are stored in its salivary "
  "glands",
  "Life cycle of Plasmodium",
  "NCERT: Plasmodium enters the human body as sporozoites (infectious form) through the bite of an infected female "
  "Anopheles mosquito (Q). The parasites initially multiply within the liver cells (P) and then attack the red "
  "blood cells, resulting in their rupture and release of haemozoin (R). The sexual stages (gametocytes) develop in "
  "the red blood cells; when a female Anopheles bites an infected person, these enter the mosquito, where "
  "fertilisation and development take place in the stomach (S). The parasites multiply to form sporozoites that are "
  "stored in the salivary glands (T), ready for the next bite.",
  ["Q -> P (liver) -> R (RBCs) -> S (mosquito stomach) -> T (salivary glands)"],
  "Common Diseases in Humans",
  at="D", correct="Q -> P -> R -> S -> T",
  wrong=["Q -> R -> P -> S -> T", "P -> Q -> R -> T -> S", "Q -> P -> R -> T -> S"],
  why="The parasites multiply in the liver before attacking RBCs, so R cannot precede P; sporozoites must enter "
      "before any multiplication in the human, so P cannot come first; sporozoites stored in the salivary glands are "
      "formed only after fertilisation in the mosquito, so T cannot precede S.", secs=60)

Z(HHD, "Drug and alcohol abuse", A, D,
  "Which one of the following sets of drug, source and usual mode of intake is entirely correct according to NCERT?",
  "Drugs: source and mode of intake",
  "NCERT: heroin (smack, diacetylmorphine) is obtained by acetylation of morphine, which is extracted from the latex "
  "of the poppy plant Papaver somniferum; it is generally taken by snorting and injection. Cannabinoids are obtained "
  "from the inflorescences of Cannabis sativa and are generally taken by inhalation and oral ingestion. Cocaine is "
  "obtained from the coca plant Erythroxylum coca, native to South America, and is usually snorted.",
  ["Cocaine: Erythroxylum coca, usually snorted", "Heroin: from morphine (poppy latex), snorting and injection",
   "Cannabinoids: Cannabis sativa inflorescences, inhalation and oral ingestion"],
  "Drugs and Alcohol Abuse",
  at="B", correct="Cocaine - Erythroxylum coca - usually snorted",
  wrong=["Heroin - inflorescences of Cannabis sativa - snorting and injection",
         "Heroin - acetylation of morphine from poppy latex - inhalation and oral ingestion",
         "Cannabinoids - latex of Papaver somniferum - inhalation and oral ingestion"],
  why="Heroin does not come from Cannabis; heroin is taken by snorting and injection, not by inhalation and oral "
      "ingestion; cannabinoids come from Cannabis sativa, not the poppy plant.", secs=50)

Z(HHD, "Pathogens and diseases", A, MUL,
  MS("Which of the following statements are true for BOTH malaria and filariasis, according to NCERT?",
     ["The disease is transmitted through an insect vector (a female mosquito).",
      "The pathogen is a protozoan.",
      "The most important preventive measure is to control or eliminate the vectors and their breeding places.",
      "The pathogen first multiplies within the liver cells of the human.",
      "The pathogen lives for many years in the lymphatic vessels of the lower limbs."]),
  "Malaria and filariasis compared",
  "NCERT: malaria is caused by Plasmodium, a protozoan, transmitted by the female Anopheles mosquito; the parasites "
  "first multiply within liver cells. Filariasis is caused by Wuchereria, a helminth (filarial worm), transmitted by "
  "the bite of female mosquito vectors; the worms live for many years in the lymphatic vessels of the lower limbs. "
  "In case of diseases such as malaria and filariasis that are transmitted through insect vectors, the most "
  "important measure is to control or eliminate the vectors and their breeding places.",
  ["(a), (c): true for both", "(b), (d): only malaria", "(e): only filariasis"],
  "Common Diseases in Humans",
  at="A", correct="(a) and (c) only",
  wrong=["(a), (b) and (c) only", "(a), (c) and (e) only", "(a), (b), (c) and (d) only"],
  why="Wuchereria is a helminth and does not multiply in the liver, so (b) and (d) apply only to malaria; Plasmodium "
      "does not live in lymphatic vessels, so (e) applies only to filariasis.", secs=60)

Z(HHD, "Pathogens and diseases", A, STP,
  SP("Typhoid and amoebiasis are both acquired through contaminated food or water, but it is for amoebiasis that "
     "NCERT names houseflies as mechanical carriers of the pathogen.",
     "Pneumonia and the common cold both infect the alveoli of the lungs."),
  "Comparing modes of infection",
  "NCERT: Salmonella typhi enters the small intestine through food and water contaminated with it. In amoebiasis, "
  "houseflies act as mechanical carriers and serve to transmit the parasite from the faeces of infected persons to "
  "food and food products. Pneumonia-causing bacteria infect the alveoli (air-filled sacs) of the lungs, whereas the "
  "rhinoviruses of the common cold infect the nose and respiratory passage but not the lungs.",
  ["Statement I: true", "Statement II: false - common cold spares the lungs"],
  "Common Diseases in Humans", ans="C",
  why="Statement II is false because the common cold does not infect the lungs, so options calling it true are "
      "wrong; Statement I is consistent with NCERT, so 'both false' and 'Statement I false' are wrong.", secs=50)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Hepatitis B vaccine is produced from yeast using recombinant DNA technology, which allows its large-scale "
     "production.",
     "Hepatitis B can be transmitted by sharing injection needles and syringes with infected persons."),
  "Recombinant hepatitis B vaccine",
  "NCERT: recombinant DNA technology has allowed the production of antigenic polypeptides of pathogens in bacteria "
  "or yeast, so vaccine production on a large scale became possible; for example, hepatitis B vaccine produced from "
  "yeast. Separately, NCERT notes that hepatitis B (like HIV) is transmitted by sharing infected needles and "
  "syringes. Both are true, but the way the disease spreads has nothing to do with how the vaccine is "
  "manufactured.",
  ["A: true", "R: true", "R concerns transmission, A concerns vaccine production -> not the explanation"],
  "Immunity; Drugs and Alcohol Abuse", ans="B",
  why="The route of transmission does not explain the method of vaccine production, so 'R is the correct "
      "explanation' is wrong; both statements are NCERT's, so options with a false statement are wrong.", secs=40)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("Which of the following statements about innate and acquired immunity are correct according to NCERT?",
     ["Innate immunity is a non-specific type of defence that is present at the time of birth.",
      "Acquired immunity is pathogen-specific and is characterised by memory.",
      "Memory-based acquired immunity evolved in higher vertebrates.",
      "Interferons secreted by virus-infected cells are a part of acquired immunity.",
      "The humoral immune response of B-lymphocytes and the cell-mediated immunity of T-lymphocytes are both "
      "responses of acquired immunity."]),
  "Innate and acquired immunity",
  "NCERT: innate immunity is a non-specific type of defence present at the time of birth, accomplished by physical, "
  "physiological, cellular and cytokine barriers (interferons form the cytokine barrier). Acquired immunity is "
  "pathogen-specific and characterised by memory; memory-based acquired immunity evolved in higher vertebrates. "
  "Within acquired immunity, B-lymphocytes give the humoral (antibody-mediated) immune response and T-lymphocytes "
  "mediate cell-mediated immunity.",
  ["(a), (b), (c), (e): true", "(d): false - interferons are a cytokine barrier of innate immunity"],
  "Immunity",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(a), (b), (c) and (d) only", "(b), (c), (d) and (e) only"],
  why="'(a), (b) and (c) only' omits (e), NCERT's two types of acquired immune response; interferons belong to the "
      "innate cytokine barrier, so any option with (d) is wrong.", secs=60)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("item", "time or duration given in NCERT"),
     ["Recurrence of chill and high fever in malaria", "Symptoms of the common cold",
      "Time-lag between HIV infection and appearance of AIDS symptoms", "Use of tobacco by human beings"],
     ["About 3-7 days", "More than 400 years", "Usually 5-10 years", "Every three to four days"]),
  "Time figures in Human Health and Disease",
  "NCERT: in malaria, haemozoin released from ruptured RBCs is responsible for the chill and high fever recurring "
  "every three to four days. The common cold symptoms usually last for 3-7 days. The time-lag between HIV infection "
  "and appearance of AIDS symptoms may vary from a few months to many years (usually 5-10 years). Tobacco has been "
  "used by human beings for more than 400 years.",
  ["A -> IV", "B -> I", "C -> III", "D -> II"],
  "Common Diseases in Humans; AIDS; Drugs and Alcohol Abuse",
  at="D", match=({"A": "IV", "B": "I", "C": "III", "D": "II"},
                 [{"A": "I", "B": "IV", "C": "III", "D": "II"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="Swapping A and B confuses the 3-4 day fever cycle of malaria with the 3-7 day duration of a cold; the HIV "
      "time-lag is years, not centuries; the last code mismatches three of the four rows.", secs=45)


# ================================================================ Biotechnology: Principles and Processes (6/8/6)
HIND_II_YEAR = 1963 + 5
assert HIND_II_YEAR == 1968
Z(BPP, "Restriction enzymes", B, NUM,
  "In 1963, two enzymes responsible for restricting the growth of bacteriophage in Escherichia coli were isolated. "
  "According to NCERT, the first restriction endonuclease whose functioning depended on a specific DNA nucleotide "
  "sequence, Hind II, was isolated and characterised five years later. In which year was this?",
  "History of restriction enzymes",
  "NCERT: in the year 1963, the two enzymes responsible for restricting the growth of bacteriophage in E. coli were "
  "isolated - one added methyl groups to DNA, the other cut DNA (restriction endonuclease). The first restriction "
  "endonuclease, Hind II, whose functioning depended on a specific DNA nucleotide sequence, was isolated and "
  "characterised five years later.",
  ["1963 + 5 = 1968"],
  "Tools of Recombinant DNA Technology",
  at="A", correct="1968",
  wrong=["1958", "1972", "1963"],
  why="1958 subtracts the five years instead of adding them; 1972 is the year Cohen and Boyer made the first "
      "recombinant DNA; 1963 is the year of the first two restriction-related enzymes.", secs=20, vb=RECOMPUTED)

Z(BPP, "PCR and gel electrophoresis", B, ASR,
  AR("A thermostable DNA polymerase is used in the polymerase chain reaction (PCR).",
     "This thermostable DNA polymerase is isolated from the bacterium Thermus aquaticus."),
  "Thermostable DNA polymerase: use and source",
  "NCERT: the repeated amplification in PCR is achieved by the use of a thermostable DNA polymerase (isolated from a "
  "bacterium, Thermus aquaticus), which remains active during the high temperature induced denaturation of "
  "double-stranded DNA. Both statements are true, but the name of the bacterium the enzyme comes from does not "
  "explain why a thermostable enzyme is needed; the reason is that it must stay active at the high temperature used "
  "for denaturation.",
  ["A: true", "R: true", "R gives the source, not the reason (stability at denaturation temperature)"],
  "Processes of Recombinant DNA Technology", ans="B",
  why="The source organism is not the reason for using a heat-stable enzyme, so 'R is the correct explanation' is "
      "wrong; both are NCERT statements, so options calling either false are wrong.", secs=30)

Z(BPP, "PCR and gel electrophoresis", B, STP,
  SP("During the isolation of DNA from a fungus, the cells are broken open by treating them with chitinase.",
     "During the isolation of DNA from bacteria, the cells are broken open by treating them with cellulase."),
  "Enzymes used to break open cells",
  "NCERT: DNA is enclosed within membranes, so the cell has to be broken open to release DNA along with other "
  "macromolecules. This is done by treating the bacterial cells, plant cells or fungus with enzymes such as "
  "lysozyme (bacteria), cellulase (plant cells) and chitinase (fungus).",
  ["Fungus -> chitinase: Statement I true", "Bacteria -> lysozyme (cellulase is for plant cells): Statement II false"],
  "Processes of Recombinant DNA Technology", ans="C",
  why="Statement II names the plant-cell enzyme for bacteria (lysozyme is used), so options calling it true are "
      "wrong; Statement I is correct, so 'both false' and 'Statement I false' are wrong.", secs=25)

Z(BPP, "Cloning vectors", B, D,
  "The plasmid of Agrobacterium tumefaciens that has been modified into a cloning vector is called the Ti plasmid. "
  "According to NCERT, 'Ti' stands for:",
  "Ti plasmid",
  "NCERT: the tumor inducing (Ti) plasmid of Agrobacterium tumefaciens has now been modified into a cloning vector "
  "which is no more pathogenic to the plants but is still able to use the mechanisms to deliver genes of our "
  "interest into a variety of plants. Agrobacterium is a pathogen of several dicot plants and delivers T-DNA that "
  "transforms normal plant cells into tumour cells.",
  ["Ti = tumour (tumor) inducing"],
  "Tools of Recombinant DNA Technology",
  at="D", correct="Tumour inducing",
  wrong=["Tetracycline inactivating", "Transfer initiating", "Thermus-isolated"],
  why="Tetracycline resistance is a pBR322 marker, not the meaning of 'Ti'; 'transfer initiating' and "
      "'Thermus-isolated' are not NCERT terms.", secs=20)

Z(BPP, "Cloning vectors", B, D,
  "According to NCERT, scientists learnt how to deliver genes to transform eukaryotic cells (and force them to do "
  "what is wanted) from:",
  "Lessons from pathogens for gene delivery",
  "NCERT: we have learnt a lesson or two from bacteria and viruses, which have known for ages how to deliver genes "
  "to transform eukaryotic cells and force them to do what the bacteria or viruses want. Agrobacterium "
  "tumefaciens delivers T-DNA into dicot plant cells, and retroviruses can transform normal animal cells into "
  "cancerous cells; both have been disarmed and used as vectors.",
  ["Gene delivery learnt from bacteria and viruses (pathogens of eukaryotes)"],
  "Tools of Recombinant DNA Technology",
  at="B", correct="Bacteria and viruses, which have known for ages how to deliver genes to transform eukaryotic cells",
  wrong=["Fungi that break down plant cell walls with chitinase", "Chemical carcinogens present in tobacco smoke",
         "Thermophilic bacteria such as Thermus aquaticus"],
  why="NCERT credits pathogenic bacteria (Agrobacterium) and viruses (retroviruses) for the art of gene delivery; "
      "chitinase is used to break fungal cells, carcinogens cause cancer, and Thermus aquaticus is the source of the "
      "PCR polymerase.", secs=25)

Z(BPP, "Restriction enzymes", B, MUL,
  MS("Which of the following are nucleases, as described in NCERT?",
     ["Exonucleases", "Endonucleases", "Restriction enzymes", "DNA ligase", "Thermostable DNA polymerase"]),
  "Nucleases",
  "NCERT: restriction enzymes belong to a larger class of enzymes called nucleases. These are of two kinds: "
  "exonucleases, which remove nucleotides from the ends of the DNA, and endonucleases, which make cuts at specific "
  "positions within the DNA. DNA ligase joins DNA fragments and DNA polymerase synthesises DNA; neither is a "
  "nuclease.",
  ["Nucleases: exonucleases, endonucleases (restriction enzymes belong here)",
   "DNA ligase: joins; DNA polymerase: synthesises"],
  "Tools of Recombinant DNA Technology",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only"],
  why="Restriction enzymes are nucleases, so '(a) and (b) only' is incomplete; DNA ligase and DNA polymerase build "
      "or join DNA rather than cut it, so options with (d) or (e) are wrong.", secs=35)

EC_SITES = 3
EC_BONDS, EC_FRAGS = 2 * EC_SITES, EC_SITES
assert (EC_BONDS, EC_FRAGS) == (6, 3)
Z(BPP, "Restriction enzymes", I, NUM,
  "A circular plasmid has three recognition sites for EcoRI. It is digested completely with EcoRI, which, at each "
  "recognition site, cuts each of the two strands of the double helix once in its sugar-phosphate backbone. How "
  "many phosphodiester bonds are broken in all, and how many DNA fragments are obtained?",
  "Counting cuts made by a restriction enzyme",
  "NCERT: once a restriction endonuclease finds its specific recognition sequence, it binds to the DNA and cuts each "
  "of the two strands of the double helix at specific points in their sugar-phosphate backbones. So each site "
  "breaks 2 phosphodiester bonds. A circular DNA cut at n sites gives n fragments (a linear DNA would give n + 1).",
  ["Bonds broken = 2 per site x 3 sites = 6", "Circular DNA with 3 cuts -> 3 fragments"],
  "Processes of Recombinant DNA Technology",
  at="C", correct="6 bonds; 3 fragments",
  wrong=["3 bonds; 3 fragments", "6 bonds; 4 fragments", "3 bonds; 4 fragments"],
  why="'3 bonds' counts only one strand per site, although both strands are cut; '4 fragments' applies the rule for "
      "a linear DNA (n + 1) to a circular plasmid.", secs=60, vb=RECOMPUTED)

Z(BPP, "Cloning vectors", I, D,
  "A researcher cuts a vector and a source DNA with the same restriction enzyme, EcoRI, and mixes the two, but "
  "forgets to add DNA ligase. Following NCERT's account, which of the following is expected?",
  "Role of DNA ligase",
  "NCERT: restriction enzymes cut each strand a little away from the centre of the palindrome, leaving overhanging "
  "stretches (sticky ends). These form hydrogen bonds with their complementary cut counterparts, and this "
  "stickiness facilitates the action of the enzyme DNA ligase, which joins the ends. Only after the cut gene and "
  "the cut vector are mixed and ligase is added does this result in recombinant DNA.",
  ["Same enzyme -> matching sticky ends -> hydrogen bonding", "Joining into recombinant DNA needs DNA ligase"],
  "Processes of Recombinant DNA Technology",
  at="A",
  correct="The sticky ends can pair by hydrogen bonds, but without ligase the gene is not joined to the vector to "
          "give a recombinant DNA",
  wrong=["A recombinant DNA forms normally, because sticky ends are joined covalently on their own",
         "EcoRI itself joins the cut ends, so ligase is not needed",
         "The ends cannot pair at all, because sticky ends never form hydrogen bonds"],
  why="Sticky ends only hydrogen-bond; joining needs ligase, so the first two options are wrong; NCERT states that "
      "sticky ends do form hydrogen bonds with their counterparts, so the last option is wrong.", secs=45)

Z(BPP, "PCR and gel electrophoresis", I, ASR,
  AR("Agarose gel electrophoresis separates DNA fragments according to their size.",
     "In an agarose gel, the larger DNA fragments move faster and farther than the smaller ones."),
  "Separation by size in agarose gel",
  "NCERT: the cut fragments of DNA are separated by gel electrophoresis; the DNA fragments separate (resolve) "
  "according to their size through the sieving effect provided by the agarose gel. Hence, the smaller the "
  "fragment size, the farther it moves. So A is true and R reverses the direction of the size effect.",
  ["A: true", "R: false - smaller fragments move farther"],
  "Processes of Recombinant DNA Technology", ans="C",
  why="R contradicts NCERT's 'the smaller the fragment size, the farther it moves', so options with R true are wrong; "
      "A is NCERT's statement, so 'A is false' is wrong.", secs=30)

Z(BPP, "Bioreactors and downstream processing", I, STP,
  SP("When a piece of alien DNA is inserted into a cloning vector and transferred into a bacterial, plant or animal "
     "cell, the alien DNA gets multiplied.",
     "Since the ultimate aim is usually to produce a desirable protein, the recombinant DNA has to be expressed, and "
     "the foreign gene gets expressed under appropriate conditions."),
  "Obtaining the foreign gene product",
  "NCERT (Obtaining the Foreign Gene Product): when you insert a piece of alien DNA into a cloning vector and "
  "transfer it into a bacterial, plant or animal cell, the alien DNA gets multiplied. In almost all recombinant "
  "technologies, the ultimate aim is to produce a desirable protein. Hence, there is a need for the recombinant DNA "
  "to be expressed. The foreign gene gets expressed under appropriate conditions.",
  ["Statement I: true", "Statement II: true"],
  "Processes of Recombinant DNA Technology", ans="A",
  why="Both statements are NCERT's own, so every option with a false statement is wrong.", secs=30)

Z(BPP, "Competent hosts and transformation", I, MAT,
  ML(("step in recombinant DNA work", "agent used"),
     ["Breaking open bacterial cells to release DNA", "Precipitating the purified DNA",
      "Joining the gene of interest to the cut vector", "Making bacterial cells competent to take up DNA"],
     ["DNA ligase", "Chilled ethanol", "A divalent cation such as calcium", "Lysozyme"]),
  "Agents used at different steps",
  "NCERT: bacterial cells are broken open with lysozyme; purified DNA ultimately precipitates out after the addition "
  "of chilled ethanol; the cut gene of interest and the cut vector are mixed and ligase is added to give recombinant "
  "DNA; bacterial cells are made competent by treating them with a specific concentration of a divalent cation, "
  "such as calcium.",
  ["A -> IV", "B -> II", "C -> I", "D -> III"],
  "Processes of Recombinant DNA Technology; Tools of Recombinant DNA Technology",
  at="D", match=({"A": "IV", "B": "II", "C": "I", "D": "III"},
                 [{"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="Calcium makes cells competent but does not lyse them, so swapping A and D is wrong; ethanol precipitates DNA "
      "and ligase joins it, so swapping B and C is wrong; the last code mismatches every step.", secs=45)

Z(BPP, "Competent hosts and transformation", I, MUL,
  MS("Which of the following statements are true for BOTH micro-injection and biolistics (gene gun), as described "
     "in NCERT?",
     ["Neither uses a 'disarmed pathogen' vector.",
      "Both are methods of introducing recombinant DNA into host cells.",
      "NCERT describes both as methods for animal cells.",
      "Both use micro-particles of gold or tungsten coated with DNA.",
      "In both, the recombinant DNA is injected directly into the nucleus."]),
  "Micro-injection and biolistics compared",
  "NCERT: in micro-injection, recombinant DNA is directly injected into the nucleus of an animal cell. In another "
  "method, suitable for plants, cells are bombarded with high velocity micro-particles of gold or tungsten coated "
  "with DNA (biolistics or gene gun). The last method uses 'disarmed pathogen' vectors. So both micro-injection and "
  "biolistics introduce rDNA without a pathogen vector; they differ in cell type and procedure.",
  ["(a), (b): true for both", "(c): biolistics is for plants", "(d): only biolistics", "(e): only micro-injection"],
  "Processes of Recombinant DNA Technology",
  at="B", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(b) and (d) only", "(a), (b) and (e) only"],
  why="Biolistics is described as suitable for plants, uses metal micro-particles and does not inject into the "
      "nucleus, while micro-injection uses no particles; so (c), (d) and (e) each hold for only one method.",
  secs=50)

Z(BPP, "PCR and gel electrophoresis", I, D,
  "In NCERT's procedure for isolating DNA, which pair of enzymes is used to REMOVE contaminating macromolecules "
  "from the DNA preparation, rather than to break open the cells?",
  "Purifying DNA",
  "NCERT: the cell is broken open with enzymes such as lysozyme (bacteria), cellulase (plant cells) and chitinase "
  "(fungus). Genes are located on long DNA molecules intertwined with proteins such as histones; RNA can be removed "
  "by treatment with ribonuclease, whereas proteins can be removed by treatment with protease. Other molecules are "
  "removed by appropriate treatments, and purified DNA is precipitated with chilled ethanol.",
  ["Break open cells: lysozyme, cellulase, chitinase", "Remove RNA: ribonuclease; remove proteins: protease"],
  "Processes of Recombinant DNA Technology",
  at="C", correct="Ribonuclease and protease",
  wrong=["Lysozyme and cellulase", "Chitinase and protease", "Ribonuclease and lysozyme"],
  why="Lysozyme, cellulase and chitinase are used to break open bacterial, plant and fungal cells respectively, so "
      "any pair containing one of them is wrong.", secs=30)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("A restriction endonuclease cuts only one of the two strands of DNA at its recognition site.",
     "Once a restriction endonuclease finds its specific recognition sequence, it binds to the DNA."),
  "Action of a restriction endonuclease",
  "NCERT: each restriction endonuclease functions by 'inspecting' the length of a DNA sequence. Once it finds its "
  "specific recognition sequence, it will bind to the DNA and cut each of the two strands of the double helix at "
  "specific points in their sugar-phosphate backbones. So A is false (both strands are cut) and R is true.",
  ["A: false - both strands are cut", "R: true"],
  "Tools of Recombinant DNA Technology", ans="D",
  why="A contradicts NCERT, which says each of the two strands is cut, so all options with A true are wrong; R is "
      "NCERT's statement, so 'A is false but R is true' is correct.", secs=30)

Z(BPP, "Restriction enzymes", A, D,
  "Starting from a bacterial culture, a researcher isolates DNA, cuts it and joins the gene of interest to a vector "
  "following NCERT's procedure. Which option lists the enzymes in the order in which they are used?",
  "Order of enzymes in recombinant DNA work",
  "NCERT: the bacterial cell is first broken open (lysozyme); RNA is removed by ribonuclease (and proteins by "
  "protease) so that the DNA is pure, because DNA must be free from other macromolecules before it can be cut; the "
  "pure DNA is then cut with a restriction enzyme; finally the cut gene of interest and the cut vector are mixed and "
  "DNA ligase is added to give recombinant DNA.",
  ["Lyse cells: lysozyme", "Purify: ribonuclease", "Cut: restriction endonuclease", "Join: DNA ligase"],
  "Processes of Recombinant DNA Technology",
  at="B", correct="Lysozyme -> ribonuclease -> restriction endonuclease -> DNA ligase",
  wrong=["Ribonuclease -> lysozyme -> DNA ligase -> restriction endonuclease",
         "Lysozyme -> restriction endonuclease -> ribonuclease -> DNA ligase",
         "Lysozyme -> ribonuclease -> DNA ligase -> restriction endonuclease"],
  why="The cells must be opened before the DNA can be purified; DNA must be pure before it is cut, so cutting cannot "
      "precede ribonuclease treatment; and the fragments must be cut before ligase can join them.", secs=50)

Z(BPP, "PCR and gel electrophoresis", A, D,
  "In an agarose gel electrophoresis, a student wrongly connects the power supply so that the electrode at the end "
  "of the gel nearer the wells is the POSITIVE electrode (anode). Following NCERT, what will happen to the DNA "
  "loaded in the wells?",
  "Direction of DNA movement in a gel",
  "NCERT: DNA is a negatively charged molecule; hence it moves towards the anode (positive electrode) under an "
  "electric field through the agarose matrix, the fragments separating by size through the sieving effect of the "
  "gel. If the anode is placed at the well end, the DNA will move towards it, i.e. out of the wells away from the "
  "gel, so it will not be resolved in the gel.",
  ["DNA is negatively charged -> moves to the anode", "Anode at the well end -> DNA leaves the wells away from the gel"],
  "Processes of Recombinant DNA Technology",
  at="A",
  correct="The DNA moves towards the electrode next to the wells, away from the gel, so no fragments are resolved in "
          "the gel",
  wrong=["The fragments separate normally, since separation depends only on size",
         "The larger fragments now move farther into the gel than the smaller ones",
         "The DNA stays in the wells, because DNA carries no charge"],
  why="Movement direction depends on DNA's negative charge, so it cannot separate normally with reversed electrodes; "
      "reversing polarity does not reverse the size order inside the gel; DNA is negatively charged, not neutral.",
  secs=50)

Z(BPP, "PCR and gel electrophoresis", A, MUL,
  MS("A researcher amplifies a gene by PCR and then clones it in E. coli. Which of the following statements are "
     "correct according to NCERT?",
     ["The amplified fragment can be used to ligate with a vector for further cloning.",
      "The DNA polymerase used is thermostable, so it remains active during the high temperature of denaturation.",
      "The PCR has to be carried out inside a living host cell.",
      "The primers are small, chemically synthesised oligonucleotides complementary to regions of the template DNA.",
      "The recombinant DNA is introduced into E. coli cells that have been made competent, for example by calcium "
      "treatment followed by heat shock."]),
  "From PCR to cloning",
  "NCERT: in PCR, multiple copies of the gene (or DNA) of interest are synthesised in vitro using two sets of primers "
  "(small chemically synthesised oligonucleotides complementary to regions of the DNA) and DNA polymerase; a "
  "thermostable DNA polymerase (from Thermus aquaticus) remains active during high-temperature denaturation. The "
  "amplified fragment, if desired, can now be used to ligate with a vector for further cloning. The recombinant DNA "
  "is put into competent host cells, e.g. E. coli treated with calcium and given a heat shock.",
  ["(a), (b), (d), (e): true", "(c): false - PCR is done in vitro"],
  "Processes of Recombinant DNA Technology; Tools of Recombinant DNA Technology",
  at="D", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (d) only", "(a), (b), (c) and (d) only", "(b), (c), (d) and (e) only"],
  why="PCR synthesises DNA in vitro, so any option with (c) is wrong; '(a), (b) and (d) only' leaves out the "
      "transformation of competent E. coli, which is how the recombinant DNA enters the host.", secs=60)

Z(BPP, "Cloning vectors", A, STP,
  SP("As used for gene transfer, both the Ti plasmid of Agrobacterium tumefaciens and the retroviruses are in a "
     "disarmed (non-pathogenic) form.",
     "Agrobacterium tumefaciens delivers a piece of DNA (T-DNA) that transforms normal plant cells into tumour cells, "
     "which then produce the chemicals required by the pathogen."),
  "Disarmed pathogen vectors",
  "NCERT: Agrobacterium tumefaciens, a pathogen of several dicot plants, is able to deliver a piece of DNA known as "
  "T-DNA to transform normal plant cells into a tumor and direct these tumor cells to produce the chemicals "
  "required by the pathogen. The tumor inducing (Ti) plasmid has now been modified into a cloning vector which is no "
  "more pathogenic to the plants. Similarly, retroviruses have also been disarmed and are now used to deliver "
  "desirable genes into animal cells.",
  ["Statement I: true (modified Ti plasmid; disarmed retroviruses)", "Statement II: true (wild Agrobacterium)"],
  "Tools of Recombinant DNA Technology", ans="A",
  why="Statement II describes the natural pathogen and Statement I the vectors derived from it; both match NCERT, so "
      "every option with a false statement is wrong.", secs=45)

Z(BPP, "Bioreactors and downstream processing", A, D,
  "An aerobic microbial culture growing in a simple stirred-tank bioreactor is limited by the supply of oxygen. "
  "Which design described in NCERT would most directly improve oxygen transfer to the cells?",
  "Sparged stirred-tank bioreactor",
  "NCERT: the most commonly used bioreactors are of the stirring type. The stirrer facilitates even mixing and "
  "oxygen availability throughout the bioreactor. In a sparged stirred-tank bioreactor, sterile air bubbles are "
  "sparged through the culture; sparging greatly increases the area for oxygen transfer. The foam control system "
  "and sampling ports serve other purposes.",
  ["Sparging sterile air bubbles -> greatly increased area for oxygen transfer"],
  "Processes of Recombinant DNA Technology",
  at="C", correct="A sparged stirred-tank bioreactor, through which sterile air bubbles are sparged",
  wrong=["Adding a foam control system", "Withdrawing more samples through the sampling ports",
         "Shifting the culture to a small-volume laboratory flask"],
  why="Foam control and sampling ports do not increase oxygen transfer; small-volume cultures cannot yield "
      "appreciable quantities of product and do not solve the oxygen limitation.", secs=40)

Z(BPP, "Restriction enzymes", A, D,
  "Which of the following steps in recombinant DNA technology does NOT need a restriction enzyme?",
  "Where restriction enzymes are and are not used",
  "NCERT: restriction enzymes are used to cut the source DNA to release the gene of interest and to cut the vector, "
  "creating matching sticky ends; a vector with a single recognition site is opened (linearised) at that site for "
  "the insert. PCR amplifies a gene in vitro using two sets of primers, DNA polymerase, nucleotides and the template "
  "DNA; no restriction enzyme is needed for amplification.",
  ["Cutting gene, cutting vector, opening the cloning site -> restriction enzyme",
   "PCR amplification -> primers + thermostable DNA polymerase only"],
  "Processes of Recombinant DNA Technology",
  at="D", correct="Amplifying the gene of interest by PCR",
  wrong=["Cutting out the gene of interest from the source DNA",
         "Creating sticky ends on the vector so that the gene can be inserted",
         "Opening a circular plasmid at its single cloning site"],
  why="Each of the other steps is a cut made at a specific recognition sequence, which is exactly what a restriction "
      "endonuclease does.", secs=35)


# ================================================================ Biotechnology and its Applications (5/7/5)
Z(BTA, "Bt crops and RNAi", B, D,
  "According to NCERT, the three critical research areas of biotechnology are:",
  "Critical research areas of biotechnology",
  "NCERT: biotechnology deals with (i) providing the best catalyst in the form of an improved organism, usually a "
  "microbe, or a pure enzyme; (ii) creating optimal conditions through engineering for a catalyst to act; and (iii) "
  "downstream processing technologies to purify the protein/organic compound.",
  ["Best catalyst", "Optimal conditions through engineering", "Downstream processing"],
  "Biotechnology and its Applications (introduction)",
  at="C",
  correct="Providing the best catalyst (an improved organism or a pure enzyme), creating optimal conditions for the "
          "catalyst to act through engineering, and downstream processing technologies to purify the product",
  wrong=["Agro-chemical based agriculture, organic agriculture and genetically engineered crop-based agriculture",
         "Therapeutics, diagnostics and genetically modified crops",
         "Isolation of DNA, cutting of DNA and amplification of DNA by PCR"],
  why="The first wrong option lists NCERT's three options for increasing food production; the second lists some "
      "areas where biotechnology is applied; the third lists steps of recombinant DNA technology.", secs=30)

Z(BTA, "Bt crops and RNAi", B, STP,
  SP("Some strains of Bacillus thuringiensis produce proteins that kill coleopterans, such as flies and mosquitoes.",
     "The lepidopterans named by NCERT as killed by some Bt proteins are the tobacco budworm and the armyworm."),
  "Insect groups killed by Bt proteins",
  "NCERT: some strains of Bacillus thuringiensis produce proteins that kill certain insects such as lepidopterans "
  "(tobacco budworm, armyworm), coleopterans (beetles) and dipterans (flies, mosquitoes). Flies and mosquitoes are "
  "dipterans, not coleopterans.",
  ["Statement I: false - coleopterans are beetles; flies and mosquitoes are dipterans", "Statement II: true"],
  "Biotechnological Applications in Agriculture", ans="D",
  why="Statement I gives the dipteran examples to the coleopterans, so options calling it true are wrong; Statement II "
      "is NCERT's own example, so 'both false' is wrong.", secs=30)

Z(BTA, "Bt crops and RNAi", B, ASR,
  AR("The Green Revolution succeeded in tripling the food supply.",
     "Several nematodes parasitise a wide variety of plants and animals, including human beings."),
  "Green Revolution and parasitic nematodes",
  "NCERT: although the Green Revolution succeeded in tripling the food supply, it was not enough to feed the growing "
  "human population; the increased yields were partly due to improved crop varieties but mainly due to better "
  "management practices and the use of agrochemicals. In a separate context (pest-resistant plants), NCERT notes "
  "that several nematodes parasitise a wide variety of plants and animals, including human beings, which leads to "
  "the RNAi example in tobacco. Both statements are true, but the parasitic habit of nematodes has nothing to do with "
  "the increase in food supply.",
  ["A: true", "R: true", "R is about nematode parasites; A is about food supply -> not the explanation"],
  "Biotechnological Applications in Agriculture", ans="B",
  why="Nematode parasitism cannot explain a rise in food supply, so 'R is the correct explanation' is wrong; both "
      "statements are NCERT's, so options calling either false are wrong.", secs=30)

Z(BTA, "Bt crops and RNAi", B, MAT,
  ML(("stage of the Bt toxin", "where or how it happens, as described in NCERT"),
     ["Toxin present as an inactive protoxin", "Solubilisation of the crystals and activation of the toxin",
      "Binding of the activated toxin", "Creation of pores by the bound toxin"],
     ["In the insect gut, due to its alkaline pH", "Causes swelling and lysis of the cells, eventually killing the insect",
      "Inside the bacterium Bacillus thuringiensis", "To the surface of the midgut epithelial cells"]),
  "How the Bt toxin acts",
  "NCERT: the Bt toxin protein exists as an inactive protoxin in the bacterium, but once an insect ingests it, it is "
  "converted into an active form of toxin due to the alkaline pH of the gut, which solubilises the crystals. The "
  "activated toxin binds to the surface of midgut epithelial cells and creates pores that cause cell swelling and "
  "lysis and eventually cause death of the insect.",
  ["A -> III", "B -> I", "C -> IV", "D -> II"],
  "Biotechnological Applications in Agriculture",
  at="A", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The protoxin is inactive inside the bacterium and is activated only in the insect gut, so swapping A and B is "
      "wrong; the toxin first binds to midgut cells and the pores then cause lysis, so swapping C and D is wrong; the "
      "last code mismatches every stage.", secs=35)

Z(BTA, "Bt crops and RNAi", B, D,
  "According to NCERT, when does Bacillus thuringiensis form the protein crystals that contain the toxic "
  "insecticidal protein?",
  "Formation of Bt toxin crystals",
  "NCERT: Bacillus thuringiensis forms protein crystals during a particular phase of their growth. These crystals "
  "contain a toxic insecticidal protein, which exists as an inactive protoxin in the bacterium.",
  ["Crystals formed during a particular phase of growth of the bacterium"],
  "Biotechnological Applications in Agriculture",
  at="B", correct="During a particular phase of their growth",
  wrong=["Only after they are ingested by an insect", "Only after the cry gene is transferred into a plant",
         "Throughout their life, at every stage of growth"],
  why="The crystals are formed by the bacterium itself during one phase of growth; in the insect gut they are only "
      "solubilised and activated, not formed; plants expressing cry genes are a later human use, not where the "
      "bacterium forms crystals.", secs=25)

Z(BTA, "Transgenic animals", I, D,
  "How many of the following does NCERT list as areas in which biotechnology has been applied?\n\n"
  "Therapeutics, diagnostics, genetically modified crops for agriculture, processed food, bioremediation, waste "
  "treatment, energy production, geological surveying, space research",
  "Areas of application of biotechnology",
  "NCERT: biotechnology has many useful applications for mankind, mainly in therapeutics, diagnostics, genetically "
  "modified crops for agriculture, processed food, bioremediation, waste treatment, and energy production. Geological "
  "surveying and space research are not among them.",
  ["Listed: therapeutics, diagnostics, GM crops, processed food, bioremediation, waste treatment, energy production = 7",
   "Not listed: geological surveying, space research"],
  "Biotechnology and its Applications (introduction)",
  at="A", correct="Seven",
  wrong=["Six", "Eight", "Five"],
  why="Six or five leave out NCERT areas such as bioremediation or energy production; eight adds geological surveying "
      "or space research, which NCERT does not list.", secs=40)

Z(BTA, "Biosafety, biopiracy and patents", I, STP,
  SP("NCERT notes a growing public anger that certain companies are being granted patents for products and "
     "technologies that make use of genetic materials, plants and other biological resources long identified, "
     "developed and used by farmers and indigenous people of a specific region or country.",
     "According to NCERT, the manipulation of living organisms by the human race can go on further without any "
     "regulation."),
  "Ethics and regulation of biotechnology",
  "NCERT (Ethical Issues): the manipulation of living organisms by the human race cannot go on any further without "
  "regulation; some ethical standards are required to evaluate the morality of all human activities that might help "
  "or harm living organisms. NCERT also notes the growing public anger that certain companies are being granted "
  "patents for products and technologies that use genetic materials, plants and other biological resources long "
  "identified, developed and used by farmers and indigenous people of a specific region/country.",
  ["Statement I: true", "Statement II: false - NCERT says it cannot go on without regulation"],
  "Ethical Issues", ans="C",
  why="Statement II reverses NCERT's position, so options calling it true are wrong; Statement I is NCERT's own "
      "observation, so 'both false' and 'Statement I false' are wrong.", secs=40)

Z(BTA, "Bt crops and RNAi", I, MUL,
  MS("Which of the following statements about the cry genes are correct according to NCERT?",
     ["The genes that code for the Bt toxin protein are named cry.",
      "The proteins encoded by the genes cryIAc and cryIIAb control the cotton bollworms.",
      "The protein encoded by cryIAb controls the corn borer.",
      "The cry genes are taken from Agrobacterium tumefaciens.",
      "The cry genes protect the plant by producing double-stranded RNA in it."]),
  "cry genes",
  "NCERT: the Bt toxin is coded by genes named cry. There are a number of them; for example, the proteins "
  "encoded by the genes cryIAc and cryIIAb control the cotton bollworms, and that of cryIAb controls the corn borer. "
  "The cry genes come from Bacillus thuringiensis and code for an insecticidal protein; protection by dsRNA is the "
  "RNAi strategy used in tobacco against a nematode.",
  ["(a), (b), (c): true", "(d): false - from Bacillus thuringiensis", "(e): false - they code for a protein toxin"],
  "Biotechnological Applications in Agriculture",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"],
  why="'(a) and (b) only' leaves out cryIAb against the corn borer; Agrobacterium is a vector source, not the source "
      "of cry genes, and dsRNA belongs to the RNAi strategy, so options with (d) or (e) are wrong.", secs=45)

Z(BTA, "Transgenic animals", I, ASR,
  AR("Transgenic models exist for many human diseases, such as cancer, cystic fibrosis, rheumatoid arthritis and "
     "Alzheimer's.",
     "The milk of the transgenic cow Rosie contained human alpha-lactalbumin."),
  "Transgenic disease models",
  "NCERT: many transgenic animals are specifically designed to increase our understanding of how genes contribute to "
  "the development of disease, so that investigation of new treatments is made possible; transgenic models exist "
  "for many human diseases such as cancer, cystic fibrosis, rheumatoid arthritis and Alzheimer's. Separately, Rosie "
  "produced milk containing human alpha-lactalbumin. Both are true, but Rosie's milk has nothing to do with disease "
  "models.",
  ["A: true", "R: true", "R is about a biological product, A about disease models -> not the explanation"],
  "Transgenic Animals", ans="B",
  why="A biological product in a cow's milk cannot explain why disease models exist, so 'R is the correct "
      "explanation' is wrong; both statements are NCERT's, so options calling either false are wrong.", secs=30)

Z(BTA, "Bt crops and RNAi", I, D,
  "How many of the following does NCERT list as ways in which genetic modification (GM) has been useful in crop "
  "plants?\n\nTolerance to abiotic stresses (cold, drought, salt, heat); reduced reliance on chemical pesticides; "
  "reduced post-harvest losses; increased efficiency of mineral usage by plants; enhanced nutritional value of food; "
  "increased reliance on chemical fertilisers; increased reliance on chemical pesticides",
  "Uses of genetically modified crops",
  "NCERT: genetic modification has (i) made crops more tolerant to abiotic stresses (cold, drought, salt, heat); "
  "(ii) reduced reliance on chemical pesticides (pest-resistant crops); (iii) helped to reduce post-harvest losses; "
  "(iv) increased efficiency of mineral usage by plants, which prevents early exhaustion of fertility of the soil; "
  "and (v) enhanced nutritional value of food, e.g. golden rice. Increased reliance on agrochemicals is the opposite "
  "of what GM crops aim at.",
  ["Listed: 5", "Not listed: increased reliance on fertilisers or pesticides"],
  "Biotechnological Applications in Agriculture",
  at="B", correct="Five",
  wrong=["Four", "Six", "Seven"],
  why="Four omits one of NCERT's five uses; six or seven count increased reliance on agrochemicals, which GM crops "
      "are meant to reduce.", secs=45)

Z(BTA, "Human insulin", I, MAT,
  ML(("feature of insulin production", "NCERT detail"),
     ["Number of polypeptide chains in mature insulin", "Bonds that link the chains",
      "Extra stretch present in the pro-hormone but not in mature insulin",
      "Organism into whose plasmids Eli Lilly introduced the DNA sequences for chains A and B"],
     ["E. coli", "C peptide", "Disulphide bridges", "Two (chain A and chain B)"]),
  "Genetically engineered insulin",
  "NCERT: mature insulin consists of two short polypeptide chains, chain A and chain B, linked together by "
  "disulphide bridges. In mammals, insulin is synthesised as a pro-hormone containing an extra stretch called the C "
  "peptide, which is removed during maturation. In 1983, Eli Lilly prepared two DNA sequences corresponding to "
  "chains A and B of human insulin and introduced them into plasmids of E. coli to produce insulin chains.",
  ["A -> IV", "B -> III", "C -> II", "D -> I"],
  "Biotechnological Applications in Medicine",
  at="A", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "I", "B": "III", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The C peptide is removed, not a link between the chains, so swapping B and C is wrong; E. coli is the host, "
      "not a number of chains; the last code makes E. coli the extra stretch.", secs=40)

Z(BTA, "Bt crops and RNAi", I, ASR,
  AR("In RNA interference, a single-stranded sense RNA by itself silences the target mRNA.",
     "RNAi involves the silencing of a specific mRNA by a complementary dsRNA molecule that binds to and prevents "
     "translation of the mRNA."),
  "Molecule that silences mRNA in RNAi",
  "NCERT: RNAi involves silencing of a specific mRNA due to a complementary dsRNA molecule that binds to and "
  "prevents translation of the mRNA (silencing). In the tobacco example, the introduced DNA produced both sense and "
  "anti-sense RNA, which, being complementary, formed dsRNA that initiated RNAi. So A is false and R is true.",
  ["A: false - silencing is by a complementary dsRNA", "R: true"],
  "Biotechnological Applications in Agriculture", ans="D",
  why="NCERT attributes silencing to dsRNA, not to a single sense strand, so options with A true are wrong; R is "
      "NCERT's definition, so 'A is false but R is true' is correct.", secs=35)

Z(BTA, "Transgenic animals", A, MUL,
  MS("Which of the following statements about products obtained, or being sought, through genetic engineering are "
     "correct according to NCERT?",
     ["The milk of the transgenic cow Rosie contained human alpha-lactalbumin, at 2.4 grams per litre.",
      "Attempts are being made to use transgenic animals for the treatment of phenylketonuria (PKU) and cystic "
      "fibrosis.",
      "Human protein (alpha-1-antitrypsin) produced using transgenic animals is used to treat emphysema.",
      "Rosie was a transgenic sheep.",
      "Golden rice is enriched in vitamin A."]),
  "Products of genetic engineering",
  "NCERT: transgenic animals have been used to produce human protein (alpha-1-antitrypsin) used to treat emphysema, "
  "and similar attempts are being made for the treatment of phenylketonuria (PKU) and cystic fibrosis. In 1997, the "
  "first transgenic cow, Rosie, produced human protein-enriched milk (2.4 grams per litre) containing human "
  "alpha-lactalbumin. Golden rice, a GM crop, is vitamin A enriched rice.",
  ["(a), (b), (c), (e): true", "(d): false - Rosie was a cow"],
  "Transgenic Animals; Biotechnological Applications in Agriculture",
  at="A", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (c), (d) and (e) only"],
  why="Rosie was the first transgenic cow, so any option with (d) is wrong; '(a), (b) and (c) only' leaves out golden "
      "rice, which NCERT describes as vitamin A enriched.", secs=60)

Z(BTA, "Human insulin", A, D,
  "In which pair of NCERT examples were DNA sequences coding for a HUMAN protein expressed in a non-human organism?",
  "Human genes in non-human hosts",
  "NCERT: Eli Lilly prepared two DNA sequences corresponding to chains A and B of human insulin and introduced them "
  "into plasmids of E. coli to produce insulin chains. The transgenic cow Rosie produced milk containing the human "
  "protein alpha-lactalbumin; transgenic animals producing useful products are created by introducing the portion of "
  "DNA (genes) which codes for that product. In Bt cotton and Bt corn the introduced genes are bacterial (cry genes "
  "of Bacillus thuringiensis), and in the RNAi tobacco they are nematode-specific genes.",
  ["Eli Lilly: human insulin chain DNA in E. coli", "Rosie: human alpha-lactalbumin in a cow",
   "Bt crops: bacterial genes; RNAi tobacco: nematode genes"],
  "Biotechnological Applications in Medicine; Transgenic Animals",
  at="B", correct="The transgenic cow Rosie, and Eli Lilly's production of insulin",
  wrong=["Bt cotton, and the RNAi-protected tobacco", "Bt cotton, and Bt corn",
         "The RNAi-protected tobacco, and Eli Lilly's production of insulin"],
  why="Bt crops carry genes from a bacterium and the RNAi tobacco carries genes from the nematode, so any pair "
      "containing them does not involve human protein-coding DNA in both examples.", secs=50)

Z(BTA, "Gene therapy", A, STP,
  SP("Eli Lilly prepared the DNA sequences for chains A and B of human insulin (1983) several years before the first "
     "clinical gene therapy was given (1990).",
     "The first clinical gene therapy was given to an adult suffering from diabetes."),
  "Chronology and the first gene therapy",
  "NCERT: in 1983, Eli Lilly prepared two DNA sequences corresponding to chains A and B of human insulin. The first "
  "clinical gene therapy was given in 1990 to a 4-year-old girl with adenosine deaminase (ADA) deficiency, an enzyme "
  "crucial for the immune system to function. So 1983 precedes 1990 by seven years, and the patient was a child with "
  "ADA deficiency, not an adult with diabetes.",
  ["1983 < 1990 -> Statement I true", "4-year-old girl, ADA deficiency -> Statement II false"],
  "Biotechnological Applications in Medicine", ans="C",
  why="Statement II misstates both the patient and the disease, so options calling it true are wrong; Statement I "
      "follows from NCERT's dates, so 'both false' and 'Statement I false' are wrong.", secs=40)

Z(BTA, "Transgenic animals", A, MUL,
  MS("Which of the following statements about the uses of transgenic animals are correct according to NCERT?",
     ["Animals made more sensitive to toxic substances than non-transgenic animals give the results of toxicity "
      "testing in less time.",
      "Transgenic mice being developed to test the safety of the polio vaccine could, if successful, replace the use "
      "of monkeys for testing the safety of batches of the vaccine.",
      "Altering the formation of insulin-like growth factor in transgenic animals is used to learn its biological "
      "role.",
      "Transgenic animals designed as models for a disease make the investigation of new treatments possible.",
      "Transgenic mice being developed for polio vaccine testing would replace the use of rabbits."]),
  "Uses of transgenic animals",
  "NCERT: in chemical safety (toxicity) testing, transgenic animals carrying genes that make them more sensitive to "
  "toxic substances are exposed to the substances and their effects studied, giving results in less time. Transgenic "
  "mice are being developed for use in testing the safety of vaccines before they are used on humans; transgenic "
  "mice are being used to test the safety of the polio vaccine and, if successful, could replace the use of monkeys. "
  "Information on the biological role of insulin-like growth factor is obtained by altering its formation in "
  "transgenic animals (normal physiology and development). Many transgenic animals serve as models for human "
  "diseases so that investigation of new treatments is made possible.",
  ["(a), (b), (c), (d): true", "(e): false - NCERT names monkeys, not rabbits"],
  "Transgenic Animals",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(a), (b), (c), (d) and (e)", "(b), (c) and (e) only"],
  why="NCERT says the transgenic mice could replace monkeys, so any option with (e) is wrong; '(a), (b) and (c) "
      "only' leaves out the disease-model use, which NCERT states.", secs=60)

Z(BTA, "Gene therapy", A, ASR,
  AR("Gene therapy is a collection of methods that allows correction of a gene defect that has been diagnosed in a "
     "child or embryo.",
     "In gene therapy, the defective gene is always cut out and removed before a normal gene is delivered."),
  "What gene therapy does",
  "NCERT: gene therapy is a collection of methods that allows correction of a gene defect that has been diagnosed in "
  "a child/embryo. Here genes are inserted into a person's cells and tissues to treat a disease. Correction of a "
  "genetic defect involves delivery of a normal gene into the individual or embryo to take over the function of and "
  "compensate for the non-functional gene. Removal of the defective gene is not part of NCERT's description, so R "
  "is false.",
  ["A: true", "R: false - the normal gene compensates; the defective gene is not removed"],
  "Biotechnological Applications in Medicine", ans="C",
  why="NCERT says the delivered normal gene compensates for the non-functional gene, so R is false and the options "
      "with R true are wrong; A is NCERT's definition, so 'A is false' is wrong.", secs=40)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 119
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "ZOO_010_p2: 119 original Zoology questions (Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers and computed match/count keys re-derived in tools/batch_010/ZOO_010_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
