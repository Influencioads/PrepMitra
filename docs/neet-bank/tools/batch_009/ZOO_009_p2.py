"""Builder for package ZOO_009_p2 of BATCH_009 (Zoology, 131 questions, NEET_ZOO_002120..NEET_ZOO_002250).

Topics: Neural Control and Coordination, Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_009/ZOO_009_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_009_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_009_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_009_ZOO_p2.json"
FIRST_ID = 2120

CHECKED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

NCC = "Neural Control and Coordination"
CCI = "Chemical Coordination and Integration"
HR = "Human Reproduction"
RH = "Reproductive Health"
EVO = "Evolution"
HHD = "Human Health and Disease"
BPP = "Biotechnology: Principles and Processes"
BTA = "Biotechnology and its Applications"

REF = {
    NCC: "Class 11 Biology, Ch 18 'Neural Control and Coordination'",
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



# ================================================================ Neural Control and Coordination (4/6/4)
Z(NCC, "Nervous system divisions", B, D,
  "Which of the following parts of the human brain belongs to the hindbrain but is NOT a part of the brain stem?",
  "Hindbrain versus brain stem",
  "NCERT: the hindbrain comprises the pons, cerebellum and medulla oblongata. The midbrain, pons and medulla "
  "oblongata together form the brain stem. The cerebellum is therefore in the hindbrain but outside the brain "
  "stem.",
  ["Hindbrain = pons + cerebellum + medulla oblongata", "Brain stem = midbrain + pons + medulla oblongata",
   "Common to the hindbrain only: cerebellum"],
  "Central Neural System",
  at="A", correct="Cerebellum",
  wrong=["Pons", "Medulla oblongata", "Corpora quadrigemina"],
  why="The pons and the medulla oblongata are in the hindbrain and are also parts of the brain stem; the corpora "
      "quadrigemina are on the dorsal side of the midbrain, so they are in the brain stem but not in the "
      "hindbrain.", secs=25)

Z(NCC, "Neuron and nerves", B, D,
  "NCERT classifies neurons into multipolar, bipolar and unipolar types. On what basis is this classification "
  "made?",
  "Types of neurons",
  "NCERT: based on the number of axon and dendrites, the neurons are divided into three types: multipolar (one "
  "axon and two or more dendrites), bipolar (one axon and one dendrite) and unipolar (cell body with one axon "
  "only).",
  ["Multipolar: 1 axon, 2 or more dendrites", "Bipolar: 1 axon, 1 dendrite", "Unipolar: cell body with 1 axon only",
   "-> basis = number of axon and dendrites"],
  "Neuron as Structural and Functional Unit of Neural System",
  at="C", correct="The number of axon and dendrites",
  wrong=["Whether the axon is myelinated or unmyelinated", "The direction in which the neuron carries impulses",
         "The number of synaptic knobs at the end of the axon"],
  why="Myelination is the basis for classing nerve fibres (myelinated and unmyelinated), not neurons into "
      "multipolar, bipolar and unipolar; direction of conduction is the basis for afferent and efferent fibres; "
      "NCERT does not class neurons by the number of synaptic knobs.", secs=25)

Z(NCC, "Neuron and nerves", B, STP,
  SP("Like the cell body, the dendrites of a neuron contain Nissl's granules.",
     "The axon of a neuron transmits nerve impulses towards the cell body."),
  "Dendrites and axon compared",
  "NCERT: short fibres which branch repeatedly and project out of the cell body also contain Nissl's granules "
  "and are called dendrites; these fibres transmit impulses towards the cell body. The axon is a long fibre that "
  "transmits nerve impulses away from the cell body to a synapse or to a neuromuscular junction.",
  ["Statement I: true - dendrites also contain Nissl's granules",
   "Statement II: false - the axon carries impulses away from the cell body"],
  "Neuron as Structural and Functional Unit of Neural System", ans="C",
  why="Statement II gives the dendrites' direction of conduction to the axon, so options calling it true are "
      "wrong; Statement I is NCERT's description of dendrites, so options calling it false are wrong.", secs=30)

Z(NCC, "Nervous system divisions", B, ASR,
  AR("The human brain is well protected.",
     "The brain is enclosed in the skull, and inside the skull it is covered by the cranial meninges."),
  "Protection of the brain",
  "NCERT: the human brain is well protected by the skull. Inside the skull, the brain is covered by cranial "
  "meninges consisting of an outer layer called dura mater, a very thin middle layer called arachnoid and an inner "
  "layer (which is in contact with the brain tissue) called pia mater. The skull and the meninges are the very "
  "structures that protect it, so R explains A.",
  ["A: true", "R: true - skull and cranial meninges", "R is the reason A holds"],
  "Central Neural System", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R names the coverings that "
      "give the protection stated in A, so it is the correct explanation.", secs=25)

Z(NCC, "Nervous system divisions", I, MAT,
  ML(("function", "part of the brain mainly involved"),
     ["Control of body temperature and of the urge for eating and drinking",
      "Control of gastric secretions",
      "Fibre tracts that interconnect different regions of the brain",
      "Regulation of sexual behaviour and motivation, along with the hypothalamus"],
     ["Pons", "Limbic system", "Hypothalamus", "Medulla oblongata"]),
  "Localisation of brain functions",
  "NCERT: the hypothalamus contains a number of centres which control body temperature and the urge for eating "
  "and drinking. The medulla contains centres which control respiration, cardiovascular reflexes and gastric "
  "secretions. The pons consists of fibre tracts that interconnect different regions of the brain. The limbic "
  "system, along with the hypothalamus, is involved in the regulation of sexual behaviour, expression of emotional "
  "reactions and motivation.",
  ["A -> hypothalamus (III)", "B -> medulla oblongata (IV)", "C -> pons (I)", "D -> limbic system (II)"],
  "Central Neural System",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="Giving temperature control to the medulla and gastric secretions to the hypothalamus reverses them; the pons, "
      "not the medulla, consists of interconnecting fibre tracts; and sexual behaviour and motivation are limbic "
      "functions, while temperature and the urge for eating and drinking are hypothalamic centres.", secs=50)

Z(NCC, "Neuron and nerves", I, MUL,
  MS("Which of the following statements correctly describe the axon of a neuron, as given in NCERT?",
     ["It is a long fibre whose distal end is branched.",
      "Each of its branches terminates as a bulb-like structure called the synaptic knob.",
      "It transmits nerve impulses towards the cell body.",
      "Axons are of two types, myelinated and non-myelinated.",
      "It transmits nerve impulses to a synapse or to a neuromuscular junction."]),
  "Structure and role of the axon",
  "NCERT: the axon is a long fibre, the distal end of which is branched. Each branch terminates as a bulb-like "
  "structure called the synaptic knob, which possesses synaptic vesicles containing neurotransmitters. Axons "
  "transmit nerve impulses away from the cell body to a synapse or to a neuromuscular junction. There are two "
  "types of axons, namely myelinated and non-myelinated. Conduction towards the cell body is the role of the "
  "dendrites.",
  ["(a) true", "(b) true", "(c) false - that is the dendrites", "(d) true", "(e) true"],
  "Neuron as Structural and Functional Unit of Neural System",
  at="D", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (c) only", "(a), (b), (c), (d) and (e)", "(b), (d) and (e) only"],
  why="(c) describes dendrites, so every option containing (c) is wrong; '(b), (d) and (e) only' leaves out (a), "
      "NCERT's description of the axon as a long fibre with a branched distal end.", secs=50)

Z(NCC, "Nervous system divisions", I, D,
  "According to NCERT, which of the following is among the functions controlled by the human brain?",
  "Functions of the brain",
  "NCERT lists that the brain controls the voluntary movements, balance of the body, functioning of vital "
  "involuntary organs (e.g. lungs, heart, kidneys, etc.), thermoregulation, hunger and thirst, circadian (24-hour) "
  "rhythms of our body, activities of several endocrine glands and human behaviour. It is also the site for "
  "processing of vision, hearing, speech, memory, intelligence, emotions and thoughts.",
  ["Brain = 'command and control system'", "Controls voluntary AND vital involuntary organs (lungs, heart, kidneys)"],
  "Central Neural System",
  at="B", correct="The functioning of vital involuntary organs such as the lungs, heart and kidneys",
  wrong=["Only voluntary movements; involuntary organs are controlled by the spinal cord alone",
         "Only the processing of vision and hearing; memory and emotions are handled by the PNS",
         "Only the activities of endocrine glands, not human behaviour"],
  why="NCERT names both voluntary movements and the functioning of vital involuntary organs as brain functions, "
      "puts memory and emotions among processes of the brain (the PNS carries impulses, it does not process them), "
      "and lists human behaviour as well as endocrine activity.", secs=35)

Z(NCC, "Nerve impulse generation and conduction", I, ASR,
  AR("Within a fraction of a second after a site on an axon is stimulated, the resting potential is restored at "
     "that site.",
     "The rise in Na⁺ permeability at the site is extremely short-lived and is quickly followed by a rise in "
     "permeability to K⁺, so that K⁺ diffuses to the outside of the membrane."),
  "Restoring the resting potential",
  "NCERT: the rise in the stimulus-induced permeability to Na⁺ is extremely short-lived. It is quickly followed by "
  "a rise in permeability to K⁺. Within a fraction of a second, K⁺ diffuses outside the membrane and restores "
  "the resting potential of the membrane at the site of excitation, and the fibre becomes once more responsive to "
  "further stimulation. The events in R are what restore the resting potential, so R explains A.",
  ["A: true", "R: true", "Short-lived Na⁺ rise + K⁺ outflow -> resting potential restored"],
  "Generation and Conduction of Nerve Impulse", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT presents the outward "
      "diffusion of K⁺ after the brief Na⁺ rise as the process that restores the resting potential, so R "
      "explains A.", secs=40)

Z(NCC, "Nervous system divisions", I, STP,
  SP("The cerebral hemispheres are connected by a tract of nerve fibres called the corpus callosum, and the "
     "cerebrum wraps around the thalamus.",
     "The midbrain is located between the thalamus/hypothalamus of the forebrain and the medulla oblongata, with "
     "no other part of the hindbrain in between."),
  "Position of brain parts",
  "NCERT: the cerebral hemispheres are connected by a tract of nerve fibres called the corpus callosum, and the "
  "cerebrum wraps around a structure called the thalamus. The midbrain is located between the thalamus/"
  "hypothalamus of the forebrain and the pons of the hindbrain; the medulla lies below the pons and is connected "
  "to the spinal cord.",
  ["Statement I: true", "Statement II: false - the midbrain borders the pons, not the medulla directly"],
  "Central Neural System", ans="C",
  why="Statement II replaces the pons with the medulla oblongata, so options calling it true are wrong; Statement "
      "I is NCERT's description of the cerebrum.", secs=40)

Z(NCC, "Nerve impulse generation and conduction", I, D,
  "At a chemical synapse, neurotransmitters bind to their specific receptors on the post-synaptic membrane. What, "
  "according to NCERT, is the immediate result of this binding?",
  "Post-synaptic events",
  "NCERT: the released neurotransmitters bind to their specific receptors present on the post-synaptic membrane. "
  "This binding opens ion channels, allowing the entry of ions which can generate a new potential in the "
  "post-synaptic neuron. The new potential developed may be either excitatory or inhibitory.",
  ["Binding to receptors -> ion channels open", "Ions enter -> new potential (excitatory or inhibitory)"],
  "Transmission of Impulses",
  at="D", correct="Ion channels open, allowing entry of ions that can generate a new potential in the "
                  "post-synaptic neuron",
  wrong=["Synaptic vesicles of the post-synaptic neuron fuse with its membrane",
         "Electrical current flows directly from the pre-synaptic into the post-synaptic neuron",
         "The post-synaptic membrane becomes permanently impermeable to all ions"],
  why="Synaptic vesicles are in the pre-synaptic knob, not the post-synaptic neuron; direct current flow happens "
      "at electrical synapses, which have no neurotransmitters; and the binding opens channels rather than closing "
      "the membrane to all ions.", secs=35)

Z(NCC, "Nerve impulse generation and conduction", A, MUL,
  MS("An axon is at rest. Which of the following are TRUE of it, according to NCERT?",
     ["The axonal membrane is nearly impermeable to Na⁺.",
      "The axonal membrane is impermeable to the negatively charged proteins present in the axoplasm.",
      "The outer surface of the axonal membrane is negatively charged.",
      "The concentration of K⁺ is higher in the axoplasm than in the fluid outside.",
      "The membrane is in a depolarised state."]),
  "The resting axonal membrane",
  "NCERT: when a neuron is not conducting any impulse, i.e. resting, the axonal membrane is comparatively more "
  "permeable to K⁺ and nearly impermeable to Na⁺; it is also impermeable to the negatively charged proteins "
  "present in the axoplasm. The axoplasm contains a high concentration of K⁺ and negatively charged proteins and a "
  "low concentration of Na⁺. The outer surface carries a positive charge and the inner surface a negative charge, "
  "so the membrane is POLARISED; a depolarised membrane is found only at a stimulated site.",
  ["(a) true", "(b) true", "(c) false - outer surface positive", "(d) true", "(e) false - polarised, not "
   "depolarised"],
  "Generation and Conduction of Nerve Impulse",
  at="A", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (e) only", "(a), (b), (d) and (e) only", "(b), (c) and (d) only"],
  why="(c) reverses the resting charges and (e) describes a stimulated site, so options with either are wrong; "
      "the remaining statements (a), (b) and (d) are all NCERT facts about the resting state.", secs=60)

Z(NCC, "Neuron and nerves", A, MAT,
  ML(("feature", "neural structure"),
     ["Has one axon and one dendrite",
      "Gap between two adjacent myelin sheaths",
      "Enclosed by a Schwann cell that does not form a myelin sheath around the axon",
      "Granular bodies present in the cell body and dendrites"],
     ["Unmyelinated nerve fibre", "Nissl's granules", "Bipolar neuron", "Node of Ranvier"]),
  "Neuron and nerve-fibre features",
  "NCERT: bipolar neurons have one axon and one dendrite (found in the retina). In myelinated fibres, the gaps "
  "between two adjacent myelin sheaths are called nodes of Ranvier. An unmyelinated nerve fibre is enclosed by a "
  "Schwann cell that does not form a myelin sheath around the axon. Nissl's granules are certain granular bodies "
  "in the cytoplasm of the cell body, also present in the dendrites.",
  ["A -> bipolar neuron (III)", "B -> node of Ranvier (IV)", "C -> unmyelinated fibre (I)",
   "D -> Nissl's granules (II)"],
  "Neuron as Structural and Functional Unit of Neural System",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="A node of Ranvier is a gap between myelin sheaths, not a fibre wrapped by a non-myelinating Schwann cell; "
      "Nissl's granules are granular bodies, not a type of neuron; and a bipolar neuron is a neuron, not an "
      "unmyelinated fibre.", secs=50)

Z(NCC, "Nerve impulse generation and conduction", A, ASR,
  AR("An electrical synapse can transmit an impulse even though no neurotransmitter is released across it.",
     "At an electrical synapse, the pre- and post-synaptic membranes are separated by a fluid-filled synaptic "
     "cleft."),
  "Electrical versus chemical synapse",
  "NCERT: at electrical synapses, the membranes of pre- and post-synaptic neurons are in very close proximity, and "
  "electrical current can flow directly from one neuron into the other across these synapses. Neurotransmitters "
  "are involved only at chemical synapses, where the membranes are separated by a fluid-filled space called the "
  "synaptic cleft. A is true; R wrongly gives the electrical synapse the cleft of a chemical synapse.",
  ["A: true - current flows directly", "R: false - the synaptic cleft belongs to a chemical synapse"],
  "Transmission of Impulses", ans="C",
  why="R is false, so options treating both statements as true are wrong; A is true because current passes "
      "directly between the closely apposed membranes, so 'A is false' is wrong.", secs=40)

Z(NCC, "Nervous system divisions", A, D,
  "How many of the following structures of the human brain belong to the MIDBRAIN or the HINDBRAIN (i.e. not "
  "to the forebrain)?\n\nCerebrum, thalamus, corpora quadrigemina, pons, hypothalamus, cerebral aqueduct, "
  "cerebellum, hippocampus",
  "Divisions of the brain",
  "NCERT: the forebrain consists of the cerebrum, thalamus and hypothalamus; the hippocampus is one of the deep "
  "structures that, with the inner parts of the cerebral hemispheres, form the limbic system of the forebrain. "
  "The midbrain has the cerebral aqueduct passing through it and the corpora quadrigemina on its dorsal side. The "
  "hindbrain comprises the pons, cerebellum and medulla oblongata.",
  ["Forebrain: cerebrum, thalamus, hypothalamus, hippocampus (4)",
   "Midbrain: corpora quadrigemina, cerebral aqueduct (2)", "Hindbrain: pons, cerebellum (2)",
   "Midbrain + hindbrain = 4"],
  "Central Neural System",
  at="B", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three misses one of the four (usually the cerebral aqueduct, which is a canal in the midbrain); five counts "
      "the hippocampus or the hypothalamus outside the forebrain; six also puts the thalamus outside it.",
  secs=60)

# ================================================================ Chemical Coordination and Integration (4/6/4)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "Which one of the following hormones is NOT secreted by the adenohypophysis (pars distalis and pars "
  "intermedia)?",
  "Adenohypophysis versus neurohypophysis",
  "NCERT: the pars distalis produces GH, PRL, TSH, ACTH, LH and FSH, and the pars intermedia secretes only one "
  "hormone, MSH. The pars nervosa (neurohypophysis) stores and releases oxytocin and vasopressin, which are "
  "actually synthesised by the hypothalamus.",
  ["Pars distalis: GH, PRL, TSH, ACTH, LH, FSH", "Pars intermedia: MSH",
   "Neurohypophysis: releases oxytocin and vasopressin (made in hypothalamus)"],
  "Pituitary Gland",
  at="D", correct="Oxytocin",
  wrong=["Melanocyte stimulating hormone", "Prolactin", "Adrenocorticotrophic hormone"],
  why="MSH comes from the pars intermedia, and prolactin and ACTH from the pars distalis, so all three are "
      "adenohypophysis hormones; oxytocin is released from the neurohypophysis.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "The glucocorticoids of the adrenal cortex take part in carbohydrate metabolism. Which hormone does NCERT "
  "name as the main glucocorticoid in our body?",
  "Glucocorticoids and mineralocorticoids",
  "NCERT: corticoids involved in carbohydrate metabolism are called glucocorticoids; in our body, cortisol is the "
  "main glucocorticoid. Corticoids which regulate the balance of water and electrolytes are called "
  "mineralocorticoids, and aldosterone is the main mineralocorticoid.",
  ["Glucocorticoids: carbohydrate metabolism -> main one cortisol",
   "Mineralocorticoids: water and electrolyte balance -> main one aldosterone"],
  "Adrenal Gland",
  at="B", correct="Cortisol",
  wrong=["Aldosterone", "Adrenaline", "Testosterone"],
  why="Aldosterone is the main mineralocorticoid; adrenaline is a catecholamine of the adrenal medulla; "
      "testosterone is the main androgen of the Leydig cells of the testis.", secs=20)

Z(CCI, "Adrenal, pancreas and gonads", B, STP,
  SP("A pair of testes is present in the scrotal sac, outside the abdomen, of male individuals.",
     "A pair of ovaries, the primary female sex organs, is located in the abdomen."),
  "Location of the gonads",
  "NCERT: a pair of testis is present in the scrotal sac (outside abdomen) of male individuals; the testis "
  "performs dual functions as a primary sex organ as well as an endocrine gland. Females have a pair of ovaries "
  "located in the abdomen; the ovary is the primary female sex organ.",
  ["Statement I: true", "Statement II: true"],
  "Testis; Ovary", ans="A",
  why="Both statements are NCERT descriptions, so every option calling either of them false is wrong.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, ASR,
  AR("Deficiency of iodine in the diet results in hypothyroidism and enlargement of the thyroid gland, commonly "
     "called goitre.",
     "Iodine is essential for the normal rate of hormone synthesis in the thyroid gland."),
  "Iodine and the thyroid",
  "NCERT: iodine is essential for the normal rate of hormone synthesis in the thyroid. Deficiency of iodine in our "
  "diet results in hypothyroidism and enlargement of the thyroid gland, commonly called goitre. Without enough "
  "iodine the gland cannot make its hormones at the normal rate, which is why iodine deficiency causes "
  "hypothyroidism; R explains A.",
  ["A: true", "R: true", "Too little iodine -> too little hormone synthesis -> hypothyroidism"],
  "Thyroid Gland", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R gives the reason iodine "
      "deficiency lowers thyroid hormone output, so it is not an unrelated statement.", secs=30)

Z(CCI, "Thyroid, parathyroid and pineal", I, MAT,
  ML(("hormone", "one of its actions described in NCERT"),
     ["Melatonin", "Cortisol", "Thyroid hormones", "Androgens"],
     ["Anabolic (synthetic) effects on protein and carbohydrate metabolism",
      "Influences the menstrual cycle",
      "Maintenance of water and electrolyte balance",
      "Produces anti-inflammatory reactions and suppresses the immune response"]),
  "Less familiar hormone actions",
  "NCERT: melatonin also influences metabolism, pigmentation, the menstrual cycle and our defence capability. "
  "Glucocorticoids, particularly cortisol, produce anti-inflammatory reactions and suppress the immune response. "
  "Maintenance of water and electrolyte balance is also influenced by thyroid hormones. Androgens produce "
  "anabolic (synthetic) effects on protein and carbohydrate metabolism.",
  ["A -> II", "B -> IV", "C -> III", "D -> I"],
  "Pineal Gland; Thyroid Gland; Adrenal Gland; Testis",
  at="D", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Anti-inflammatory and immunosuppressive action belongs to cortisol, not to thyroid hormones or melatonin; "
      "the anabolic effect is an androgen action, not a melatonin action.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, MUL,
  MS("Which of the following hormones are produced by cells of the gonads (testis or ovary)?",
     ["Testosterone", "Estrogen", "Progesterone", "Follicle stimulating hormone", "Gonadotrophin releasing hormone"]),
  "Hormones of the gonads",
  "NCERT: Leydig cells in the intertubular spaces of the testis produce androgens, mainly testosterone. In the "
  "ovary, estrogen is synthesised and secreted mainly by the growing ovarian follicles, and the corpus luteum "
  "(formed from the ruptured follicle after ovulation) secretes mainly progesterone. FSH is a pars distalis "
  "hormone that acts on the gonads, and GnRH is a hypothalamic hormone acting on the pituitary.",
  ["(a) Leydig cells", "(b) growing follicles", "(c) corpus luteum", "(d) pituitary - acts ON gonads",
   "(e) hypothalamus"],
  "Testis; Ovary",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="FSH and GnRH regulate the gonads but are made in the pituitary and the hypothalamus respectively, so every "
      "option containing (d) or (e) is wrong.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", I, D,
  "Which of the following actions does NCERT ascribe to BOTH the glucocorticoids (such as cortisol) and the "
  "catecholamines (adrenaline and noradrenaline)?",
  "Comparing adrenal cortex and adrenal medulla hormones",
  "NCERT: glucocorticoids stimulate gluconeogenesis, lipolysis and proteolysis; cortisol also produces "
  "anti-inflammatory reactions, suppresses the immune response and stimulates RBC production. Catecholamines "
  "increase alertness, pupillary dilation, piloerection and sweating, increase heart beat and rate of respiration, "
  "stimulate glycogen breakdown, and also stimulate the breakdown of lipids and proteins. Breakdown of lipids and "
  "proteins is the action common to both.",
  ["Glucocorticoids: lipolysis + proteolysis (+ gluconeogenesis)",
   "Catecholamines: breakdown of lipids and proteins (+ glycogen breakdown)", "Common: lipids and proteins broken down"],
  "Adrenal Gland",
  at="A", correct="Stimulating the breakdown of lipids and proteins",
  wrong=["Causing pupillary dilation and piloerection", "Suppressing the immune response",
         "Stimulating RBC production"],
  why="Pupillary dilation and piloerection are catecholamine effects only; suppression of the immune response and "
      "stimulation of RBC production are given for cortisol only.", secs=40)

Z(CCI, "Thyroid, parathyroid and pineal", I, ASR,
  AR("Thyroid hormones support the process of red blood cell formation.",
     "The thyroid gland is composed of follicles and stromal tissues."),
  "Thyroid structure and functions",
  "NCERT: the thyroid gland is composed of follicles and stromal tissues, each follicle being composed of "
  "follicular cells enclosing a cavity. Separately, NCERT lists among the actions of thyroid hormones that they "
  "support the process of red blood cell formation. Both are true, but the histology of the gland does not "
  "explain why its hormones support RBC formation.",
  ["A: true", "R: true", "R is structure of the gland, A is an action of its hormones -> unrelated"],
  "Thyroid Gland", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R describes the gland's "
      "tissue make-up, which says nothing about the hormones' effect on RBC formation, so it is not the "
      "explanation.", secs=35)

Z(CCI, "Thyroid, parathyroid and pineal", I, STP,
  SP("Thyroxine (tetraiodothyronine) and triiodothyronine, the hormones of the thyroid follicular cells, are "
     "iodothyronines.",
     "Thyrocalcitonin (TCT), which is also secreted by the thyroid gland, is an iodothyronine as well."),
  "Chemical nature of thyroid secretions",
  "NCERT: the follicular cells synthesise two hormones, tetraiodothyronine or thyroxine (T4) and "
  "triiodothyronine (T3); in the classification of hormones by chemical nature, iodothyronines are the thyroid "
  "hormones. The thyroid gland also secretes a PROTEIN hormone called thyrocalcitonin (TCT), which regulates the "
  "blood calcium level.",
  ["Statement I: true (T4 and T3 are iodothyronines)", "Statement II: false - TCT is a protein hormone"],
  "Thyroid Gland; Mechanism of Hormone Action", ans="C",
  why="Statement II is false because NCERT calls TCT a protein hormone, so options calling it true are wrong; "
      "Statement I is true, so options calling it false are wrong.", secs=35)

Z(CCI, "Hypothalamus and pituitary", I, D,
  "A hormone has these three features: it is synthesised by hypothalamic neurons; it is stored in and released "
  "from the neurohypophysis; and it acts mainly at the kidney, reducing the loss of water through urine. The "
  "hormone is:",
  "Identifying a hormone from its features",
  "NCERT: the pars nervosa stores and releases oxytocin and vasopressin, which are synthesised by the "
  "hypothalamus and transported axonally to the neurohypophysis. Vasopressin acts mainly at the kidney and "
  "stimulates resorption of water and electrolytes by the distal tubules, thereby reducing loss of water through "
  "urine (diuresis); hence it is also called the anti-diuretic hormone (ADH).",
  ["Hypothalamic synthesis + neurohypophysis release -> oxytocin or vasopressin",
   "Acts on kidney, reduces water loss -> vasopressin (ADH)"],
  "Hypothalamus; Pituitary Gland",
  at="D", correct="Vasopressin",
  wrong=["Oxytocin", "Aldosterone", "Parathyroid hormone"],
  why="Oxytocin shares the origin and release route but acts on smooth muscles (uterus, mammary glands), not the "
      "kidney; aldosterone and PTH act on renal tubules but come from the adrenal cortex and the parathyroid "
      "glands, not from hypothalamic neurons.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following actions does NCERT attribute to ESTROGENS?",
     ["Stimulation of growth and activities of the female secondary sex organs",
      "Development of the growing ovarian follicles",
      "Stimulation of the formation of alveoli in the mammary glands and of milk secretion",
      "Regulation of female sexual behaviour",
      "Induction of ovulation of the fully mature Graafian follicle"]),
  "Actions of estrogens",
  "NCERT: estrogen performs a wide range of actions such as stimulation of growth and activities of female "
  "secondary sex organs, development of growing ovarian follicles, appearance of female secondary sex characters "
  "and mammary gland development; estrogens also regulate female sexual behaviour. The formation of alveoli (sac-"
  "like structures which store milk) and milk secretion is stimulated by PROGESTERONE, and ovulation of the "
  "Graafian follicle is induced by LH.",
  ["(a) true", "(b) true", "(c) false - progesterone", "(d) true", "(e) false - LH"],
  "Ovary; Pituitary Gland",
  at="C", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(c) is a progesterone action and (e) is an LH action, so every option containing either is wrong; (a), "
      "(b) and (d) are the estrogen actions listed by NCERT.", secs=50)

Z(CCI, "Mechanism of hormone action", A, MAT,
  ML(("hormone", "chemical nature"),
     ["Thyrocalcitonin", "Triiodothyronine", "Progesterone", "Epinephrine"],
     ["Steroid", "Protein hormone", "Amino-acid derivative", "Iodothyronine"]),
  "Chemical classes of hormones",
  "NCERT groups hormones into peptide, polypeptide and protein hormones; steroids (e.g. cortisol, testosterone, "
  "estradiol and progesterone); iodothyronines (thyroid hormones); and amino-acid derivatives (e.g. epinephrine). "
  "The trap is thyrocalcitonin: although it comes from the thyroid gland, NCERT calls it a protein hormone, while "
  "triiodothyronine is an iodothyronine.",
  ["A thyrocalcitonin -> protein (II)", "B triiodothyronine -> iodothyronine (IV)", "C progesterone -> steroid (I)",
   "D epinephrine -> amino-acid derivative (III)"],
  "Mechanism of Hormone Action; Thyroid Gland",
  at="B", match=({"A": "II", "B": "IV", "C": "I", "D": "III"},
                 [{"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="Calling TCT an iodothyronine (and T3 a protein) confuses the two thyroid secretions; epinephrine is an "
      "amino-acid derivative, not a protein; and progesterone is a steroid, not an amino-acid derivative.",
  secs=50)

Z(CCI, "Hormonal disorders", A, ASR,
  AR("Both cretinism and exophthalmic goitre are disorders involving the thyroid gland.",
     "Both cretinism and exophthalmic goitre are forms of hyperthyroidism."),
  "Hypo- and hyperthyroid disorders",
  "NCERT: hypothyroidism during pregnancy causes defective development and maturation of the growing baby, "
  "leading to stunted growth (cretinism), mental retardation and other defects. Exophthalmic goitre (Graves' "
  "disease) is a form of hyperthyroidism, characterised by enlargement of the thyroid, protruding eyeballs, "
  "increased BMR and weight loss. So both involve the thyroid (A true), but cretinism results from "
  "HYPOthyroidism (R false).",
  ["A: true - both are thyroid disorders", "R: false - cretinism is due to hypothyroidism"],
  "Thyroid Gland", ans="C",
  why="R is false because cretinism is a hypothyroid condition, so options treating R as true are wrong; A is true, "
      "so 'A is false but R is true' is wrong.", secs=40)

Z(CCI, "Mechanism of hormone action", A, D,
  "How many of the following hormones are steroids, according to NCERT's classification of hormones by chemical "
  "nature?\n\nCortisol, thyroxine, testosterone, insulin, estradiol, epinephrine, progesterone, glucagon",
  "Steroid hormones",
  "NCERT: steroids include cortisol, testosterone, estradiol and progesterone. Thyroxine is an iodothyronine, "
  "insulin and glucagon are peptide (protein) hormones, and epinephrine is an amino-acid derivative.",
  ["Steroids: cortisol, testosterone, estradiol, progesterone = 4",
   "Not steroids: thyroxine (iodothyronine), insulin and glucagon (peptide), epinephrine (amino-acid derivative)"],
  "Mechanism of Hormone Action",
  at="D", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three leaves out one of NCERT's four steroid examples; five adds thyroxine, which also acts through "
      "intracellular receptors but is an iodothyronine, not a steroid; six adds insulin and glucagon or "
      "epinephrine.", secs=45)

# ================================================================ Human Reproduction (6/9/6)
Z(HR, "Gametogenesis", B, D,
  "A couple of million oogonia are formed in each fetal ovary, but a large number of follicles degenerate between "
  "birth and puberty. About how many primary follicles are left in each ovary at puberty?",
  "Follicles left at puberty",
  "NCERT: a large number of the follicles degenerate during the phase from birth to puberty. Therefore, at puberty "
  "only 60,000–80,000 primary follicles are left in each ovary.",
  ["Fetal ovary: a couple of million oogonia", "Birth -> puberty: many follicles degenerate",
   "Puberty: 60,000–80,000 primary follicles per ovary"],
  "Gametogenesis",
  at="C", correct="60,000–80,000",
  wrong=["200–300", "1–2 million", "200–300 million"],
  why="200–300 is near the number of testicular lobules (about 250), not follicles; 1–2 million is the order of "
      "the oogonia formed in fetal life, before degeneration; 200–300 million is the number of sperms in one "
      "ejaculate.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "The urethra of a human male originates from the urinary bladder and extends through the penis. Its external "
  "opening is called the:",
  "Male urethra",
  "NCERT: the urethra originates from the urinary bladder and extends through the penis to its external opening "
  "called the urethral meatus.",
  ["Urinary bladder -> urethra -> through the penis -> urethral meatus"],
  "The Male Reproductive System",
  at="A", correct="Urethral meatus",
  wrong=["Glans penis", "Ejaculatory duct", "Cervical canal"],
  why="The glans penis is the enlarged end of the penis, covered by the foreskin, not an opening; the ejaculatory "
      "duct is formed by the vas deferens and the seminal vesicle duct and opens into the urethra; the cervical "
      "canal is in the female cervix.", secs=20)

Z(HR, "Male and female reproductive systems", B, STP,
  SP("The uterus opens into the vagina through a narrow cervix.",
     "The cavity of the cervix, the cervical canal, forms the birth canal together with the oviduct."),
  "Cervix and birth canal",
  "NCERT: the uterus opens into the vagina through a narrow cervix. The cavity of the cervix is called the "
  "cervical canal, which along with the VAGINA forms the birth canal. The oviduct joins the uterus at the other "
  "end and is not part of the birth canal.",
  ["Statement I: true", "Statement II: false - cervical canal + vagina = birth canal"],
  "The Female Reproductive System", ans="C",
  why="Statement II replaces the vagina with the oviduct, so options calling it true are wrong; Statement I is "
      "NCERT's description, so options calling it false are wrong.", secs=30)

Z(HR, "Male and female reproductive systems", B, ASR,
  AR("Each ovary is covered by a thin epithelium which encloses the ovarian stroma.",
     "The ovaries are located one on each side of the lower abdomen."),
  "Structure and position of the ovary",
  "NCERT: ovaries are the primary female sex organs located one on each side of the lower abdomen. Each ovary is "
  "covered by a thin epithelium which encloses the ovarian stroma, which is divided into a peripheral cortex and "
  "an inner medulla. Both are true, but the ovary's position in the abdomen does not explain its epithelial "
  "covering.",
  ["A: true", "R: true", "R gives position, A gives structure -> no causal link"],
  "The Female Reproductive System", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; where the ovaries lie does "
      "not account for the epithelium around the stroma, so R is not the explanation of A.", secs=30)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "According to NCERT, during which month of human pregnancy are the first movements of the foetus and the "
  "appearance of hair on the head usually observed?",
  "Foetal development timeline",
  "NCERT: after one month of pregnancy, the embryo's heart is formed; by the end of the second month the foetus "
  "develops limbs and digits; by the end of 12 weeks most of the major organ systems are formed; during the fifth "
  "month, the first movements of the foetus and the appearance of hair on the head are usually observed; by the end "
  "of about 24 weeks the body is covered with fine hair, eyelids separate and eyelashes are formed.",
  ["1 month: heart", "2 months: limbs and digits", "12 weeks: major organ systems",
   "5th month: first movements, hair on head", "24 weeks: fine hair, eyelids separate"],
  "Pregnancy and Embryonic Development",
  at="D", correct="The fifth month",
  wrong=["The first month", "The second month", "The ninth month"],
  why="The first month is when the heart forms and the second month when limbs and digits develop; by the end of "
      "the ninth month the foetus is fully developed and ready for delivery, long after the first movements.",
  secs=25)

Z(HR, "Gametogenesis", B, D,
  "In the fetal ovary, the gamete mother cells (oogonia) start division and get temporarily arrested as primary "
  "oocytes. At which stage are they arrested?",
  "Arrest of primary oocytes",
  "NCERT: oogonia start division and enter into prophase-I of the meiotic division and get temporarily arrested "
  "at that stage; they are then called primary oocytes.",
  ["Oogonia -> enter meiosis I", "Arrested in prophase-I -> primary oocytes"],
  "Gametogenesis",
  at="B", correct="Prophase-I of the meiotic division",
  wrong=["Metaphase of mitosis", "Prophase-II of the meiotic division",
         "After completing the second meiotic division"],
  why="The oogonia have entered meiosis, so a mitotic arrest is wrong; prophase-II would require the first "
      "meiotic division to be complete, which happens only within the tertiary follicle; the second meiotic "
      "division is completed only when a sperm enters the secondary oocyte.", secs=25)

Z(HR, "Male and female reproductive systems", I, MAT,
  ML(("part of a human sperm", "feature described in NCERT"),
     ["Head", "Acrosome", "Middle piece", "Tail"],
     ["Its movement facilitates the sperm motility essential for fertilisation",
      "Contains an elongated haploid nucleus",
      "Possesses numerous mitochondria",
      "Cap-like structure filled with enzymes that help fertilisation of the ovum"]),
  "Structure of a sperm",
  "NCERT: the sperm head contains an elongated haploid nucleus, the anterior portion of which is covered by a "
  "cap-like structure, the acrosome, filled with enzymes that help fertilisation of the ovum. The middle piece "
  "possesses numerous mitochondria, which produce energy for the movement of the tail that facilitates sperm "
  "motility essential for fertilisation.",
  ["A head -> II", "B acrosome -> IV", "C middle piece -> III", "D tail -> I"],
  "The Male Reproductive System; Gametogenesis",
  at="D", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="The acrosome caps the head but carries enzymes, while the nucleus lies in the head, so swapping A and B is "
      "wrong; the mitochondria are in the middle piece and supply energy for the tail's movement, so swapping C "
      "and D is wrong; the acrosome holds enzymes, not mitochondria.", secs=40)

Z(HR, "Menstrual cycle", I, MUL,
  MS("Which of the following statements about the human menstrual cycle are correct, according to NCERT?",
     ["The first menstruation, which begins at puberty, is called menarche.",
      "The menstrual flow lasts for about 3–5 days.",
      "The menstrual cycle is repeated at an average interval of about 14 days.",
      "Both LH and FSH attain a peak level in the middle of the cycle (about the 14th day).",
      "Menstrual cycles cease around 50 years of age; this is termed menopause."]),
  "Timings in the menstrual cycle",
  "NCERT: the first menstruation begins at puberty and is called menarche. The cycle is repeated at an average "
  "interval of about 28/29 days. The menstrual flow lasts for 3–5 days. Both LH and FSH attain a peak level in the "
  "middle of the cycle (about the 14th day). In human beings, menstrual cycles cease around 50 years of age, "
  "termed menopause. 14 days is the time to ovulation, not the length of the cycle.",
  ["(a) true", "(b) true", "(c) false - about 28/29 days", "(d) true", "(e) true"],
  "Menstrual Cycle",
  at="C", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (d) only", "(b), (c) and (e) only"],
  why="(c) gives the time to the mid-cycle peak instead of the length of the cycle, so options containing (c) are "
      "wrong; the correct option keeps all the other four NCERT timings.", secs=45)

Z(HR, "Fertilisation and implantation", I, D,
  "In a woman, an ovum is fertilised in the ampullary region and the zygote undergoes cleavage to form a morula, "
  "but the morula fails to transform into a blastocyst. According to NCERT's sequence of events, which of the "
  "following could then NOT take place?",
  "From morula to implantation",
  "NCERT: the morula continues to divide and transforms into a blastocyst as it moves further into the uterus. "
  "The blastomeres in the blastocyst are arranged into an outer trophoblast and an inner cell mass. The "
  "trophoblast layer then gets attached to the endometrium; the uterine cells divide rapidly and cover the "
  "blastocyst, which becomes embedded in the endometrium (implantation). Without a blastocyst there is no "
  "trophoblast to attach, so implantation cannot occur. The other events listed come before the morula stage.",
  ["Fertilisation (done) -> cleavage -> morula (done)", "Morula -> blastocyst (fails)",
   "Trophoblast attaches to endometrium -> implantation (cannot occur)"],
  "Fertilisation and Implantation",
  at="A", correct="Attachment of the trophoblast to the endometrium (implantation)",
  wrong=["Fusion of the haploid nuclei of the sperm and the ovum",
         "Formation of 2, 4 and 8 blastomeres by mitotic division",
         "Completion of the second meiotic division of the secondary oocyte"],
  why="Fusion of the gametes' nuclei and completion of the second meiotic division happen at fertilisation, and "
      "cleavage into 2, 4 and 8 blastomeres produces the morula; all three are already over when the morula "
      "fails to form a blastocyst.", secs=45)

Z(HR, "Gametogenesis", I, ASR,
  AR("Oogonia continue to be formed and added to the ovaries throughout the reproductive life of a woman.",
     "Gamete mother cells (oogonia) are formed within each fetal ovary during embryonic development."),
  "Timing of oogonia formation",
  "NCERT: oogenesis is initiated during the embryonic development stage when a couple of million gamete mother "
  "cells (oogonia) are formed within each fetal ovary; no more oogonia are formed and added after birth. So R is "
  "true and A is false.",
  ["A: false - no oogonia are added after birth", "R: true - formed in the fetal ovary"],
  "Gametogenesis", ans="D",
  why="A contradicts NCERT's statement that no more oogonia are formed and added after birth, so options calling A "
      "true are wrong; R is NCERT's own statement, so 'A is false but R is true' is the answer.", secs=35)

Z(HR, "Male and female reproductive systems", I, STP,
  SP("Each human testis has about 250 compartments called testicular lobules.",
     "Each testicular lobule contains about 10 to 12 highly coiled seminiferous tubules."),
  "Testicular lobules",
  "NCERT: each testis has about 250 compartments called testicular lobules, and each lobule contains one to three "
  "highly coiled seminiferous tubules in which sperms are produced. 10–12 cm is the length of an oviduct, not the "
  "number of tubules.",
  ["Statement I: true", "Statement II: false - one to three tubules per lobule"],
  "The Male Reproductive System", ans="C",
  why="Statement II overstates the number of tubules per lobule, so options calling it true are wrong; Statement "
      "I is NCERT's figure, so options calling it false are wrong.", secs=30)

Z(HR, "Male and female reproductive systems", I, D,
  "Which option gives the three layers of the wall of the human uterus in the correct order from the OUTSIDE to "
  "the INSIDE (towards the uterine cavity)?",
  "Layers of the uterine wall",
  "NCERT: the wall of the uterus has three layers of tissue: the external thin membranous perimetrium, the middle "
  "thick layer of smooth muscle, the myometrium, and the inner glandular layer called the endometrium that lines "
  "the uterine cavity.",
  ["Outer: perimetrium (thin, membranous)", "Middle: myometrium (thick smooth muscle)",
   "Inner: endometrium (glandular, lines the cavity)"],
  "The Female Reproductive System",
  at="B", correct="Perimetrium → myometrium → endometrium",
  wrong=["Endometrium → myometrium → perimetrium", "Myometrium → perimetrium → endometrium",
         "Perimetrium → endometrium → myometrium"],
  why="The first option lists the layers from inside to outside; the myometrium is the middle layer, not the "
      "outermost; and the glandular endometrium lines the cavity, so it cannot lie between the other two.", secs=30)

Z(HR, "Male and female reproductive systems", I, D,
  "According to NCERT, each seminiferous tubule of the human testis is lined on its inside by which two types of "
  "cells?",
  "Lining of the seminiferous tubule",
  "NCERT: each seminiferous tubule is lined on its inside by two types of cells called male germ cells "
  "(spermatogonia) and Sertoli cells. The regions outside the seminiferous tubules, the interstitial spaces, "
  "contain small blood vessels and interstitial cells or Leydig cells; other immunologically competent cells are "
  "also present there.",
  ["Inside the tubule: spermatogonia + Sertoli cells", "Outside (interstitial spaces): Leydig cells, blood vessels"],
  "The Male Reproductive System",
  at="A", correct="Male germ cells (spermatogonia) and Sertoli cells",
  wrong=["Leydig cells and spermatogonia", "Sertoli cells and Leydig cells",
         "Leydig cells and immunologically competent cells"],
  why="Leydig cells and immunologically competent cells lie in the interstitial spaces outside the tubules, so "
      "every option naming Leydig cells is wrong.", secs=25)

# numerical: date of ovulation in a 28-day cycle
import datetime as _dt
_ov = _dt.date(2026, 6, 3) + _dt.timedelta(days=14 - 1)
assert _ov == _dt.date(2026, 6, 16)
Z(HR, "Menstrual cycle", I, NUM,
  "A woman has regular 28-day menstrual cycles. The menstrual flow of one cycle begins on 3 June, which is day 1 of "
  "that cycle. Using NCERT's account that ovulation takes place in the middle of the cycle (about the 14th day), on "
  "about which date is ovulation expected in this cycle?",
  "Locating ovulation in the cycle",
  "NCERT: the menstrual phase starts the cycle, and both LH and FSH peak in the middle of the cycle (about the 14th "
  "day); the LH surge induces rupture of the Graafian follicle and release of the ovum (ovulation). Day 1 is 3 "
  "June, so day 14 is 13 days later: 16 June.",
  ["Day 1 = 3 June", "Day 14 = 3 June + 13 days", "= 16 June"],
  "Menstrual Cycle",
  at="D", correct="16 June",
  wrong=["17 June", "1 July", "10 June"],
  why="17 June adds 14 days to day 1 (that is day 15); 1 July is day 29, the start of the next cycle; 10 June "
      "(day 8) falls in the follicular phase, before the mid-cycle LH surge.",
  short="Day n of the cycle = start date + (n - 1) days.", secs=45, vb=RECOMPUTED)

_chrom = 23 + 23 + 23   # ootid + second polar body + first polar body, all haploid
assert _chrom == 69
Z(HR, "Gametogenesis", I, NUM,
  "A human primary oocyte (46 chromosomes) completes its first meiotic division before ovulation, and the "
  "secondary oocyte completes its second meiotic division when a sperm enters it. Assume the first polar body "
  "does not divide further. What is the total number of chromosomes present in the ootid (ovum), the second polar "
  "body and the first polar body taken together?",
  "Chromosome numbers in oogenesis",
  "NCERT: the first meiotic division of the primary oocyte is unequal and gives a large haploid secondary oocyte "
  "and a tiny first polar body. When a sperm enters, the secondary oocyte completes the second meiotic division, "
  "giving a second polar body and a haploid ovum (ootid). All three cells are haploid, with 23 chromosomes each.",
  ["First polar body: 23", "Second polar body: 23", "Ootid: 23", "Total = 69"],
  "Gametogenesis; Fertilisation and Implantation",
  at="B", correct="69",
  wrong=["46", "92", "23"],
  why="46 forgets the first polar body; 92 treats the ootid as diploid (46) and adds two haploid polar bodies; "
      "23 counts only the ootid.", secs=50, vb=RECOMPUTED)

Z(HR, "Male and female reproductive systems", A, MUL,
  MS("Which of the following statements correctly compare the human testis and ovary?",
     ["Both are primary sex organs that produce gametes as well as hormones.",
      "The testes lie outside the abdominal cavity in the scrotum, whereas the ovaries lie in the lower abdomen.",
      "Both contain highly coiled seminiferous tubules in which the gametes are produced.",
      "Each testis is about 4 to 5 cm long, whereas each ovary is about 2 to 4 cm long.",
      "The ovarian stroma is divided into a peripheral cortex and an inner medulla, whereas each testicular lobule "
      "contains one to three seminiferous tubules."]),
  "Testis and ovary compared",
  "NCERT: the testes are situated outside the abdominal cavity within a pouch called the scrotum; each testis is "
  "oval, about 4 to 5 cm long and 2 to 3 cm wide, with about 250 lobules each containing one to three seminiferous "
  "tubules in which sperms are produced. The ovaries are located one on each side of the lower abdomen; each ovary "
  "is about 2 to 4 cm long, and its stroma is divided into a peripheral cortex and an inner medulla. Both are "
  "primary sex organs that produce gametes and hormones. Seminiferous tubules occur only in the testis; ova "
  "develop in ovarian follicles.",
  ["(a) true", "(b) true", "(c) false - seminiferous tubules only in the testis", "(d) true", "(e) true"],
  "The Male Reproductive System; The Female Reproductive System",
  at="A", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (c) only", "(b), (d) and (e) only"],
  why="(c) is false because ova develop in ovarian follicles, so every option with (c) is wrong; '(b), (d) and (e) "
      "only' leaves out (a), which is true for both gonads.", secs=60)

Z(HR, "Menstrual cycle", A, MAT,
  ML(("event", "hormone mainly responsible, as described in NCERT"),
     ["Rupture of the Graafian follicle and release of the ovum",
      "Maintenance of the endometrium during the luteal phase",
      "Stronger uterine contractions during parturition",
      "Secretion of factors by Sertoli cells that help in spermiogenesis"],
     ["FSH", "Oxytocin", "LH", "Progesterone"]),
  "Hormonal control of reproductive events",
  "NCERT: the rapid secretion of LH (LH surge) in the middle of the cycle induces rupture of the Graafian follicle "
  "and release of the ovum. Progesterone secreted by the corpus luteum is essential for maintenance of the "
  "endometrium. Oxytocin from the maternal pituitary acts on the uterine muscle and causes stronger uterine "
  "contractions at parturition. FSH acts on the Sertoli cells and stimulates secretion of some factors which help "
  "in the process of spermiogenesis (LH acts on the Leydig cells).",
  ["A -> LH (III)", "B -> progesterone (IV)", "C -> oxytocin (II)", "D -> FSH (I)"],
  "Menstrual Cycle; Gametogenesis; Parturition and Lactation",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "I", "B": "IV", "C": "II", "D": "III"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="Swapping LH and FSH puts ovulation under FSH and the Sertoli cells under LH, which acts on the Leydig cells; "
      "progesterone maintains the endometrium and oxytocin causes the contractions, so swapping them is wrong; "
      "FSH does not cause uterine contractions.", secs=55)

Z(HR, "Gametogenesis", A, ASR,
  AR("The secondary oocyte released at ovulation is haploid, although it has not yet completed meiosis.",
     "Before ovulation, the primary oocyte completes its first meiotic division, which results in a large haploid "
     "secondary oocyte and a tiny first polar body."),
  "Ploidy of the ovulated oocyte",
  "NCERT: the primary oocyte within the tertiary follicle grows in size and completes its first meiotic division. "
  "It is an unequal division resulting in the formation of a large haploid secondary oocyte and a tiny first polar "
  "body. The second meiotic division is completed only when a sperm enters. The haploid state of the ovulated cell "
  "is therefore the result of the completed first meiotic division described in R.",
  ["A: true - secondary oocyte is haploid, meiosis II pending", "R: true - meiosis I completed before ovulation",
   "First meiotic division halves the chromosome number -> R explains A"],
  "Gametogenesis", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; the haploid state comes from "
      "the first meiotic division that R describes, so R is the explanation, not an unrelated fact.", secs=45)

Z(HR, "Menstrual cycle", A, STP,
  SP("During pregnancy, all events of the menstrual cycle stop and there is no menstruation.",
     "Menstruation occurs only if the released ovum is not fertilised."),
  "Menstruation and pregnancy",
  "NCERT: menstruation only occurs if the released ovum is not fertilised; lack of menstruation may be indicative "
  "of pregnancy, though it may also be caused by other underlying causes such as stress or poor health. During "
  "pregnancy all events of the menstrual cycle stop and there is no menstruation.",
  ["Statement I: true", "Statement II: true"],
  "Menstrual Cycle", ans="A",
  why="Both statements are NCERT's own, so options calling either false are wrong. (The converse of II, that "
      "every missed period means pregnancy, is NOT claimed: NCERT adds stress and poor health as other causes.)",
  secs=35)

Z(HR, "Pregnancy, parturition and lactation", A, D,
  "How many of the following are produced by the human OVARY (at some stage of the reproductive life of a woman)?"
  "\n\nRelaxin, estrogen, hCG, progesterone, hPL, oxytocin, prolactin, secondary oocyte",
  "Products of the ovary",
  "NCERT: the ovaries produce the female gamete (ovum, released as the secondary oocyte at ovulation) and several "
  "steroid hormones, estrogen and progesterone. In the later phase of pregnancy, relaxin is secreted by the ovary. "
  "hCG and hPL are made by the placenta; oxytocin is released from the maternal pituitary and prolactin from the "
  "anterior pituitary.",
  ["Ovary: secondary oocyte, estrogen, progesterone, relaxin = 4", "Placenta: hCG, hPL",
   "Pituitary: oxytocin (released), prolactin"],
  "The Female Reproductive System; Pregnancy and Embryonic Development",
  at="B", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three usually forgets relaxin, which NCERT says the ovary secretes late in pregnancy; five or six add "
      "placental hormones (hCG, hPL) or pituitary hormones (prolactin, oxytocin).", secs=50)

Z(HR, "Gametogenesis", A, D,
  "Which pair consists of cells that are BOTH haploid and BOTH formed directly by the second meiotic division?",
  "Products of meiosis II",
  "NCERT: secondary spermatocytes undergo the second meiotic division to produce four equal, haploid spermatids. "
  "The secondary oocyte completes the second meiotic division when a sperm enters, forming a second polar body and "
  "a haploid ovum (ootid). Secondary spermatocytes and the first polar body come from the FIRST meiotic division; "
  "spermatozoa come from spermatids by spermiogenesis, which involves no division; and the primary oocyte is "
  "diploid.",
  ["Meiosis I products: secondary spermatocytes, secondary oocyte + first polar body",
   "Meiosis II products: spermatids, ootid + second polar body", "Spermiogenesis: spermatid -> spermatozoon"],
  "Gametogenesis",
  at="C", correct="Spermatid and second polar body",
  wrong=["Secondary spermatocyte and first polar body", "Spermatozoon and ootid", "Primary oocyte and spermatid"],
  why="Secondary spermatocytes and the first polar body are haploid but come from the first meiotic division; a "
      "spermatozoon is formed by spermiogenesis, not by a division; the primary oocyte is diploid.", secs=50)

# ================================================================ Reproductive Health (4/5/4)
Z(RH, "Contraception", B, D,
  "Besides motivating smaller families, NCERT mentions a statutory measure taken to tackle population growth in "
  "India: raising the marriageable age. To what ages was it raised?",
  "Measures for population stabilisation",
  "NCERT: statutory raising of the marriageable age of the female to 18 years and that of the male to 21 years, "
  "and incentives given to couples with small families, are two of the other measures taken to tackle the "
  "problem of population growth.",
  ["Female: 18 years", "Male: 21 years"],
  "Population Stabilisation and Birth Control",
  at="D", correct="18 years for females and 21 years for males",
  wrong=["21 years for females and 18 years for males", "18 years for both females and males",
         "16 years for females and 18 years for males"],
  why="The first option reverses the two ages; NCERT gives different ages for males and females, so 18 for both "
      "is wrong; 16 and 18 are lower than the ages NCERT states.", secs=20)

Z(RH, "STDs and their prevention", B, D,
  "If sexually transmitted infections (STIs) are not detected and treated in time, NCERT says they may lead to "
  "complications later. Which set lists those complications?",
  "Complications of untreated STIs",
  "NCERT: early symptoms of most STIs are minor, and infected females may often be asymptomatic, so infections "
  "may remain undetected or untreated for a long time. This could lead to complications later, which include "
  "pelvic inflammatory diseases (PID), abortions, still births, ectopic pregnancies, infertility or even cancer of "
  "the reproductive tract.",
  ["Untreated STIs -> PID, abortions, still births, ectopic pregnancies, infertility, cancer of the reproductive "
   "tract"],
  "Sexually Transmitted Infections (STIs)",
  at="A", correct="Pelvic inflammatory diseases, abortions, still births, ectopic pregnancies, infertility and even "
                  "cancer of the reproductive tract",
  wrong=["Goitre, cretinism and exophthalmic goitre",
         "Diabetes insipidus, diabetes mellitus and Addison's disease",
         "Colour blindness, haemophilia and sickle-cell anaemia"],
  why="The other sets are hormonal disorders (thyroid, ADH, insulin, adrenal cortex) or inherited genetic "
      "disorders, none of which NCERT links to untreated STIs.", secs=25)

Z(RH, "Contraception", B, STP,
  SP("'Nirodh' is a popular brand of condom for the male.",
     "Unlike diaphragms, cervical caps and vaults, male and female condoms are reusable."),
  "Condoms and other barriers",
  "NCERT: condoms are barriers made of thin rubber/latex sheath; 'Nirodh' is a popular brand of condom for the "
  "male. Both the male and the female condoms are DISPOSABLE, can be self-inserted and thereby give privacy to the "
  "user. It is the diaphragms, cervical caps and vaults (also made of rubber) that are reusable.",
  ["Statement I: true", "Statement II: false - condoms are disposable; diaphragms, caps and vaults are reusable"],
  "Population Stabilisation and Birth Control", ans="C",
  why="Statement II reverses NCERT's contrast between disposable condoms and reusable diaphragms, caps and vaults, "
      "so options calling it true are wrong; Statement I is NCERT's own, so options calling it false are wrong.",
  secs=30)

Z(RH, "Contraception", B, ASR,
  AR("Lactational amenorrhea is a natural method of contraception.",
     "The chances of failure of natural methods of contraception are high."),
  "Natural methods",
  "NCERT: natural methods work on the principle of avoiding chances of the ovum and sperms meeting; periodic "
  "abstinence, withdrawal (coitus interruptus) and lactational amenorrhea are such methods. Since no medicines or "
  "devices are used, side effects are almost nil, but the chances of failure are also high. A method is natural "
  "because it uses no device, medicine or surgery, not because it often fails; so R, though true, does not explain "
  "A.",
  ["A: true", "R: true", "R is a limitation of natural methods, not the reason a method is called natural"],
  "Population Stabilisation and Birth Control", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; a high failure rate is a "
      "drawback of natural methods, not what makes lactational amenorrhea one, so R is not the explanation.",
  secs=35)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive", "type"),
     ["Vaults", "Multiload 375", "Implants under the skin", "Periodic abstinence"],
     ["Natural method", "Barrier method", "Progestogens alone or with estrogen given by the female",
      "Copper-releasing IUD"]),
  "Kinds of contraceptives",
  "NCERT: diaphragms, cervical caps and vaults are barriers made of rubber, inserted into the female tract to cover "
  "the cervix during coitus. Copper-releasing IUDs are CuT, Cu7 and Multiload 375. Progestogens alone or in "
  "combination with estrogen can be used by females as injections or implants under the skin. Periodic abstinence "
  "is a natural method.",
  ["A vaults -> barrier (II)", "B Multiload 375 -> copper IUD (IV)", "C implants -> progestogens (III)",
   "D periodic abstinence -> natural (I)"],
  "Population Stabilisation and Birth Control",
  at="B", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="A vault is a rubber barrier, not an IUD; Multiload 375 releases copper, not hormones, and implants are "
      "hormonal; periodic abstinence uses no barrier at all.", secs=40)

Z(RH, "Infertility and ART", I, MUL,
  MS("A large number of couples all over the world, including India, are infertile. Which of the following does "
     "NCERT list as possible reasons for infertility?",
     ["Physical reasons", "Congenital diseases", "Drugs", "Immunological reasons", "Psychological reasons"]),
  "Causes of infertility",
  "NCERT: infertility is the inability to conceive or produce children even after unprotected sexual "
  "co-habitation. The reasons for this could be many: physical, congenital diseases, drugs, immunological or even "
  "psychological. All five listed causes are therefore in NCERT's list.",
  ["(a)-(e) all appear in NCERT's list: physical, congenital diseases, drugs, immunological, psychological"],
  "Infertility",
  at="D", correct="(a), (b), (c), (d) and (e)",
  wrong=["(a), (b) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only"],
  why="NCERT includes immunological and even psychological reasons alongside physical causes, congenital "
      "diseases and drugs, so every option that leaves out any of them is incomplete.", secs=35)

Z(RH, "Contraception", I, D,
  "Advertisements and posters in India often show a happy couple with two children and the slogan 'Hum Do Hamare "
  "Do' (we two, our two). According to NCERT, what is the purpose of such campaigns?",
  "Motivating small families",
  "NCERT: the most important step to overcome the population explosion is to motivate smaller families by using "
  "various contraceptive methods. Advertisements showing a happy couple with two children and the slogan Hum Do "
  "Hamare Do serve this aim; many couples, mostly the young, urban, working ones, have even adopted a 'one child "
  "norm'.",
  ["Problem: population explosion", "Strategy: motivate smaller families using contraceptive methods"],
  "Population Stabilisation and Birth Control",
  at="C", correct="To motivate smaller families by using contraceptive methods, so as to check population growth",
  wrong=["To encourage medical termination of every third pregnancy",
         "To promote amniocentesis for choosing the sex of the two children",
         "To encourage assisted reproductive technologies for every couple"],
  why="NCERT says MTP is not meant for population control and condemns the misuse of amniocentesis for sex "
      "determination; ART is for infertile couples, not a population measure.", secs=30)

Z(RH, "STDs and their prevention", I, ASR,
  AR("STIs in women may remain undetected or untreated for a long time.",
     "In infected females, STIs are often asymptomatic, and the early symptoms of most STIs are minor."),
  "Late detection of STIs",
  "NCERT: early symptoms of most of these diseases are minor, and these include itching, fluid discharge, slight "
  "pain, swellings, etc., in the genital region. Infected females may often be asymptomatic and hence may remain "
  "undetected for long. Absent or less significant early symptoms (along with social stigma) deter people from "
  "timely detection and treatment. R gives the very reason for A.",
  ["A: true", "R: true", "No or minor symptoms -> infection goes unnoticed -> R explains A"],
  "Sexually Transmitted Infections (STIs)", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT links the absence of "
      "symptoms directly to infections remaining undetected, so R is the correct explanation.", secs=35)

Z(RH, "Contraception", I, STP,
  SP("The chances of failure of periodic abstinence and coitus interruptus are high.",
     "Tubectomy is the sterilisation method adopted by the male partner."),
  "Natural and surgical methods",
  "NCERT: natural methods such as periodic abstinence and coitus interruptus have almost nil side effects, but "
  "their chances of failure are also high. Sterilisation in the male is called vasectomy (a small part of the vas "
  "deferens is removed or tied up); that in the female is called tubectomy (a small part of the fallopian tube is "
  "removed or tied up).",
  ["Statement I: true", "Statement II: false - tubectomy is for the female; vasectomy for the male"],
  "Population Stabilisation and Birth Control", ans="C",
  why="Statement II confuses tubectomy with vasectomy, so options calling it true are wrong; Statement I is "
      "NCERT's limitation of natural methods, so options calling it false are wrong.", secs=30)

Z(RH, "Contraception", A, MUL,
  MS("Which of the following methods prevent conception WITHOUT the use of any device, medicine or surgery?",
     ["Periodic abstinence", "Coitus interruptus (withdrawal)", "Lactational amenorrhea", "Vasectomy",
      "Diaphragm"]),
  "Natural methods of contraception",
  "NCERT: natural methods work on the principle of avoiding chances of the ovum and sperms meeting; periodic "
  "abstinence, withdrawal (coitus interruptus) and lactational amenorrhea are such methods, and since no medicines "
  "or devices are used in them, side effects are almost nil. Vasectomy is a surgical method (sterilisation), and a "
  "diaphragm is a rubber barrier device.",
  ["(a), (b), (c): natural methods", "(d): surgical", "(e): barrier device"],
  "Population Stabilisation and Birth Control",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(a) and (c) only", "(b), (c) and (d) only"],
  why="A diaphragm is a device and vasectomy is surgery, so options with (d) or (e) are wrong; '(a) and (c) only' "
      "leaves out withdrawal, which NCERT lists as a natural method.", secs=40)

Z(RH, "Infertility and ART", A, D,
  "In how many of the following techniques does fertilisation take place INSIDE the body of the female (in vivo)?"
  "\n\nGIFT, ZIFT, IUT, ICSI, intra-uterine insemination (IUI), artificial insemination with semen introduced into "
  "the vagina",
  "In vivo versus in vitro fertilisation in ART",
  "NCERT: in IVF, ova and sperms are induced to form a zygote under simulated conditions in the laboratory; the "
  "zygote or early embryo (up to 8 blastomeres) is then transferred into the fallopian tube (ZIFT), and embryos "
  "with more than 8 blastomeres into the uterus (IUT). ICSI is a procedure to form an embryo in the laboratory, in "
  "which a sperm is directly injected into the ovum. In GIFT, an ovum collected from a donor is transferred into "
  "the fallopian tube of another female who can provide suitable environment for fertilisation. In artificial "
  "insemination, semen is introduced into the vagina or into the uterus (IUI), so fertilisation follows inside "
  "the female body.",
  ["In vivo: GIFT, IUI, AI into the vagina = 3", "In vitro (laboratory): ZIFT, IUT, ICSI"],
  "Infertility",
  at="B", correct="Three",
  wrong=["Two", "Four", "Five"],
  why="Two forgets that artificial insemination into the vagina, like IUI, leads to fertilisation in the body; four "
      "or five add ZIFT, IUT or ICSI, in which the zygote or embryo is formed in the laboratory.", secs=50)

Z(RH, "Contraception", A, ASR,
  AR("Emergency contraceptives are very effective even when used a week after unprotected coitus.",
     "Administration of progestogens or progestogen–estrogen combinations, or the use of IUDs, can be used as "
     "emergency contraceptives."),
  "Emergency contraception",
  "NCERT: administration of progestogens or progestogen–estrogen combinations, or IUDs, within 72 hours of coitus "
  "have been found to be very effective as emergency contraceptives, as they could be used to avoid possible "
  "pregnancy due to rape or casual unprotected intercourse. A week is well beyond the 72-hour window, so A is "
  "false while R is true.",
  ["A: false - effective within 72 hours", "R: true - pills/progestogens or IUDs"],
  "Population Stabilisation and Birth Control", ans="D",
  why="A ignores NCERT's 72-hour limit, so options calling A true are wrong; R correctly names the emergency "
      "methods, so 'A is false but R is true' is the answer.", secs=35)

Z(RH, "MTP and amniocentesis", A, MUL,
  MS("Which of the following does NCERT mention in its account of reproductive health programmes and their "
     "outcomes in India?",
     ["A statutory ban on amniocentesis for sex determination, to legally check increasing female foeticides",
      "Massive child immunisation",
      "Development of the oral contraceptive 'Saheli' by scientists at CDRI, Lucknow, as an outcome of research "
      "on reproduction-related areas",
      "Increased medically assisted deliveries and better post-natal care, leading to decreased maternal and infant "
      "mortality rates",
      "Compulsory sterilisation of every couple after the birth of two children"]),
  "Reproductive health programmes",
  "NCERT: a statutory ban on amniocentesis for sex determination to legally check increasing female foeticides, "
  "massive child immunisation, etc. are some programmes being undertaken; research on reproduction-related areas "
  "is encouraged, and 'Saheli' was developed by scientists at CDRI, Lucknow. Better awareness, increased "
  "medically assisted deliveries and better post-natal care leading to decreased MMR and IMR indicate improved "
  "reproductive health. NCERT speaks of motivating smaller families and incentives to couples with small "
  "families; it mentions no compulsory sterilisation.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - not in NCERT; sterilisation is a voluntary terminal "
   "method"],
  "Reproductive Health - Problems and Strategies",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (e) only", "(c), (d) and (e) only"],
  why="(e) is not among NCERT's measures (it speaks of motivation and incentives), so every option containing (e) "
      "is wrong; the remaining four are all NCERT statements.", secs=55)

# ================================================================ Evolution (5/7/5)
_n, _q = 250, F(1, 5)
_A_copies = 2 * _n * (1 - _q)
assert _A_copies == 400
Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "A population of 250 diploid individuals is being studied for a gene with two alleles, A and a. The frequency "
  "of allele a in the gene pool is 0.2. How many copies of allele A are present in the gene pool of this population "
  "for this gene?",
  "Gene pool and allele frequency",
  "NCERT: the gene pool is the total genes and their alleles in a population, and the sum total of all allelic "
  "frequencies is 1. Each diploid individual carries two copies of the gene, so the gene pool holds 2 × 250 = 500 "
  "copies. The frequency of A is 1 - 0.2 = 0.8, so the number of A copies is 0.8 × 500 = 400.",
  ["Copies of the gene = 2 × 250 = 500", "p = 1 - q = 0.8", "A copies = 0.8 × 500 = 400"],
  "Hardy-Weinberg Principle",
  at="A", correct="400",
  wrong=["200", "100", "160"],
  why="200 forgets that each individual carries two copies; 100 is the number of copies of allele a; 160 is the "
      "expected number of AA individuals (0.64 × 250), not of A alleles.",
  short="Copies of an allele = 2N × its frequency.", secs=40, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", B, D,
  "Ernst Haeckel proposed embryological support for evolution based on features common to vertebrate embryos. "
  "Who, according to NCERT, disapproved of this proposal on careful study, noting that embryos never pass through "
  "the adult stages of other animals?",
  "Embryological evidence",
  "NCERT: embryological support for evolution was proposed by Ernst Haeckel based upon the observation of certain "
  "features during the embryonic stage common to all vertebrates that are absent in the adult (e.g. a row of "
  "vestigial gill slits). This proposal was disapproved on careful study performed by Karl Ernst von Baer, who "
  "noted that embryos never pass through the adult stages of other animals.",
  ["Haeckel: proposed embryological support", "von Baer: disapproved it"],
  "What are the Evidences for Evolution?",
  at="B", correct="Karl Ernst von Baer",
  wrong=["Louis Pasteur", "Hugo de Vries", "Alfred Wallace"],
  why="Pasteur disproved spontaneous generation; de Vries proposed mutation from his work on evening primrose; "
      "Wallace reached conclusions similar to Darwin's in the Malay Archipelago. None of them tested Haeckel's "
      "proposal.", secs=25)

Z(EVO, "Evidences of evolution", B, D,
  "Similarities in proteins and genes performing a given function among diverse organisms are used as evidence of "
  "evolution. According to NCERT, what do these similarities indicate?",
  "Biochemical evidence",
  "NCERT: similarities in proteins and genes performing a given function among diverse organisms give clues to "
  "common ancestry. These biochemical similarities point to the same shared ancestry as structural similarities "
  "among diverse organisms.",
  ["Similar proteins and genes for a given function", "-> clues to common (shared) ancestry",
   "Same conclusion as structural (anatomical) similarities"],
  "What are the Evidences for Evolution?",
  at="D", correct="They point to the same shared ancestry as structural similarities among diverse organisms",
  wrong=["They show analogy produced only by convergent evolution",
         "They show that the organisms arose by special creation",
         "They show that the proteins were acquired through use and disuse"],
  why="NCERT treats these biochemical similarities as clues to common ancestry, not as analogy; special creation "
      "and use and disuse (Lamarck) are not what NCERT draws from them.", secs=25)

Z(EVO, "Human evolution", B, STP,
  SP("Fossils of Homo erectus were discovered in Java in 1891.",
     "Neanderthal man used hides to protect the body and buried their dead."),
  "Homo erectus and Neanderthal man",
  "NCERT: fossils discovered in Java in 1891 revealed the next stage, Homo erectus, about 1.5 mya; Homo erectus had "
  "a large brain of around 900 cc and probably ate meat. The Neanderthal man, with a brain size of 1400 cc, lived in "
  "near east and central Asian countries; they used hides to protect their body and buried their dead.",
  ["Statement I: true", "Statement II: true"],
  "Origin and Evolution of Man", ans="A",
  why="Both statements are NCERT's account, so every option calling either of them false is wrong.", secs=25)

Z(EVO, "Origin of life", B, ASR,
  AR("Louis Pasteur's experiments dismissed the theory of spontaneous generation.",
     "Pasteur showed that in pre-sterilised flasks life did not come from killed yeast, while in another flask "
     "open to air new living organisms arose from the 'killed yeast'."),
  "Pasteur and spontaneous generation",
  "NCERT: earlier it was believed that life came out of decaying and rotting matter like straw and mud "
  "(spontaneous generation). Louis Pasteur, by careful experimentation, demonstrated that life comes only from "
  "pre-existing life: in pre-sterilised flasks life did not come from killed yeast, while in another flask open to "
  "air new living organisms arose from killed yeast. Spontaneous generation theory was dismissed once and for all. "
  "The experiment in R is the reason A happened.",
  ["A: true", "R: true", "R is the experimental result that dismissed the theory"],
  "Origin of Life",
  ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R describes the very "
      "experiment that dismissed spontaneous generation, so it explains A.", secs=35)

_cave, _agri = 18000, 10000
assert _cave - _agri == 8000
Z(EVO, "Human evolution", I, NUM,
  "According to NCERT, pre-historic cave art developed about 18,000 years ago, and agriculture came around 10,000 "
  "years back, when human settlements started. About how many years separated the development of cave art from "
  "the coming of agriculture?",
  "Timeline of modern humans",
  "NCERT: pre-historic cave art developed about 18,000 years ago; agriculture came around 10,000 years back and "
  "human settlements started. Both are given as 'years ago', so the gap is 18,000 - 10,000 = 8,000 years, with "
  "cave art coming first.",
  ["Cave art: about 18,000 years ago", "Agriculture: about 10,000 years ago", "Gap = 18,000 - 10,000 = 8,000 years"],
  "Origin and Evolution of Man",
  at="C", correct="About 8,000 years",
  wrong=["About 28,000 years", "About 80,000 years", "About 1,800 years"],
  why="28,000 adds two 'years ago' figures instead of subtracting them; 80,000 and 1,800 slip a factor of ten "
      "(the difference multiplied by ten, and the cave-art date divided by ten).",
  short="For two 'years ago' dates, the gap is the difference.", secs=35, vb=RECOMPUTED)

Z(EVO, "Origin of life", I, MUL,
  MS("Which of the following are connotations of the theory of special creation, as stated in NCERT?",
     ["All living organisms (species or types) that we see today were created as such.",
      "The diversity was always the same since creation and will be the same in future also.",
      "The earth is about 4000 years old.",
      "Present-day species arose by natural selection of heritable variations.",
      "Life came out of decaying and rotting matter like straw and mud."]),
  "Theory of special creation",
  "NCERT: the theory of special creation has three connotations: one, that all living organisms (species or types) "
  "that we see today were created as such; two, that the diversity was always the same since creation and will be "
  "the same in future also; and three, that the earth is about 4000 years old. Natural selection is Darwin's idea, "
  "and life from rotting matter is spontaneous generation.",
  ["(a), (b), (c): the three connotations", "(d): Darwinism", "(e): spontaneous generation"],
  "Evolution of Life Forms - A Theory",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(a) and (d) only", "(b), (c) and (d) only"],
  why="(d) is the opposite of special creation and (e) is the theory of spontaneous generation, so every option "
      "containing either is wrong; all three of (a), (b) and (c) are needed.", secs=40)

Z(EVO, "Natural selection", I, D,
  "NCERT notes that excess use of herbicides and pesticides has resulted only in the selection of resistant "
  "varieties in a much lesser time scale. To which other case does NCERT say this is also true?",
  "Evolution by anthropogenic action",
  "NCERT: excess use of herbicides, pesticides, etc., has only resulted in selection of resistant varieties in a "
  "much lesser time scale. This is also true for microbes against which we employ antibiotics or drugs against "
  "eukaryotic organisms/cells. Hence, resistant organisms/cells are appearing in a time scale of months or years "
  "and not centuries. These are examples of evolution by anthropogenic action.",
  ["Herbicides/pesticides -> resistant varieties quickly",
   "Same for microbes and antibiotics, and drugs against eukaryotic cells", "Time scale: months or years"],
  "Evolution by Natural Selection",
  at="D", correct="Microbes against which we employ antibiotics, and eukaryotic organisms/cells against which we "
                  "use drugs",
  wrong=["Darwin's finches of the Galapagos Islands", "The marsupials of Australia",
         "The forelimbs of whales, bats, cheetahs and humans"],
  why="Darwin's finches and the Australian marsupials are NCERT's examples of adaptive radiation over long periods; "
      "vertebrate forelimbs are homologous organs, an anatomical evidence, not resistance arising from human "
      "action.", secs=30)

Z(EVO, "Origin of life", I, ASR,
  AR("NCERT describes the origin of life as a unique event in the history of the universe.",
     "Life appeared on the earth about one billion years after the earth was formed."),
  "When life appeared",
  "NCERT: the origin of life is considered a unique event in the history of the universe. The earth was formed "
  "about 4.5 billion years back, and life appeared 500 million years after the formation of the earth, i.e. "
  "almost four billion years back. R doubles that interval, so A is true and R is false.",
  ["A: true", "R: false - life appeared about 500 million years after the earth formed"],
  "Origin of Life", ans="C",
  why="R gives one billion years instead of NCERT's 500 million, so options treating R as true are wrong; A is "
      "NCERT's own statement, so 'A is false' is wrong.", secs=35)

Z(EVO, "Origin of life", I, STP,
  SP("The first mammals were large animals, like elephants.",
     "Mammals were viviparous and protected their unborn young inside the mother's body."),
  "Early mammals",
  "NCERT: the first mammals were like shrews; their fossils are small sized. Mammals were viviparous and protected "
  "their unborn young inside the mother's body; they were also more intelligent in sensing and avoiding danger, at "
  "least.",
  ["Statement I: false - the first mammals were like shrews", "Statement II: true"],
  "A Brief Account of Evolution", ans="D",
  why="Statement I is false because NCERT compares the first mammals to shrews, so options calling it true are "
      "wrong; Statement II is NCERT's description, so options calling it false are wrong.", secs=30)

Z(EVO, "Origin of life", I, D,
  "Which sequence of events agrees with NCERT's account of the Big Bang theory of the origin of the universe?",
  "Big Bang and the formation of galaxies",
  "NCERT: the Big Bang theory talks of a singular huge explosion unimaginable in physical terms. The universe "
  "expanded and hence the temperature came down. Hydrogen and helium formed sometime later. The gases condensed "
  "under gravitation and formed the galaxies of the present-day universe. In the solar system of the Milky Way "
  "galaxy, the earth was formed about 4.5 billion years back.",
  ["Explosion -> expansion and cooling", "-> hydrogen and helium formed", "-> gases condensed under gravitation",
   "-> galaxies"],
  "Origin of Life",
  at="B", correct="Huge explosion → expansion and fall in temperature → formation of hydrogen and helium → "
                  "condensation of gases under gravitation to form galaxies",
  wrong=["Formation of galaxies → huge explosion → formation of hydrogen and helium → expansion and fall in "
         "temperature",
         "Huge explosion → condensation of gases under gravitation to form galaxies → expansion and fall in "
         "temperature → formation of hydrogen and helium",
         "Formation of hydrogen and helium → huge explosion → contraction and rise in temperature → formation of "
         "galaxies"],
  why="Galaxies formed last, from gases that condensed after hydrogen and helium had formed, so options placing "
      "galaxies before or at the explosion are wrong; NCERT describes expansion and cooling, not contraction and "
      "heating.", secs=35)

Z(EVO, "Darwinism and modern synthesis", I, MAT,
  ML(("scientist", "what NCERT links with the scientist"),
     ["Charles Darwin", "Hugo de Vries", "Louis Pasteur", "Alfred Wallace"],
     ["Malay Archipelago", "Evening primrose", "Sea voyage round the world in H.M.S. Beagle",
      "Killed yeast in pre-sterilised flasks"]),
  "Scientists in the history of evolutionary thought",
  "NCERT: Darwin's conclusions were based on observations made during a sea voyage in the sailing ship H.M.S. "
  "Beagle round the world. Hugo de Vries, based on his work on evening primrose, brought forth the idea of "
  "mutations. Louis Pasteur showed with killed yeast in pre-sterilised flasks that life comes only from "
  "pre-existing life. Alfred Wallace, a naturalist who worked in the Malay Archipelago, came to similar conclusions "
  "as Darwin around the same time.",
  ["A Darwin -> III", "B de Vries -> II", "C Pasteur -> IV", "D Wallace -> I"],
  "Evolution by Natural Selection; Origin of Life",
  at="D", match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"}]),
  why="Wallace, not Darwin, worked in the Malay Archipelago; de Vries worked on evening primrose and Pasteur on "
      "killed yeast, so swapping them is wrong.", secs=40)

_qq = 1 - F(91, 100)
_q3 = F(3, 10)
assert _q3 * _q3 == _qq
_p3 = 1 - _q3
assert (_p3 * _p3) / (2 * _p3 * _q3) == F(7, 6)
Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population in Hardy-Weinberg equilibrium for a gene with a dominant allele A and a recessive allele a, "
  "91% of the individuals show the dominant phenotype. What is the ratio of homozygous dominant (AA) to "
  "heterozygous (Aa) individuals in this population?",
  "Genotype frequencies from a phenotype frequency",
  "In Hardy-Weinberg equilibrium the genotype frequencies are p², 2pq and q² (p² + 2pq + q² = 1). The recessive "
  "phenotype shows only in aa, so q² = 1 - 0.91 = 0.09 and q = 0.3; p = 1 - 0.3 = 0.7. Then AA = p² = 0.49 and "
  "Aa = 2pq = 2 × 0.7 × 0.3 = 0.42, giving AA : Aa = 0.49 : 0.42 = 7 : 6.",
  ["q² = 1 - 0.91 = 0.09 -> q = 0.3", "p = 0.7", "AA = p² = 0.49; Aa = 2pq = 0.42", "Ratio = 49 : 42 = 7 : 6"],
  "Hardy-Weinberg Principle",
  at="B", correct="7 : 6",
  wrong=["49 : 9", "7 : 3", "1 : 1"],
  why="49 : 9 is AA : aa; 7 : 3 is the ratio of the allele frequencies p : q, not of genotypes; 1 : 1 assumes "
      "the dominant phenotype is split equally between AA and Aa.",
  short="AA : Aa = p² : 2pq = p : 2q = 0.7 : 0.6.", secs=75, vb=RECOMPUTED)

Z(EVO, "Darwinism and modern synthesis", A, MUL,
  MS("Which of the following ideas belong to Darwin's theory of evolution as described in NCERT?",
     ["Any population has built-in variation in characteristics.",
      "Fitness ultimately and only refers to reproductive fitness: those better fit in an environment leave more "
      "progeny than others.",
      "Characters developed by the use of organs during an individual's life are passed on, as in the long neck "
      "of the giraffe.",
      "New species arise by single-step large mutations (saltation).",
      "Existing living forms share similarities, to varying degrees, with life forms that existed millions of "
      "years ago."]),
  "Darwin versus Lamarck and de Vries",
  "NCERT: Darwin concluded that existing living forms share similarities to varying degrees not only among "
  "themselves but also with life forms that existed millions of years ago; that any population has built-in "
  "variation in characteristics; and that fitness ultimately and only refers to reproductive fitness. Evolution "
  "driven by the use and disuse of organs (giraffe's neck) was Lamarck's idea, and single-step large mutation "
  "(saltation) was de Vries's.",
  ["(a) Darwin", "(b) Darwin", "(c) Lamarck", "(d) de Vries", "(e) Darwin"],
  "Evolution by Natural Selection; Mechanism of Evolution",
  at="A", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="(c) is Lamarck's use and disuse and (d) is de Vries's saltation, so every option including either is "
      "wrong; the correct option keeps all three of Darwin's ideas.", secs=50)

Z(EVO, "Darwinism and modern synthesis", A, MAT,
  ML(("term", "meaning, as used in NCERT"),
     ["Saltation", "Fitness (Darwin)", "Genetic equilibrium", "Adaptive radiation"],
     ["Reproductive fitness: those better fit leave more progeny",
      "Allele frequencies stable, so the gene pool remains a constant",
      "Evolution of different species in a given geographical area starting from a point and radiating to other "
      "habitats",
      "Single-step large mutation"]),
  "Evolutionary terms",
  "NCERT: de Vries believed mutation causes evolution, and single-step large mutation is called saltation. "
  "Darwin's fitness ultimately and only refers to reproductive fitness. When allele frequencies are stable, the "
  "gene pool remains a constant; this is called genetic equilibrium. Adaptive radiation is the process of evolution "
  "of different species in a given geographical area starting from a point and literally radiating to other areas "
  "of geography (habitats).",
  ["A saltation -> IV", "B fitness -> I", "C genetic equilibrium -> II", "D adaptive radiation -> III"],
  "Mechanism of Evolution; Hardy-Weinberg Principle; Adaptive Radiation",
  at="C", match=({"A": "IV", "B": "I", "C": "II", "D": "III"},
                 [{"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "I", "B": "IV", "C": "II", "D": "III"}]),
  why="Saltation is a single large mutation, not radiation into habitats; Darwin's fitness concerns leaving more "
      "progeny, while a constant gene pool is genetic equilibrium; and fitness is not a mutation.", secs=50)

Z(EVO, "Evidences of evolution", A, ASR,
  AR("Analogous structures indicate common ancestry of the organisms that have them.",
     "Analogous structures are a result of convergent evolution, in which different structures evolve for the same "
     "function."),
  "Analogy versus homology",
  "NCERT: analogous structures are not anatomically similar though they perform similar functions (e.g. wings of "
  "butterfly and of birds); they are a result of convergent evolution, where different structures evolve for the "
  "same function and hence have similarity. It is homology, a result of divergent evolution, that indicates "
  "common ancestry. So A is false and R is true.",
  ["A: false - homology, not analogy, indicates common ancestry", "R: true - analogy arises by convergent evolution"],
  "What are the Evidences for Evolution?", ans="D",
  why="A gives analogous structures the meaning of homologous ones, so options calling A true are wrong; R is "
      "NCERT's own explanation of analogy, so 'A is false but R is true' is the answer.", secs=40)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "In which of the following situations does the allele frequency of a population change mainly through GENETIC "
  "DRIFT, as NCERT defines it?",
  "Genetic drift as a chance change",
  "NCERT: gene flow is the change in gene frequencies caused by migration of a section of a population to another "
  "place and population. If the same change occurs by chance, it is called genetic drift. Natural selection acts on "
  "heritable variation that enables better survival and reproduction, and mutation produces new variation. A "
  "landslide that kills individuals at random, irrespective of genotype, changes allele frequencies by chance.",
  ["Migration -> gene flow", "Chance -> genetic drift", "Better survival of a variant -> natural selection",
   "New allele -> mutation"],
  "Hardy-Weinberg Principle",
  at="C", correct="A landslide kills half of a small population at random, irrespective of genotype, and the "
                  "allele frequencies of the survivors happen to differ from those before",
  wrong=["Excessive use of a pesticide leaves mostly resistant insects, whose numbers then increase",
         "Individuals of a neighbouring population repeatedly migrate in and interbreed",
         "A new allele appears in a gamete and is passed on to the offspring"],
  why="Pesticide resistance spreading is natural selection; repeated migration with interbreeding is gene flow; a "
      "new allele arising in a gamete is mutation. Only the random deaths change frequencies purely by chance.",
  secs=50)

# ================================================================ Human Health and Disease (6/9/6)
Z(HHD, "Drug and alcohol abuse", B, D,
  "According to NCERT, in which ways is tobacco used by human beings?",
  "Forms of tobacco use",
  "NCERT: tobacco has been used by human beings for more than 400 years. It is smoked, chewed or used as a snuff. "
  "Tobacco contains a large number of chemical substances, including nicotine, an alkaloid.",
  ["Smoked", "Chewed", "Used as a snuff"],
  "Drugs and Alcohol Abuse",
  at="A", correct="It is smoked, chewed or used as a snuff",
  wrong=["It is only smoked; chewing tobacco is not described",
         "It is taken only by intravenous injection",
         "It is used only as an ointment applied to the skin"],
  why="NCERT names chewing (linked to oral cancer) and snuff as well as smoking; injection is described for drugs "
      "like heroin, not tobacco; and NCERT does not mention tobacco ointments.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "In malaria, the chill and high fever recur every three to four days. According to NCERT, this is due to the "
  "release of a toxic substance called:",
  "Cause of malarial fever",
  "NCERT: Plasmodium multiplies within the liver cells and then attacks the red blood cells (RBCs), resulting in "
  "their rupture. The ruptured RBCs release a toxic substance, haemozoin, which is responsible for the chill and "
  "high fever recurring every three to four days.",
  ["Liver cells -> RBCs attacked and ruptured", "Haemozoin released -> chill and high fever every 3-4 days"],
  "Common Diseases in Humans",
  at="C", correct="Haemozoin",
  wrong=["Histamine", "Interferon", "Serotonin"],
  why="Histamine and serotonin are released from mast cells in allergy; interferons are proteins secreted by "
      "virus-infected cells that protect non-infected cells. None is the malarial toxin.", secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "According to NCERT, what has modern-day life style done that results in more and more children in the metro "
  "cities of India suffering from allergies and asthma?",
  "Life style and allergy",
  "NCERT: somehow, modern-day life style has resulted in lowering of immunity and more sensitivity to allergens; "
  "more and more children in metro cities of India suffer from allergies and asthma due to sensitiveness to the "
  "environment.",
  ["Modern life style -> lower immunity + more sensitivity to allergens", "-> allergies and asthma in children"],
  "Immunity (Allergies)",
  at="B", correct="It has lowered immunity and increased sensitivity to allergens",
  wrong=["It has made the thymus larger in children", "It has removed all allergens from the environment",
         "It has stopped the production of IgE antibodies"],
  why="NCERT says the thymus reduces in size with age and does not link it to life style; allergens such as dust "
      "and pollen remain in the environment; and IgE antibodies are what produce allergic reactions, so stopping "
      "them would reduce allergy, not increase it.", secs=25)

Z(HHD, "Immunity and vaccines", B, STP,
  SP("When the body encounters a pathogen for the first time, it produces a primary response of low intensity.",
     "A subsequent encounter with the same pathogen elicits a highly intensified secondary or anamnestic response."),
  "Primary and secondary immune responses",
  "NCERT: our body, when it encounters a pathogen for the first time, produces a response called the primary "
  "response, which is of low intensity. Subsequent encounter with the same pathogen elicits a highly intensified "
  "secondary or anamnestic response. This is ascribed to the fact that our body appears to have memory of the "
  "first encounter.",
  ["Statement I: true - primary response, low intensity", "Statement II: true - secondary (anamnestic), intensified"],
  "Immunity (Acquired Immunity)", ans="A",
  why="Both statements are NCERT's own, so every option calling either false is wrong.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, ASR,
  AR("Cocaine is commonly called coke or crack.",
     "Cocaine interferes with the transport of the neurotransmitter dopamine."),
  "Cocaine",
  "NCERT: coca alkaloid or cocaine is obtained from the coca plant Erythroxylum coca, native to South America. It "
  "interferes with the transport of the neurotransmitter dopamine. Cocaine, commonly called coke or crack, is "
  "usually snorted. Both statements are true, but the drug's street names have nothing to do with its action on "
  "dopamine.",
  ["A: true", "R: true", "R is its mode of action; A is its common name -> unrelated"],
  "Drugs and Alcohol Abuse", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; how cocaine acts on dopamine "
      "transport does not explain what it is commonly called, so R is not the explanation.", secs=25)

Z(HHD, "Pathogens and diseases", B, D,
  "Rhinoviruses cause the common cold, with nasal congestion and discharge, sore throat, hoarseness, cough, "
  "headache and tiredness. According to NCERT, these symptoms usually last for:",
  "Common cold",
  "NCERT: rhinoviruses infect the nose and respiratory passage but not the lungs. The common cold is characterised "
  "by nasal congestion and discharge, sore throat, hoarseness, cough, headache, tiredness, etc., which usually last "
  "for 3–7 days.",
  ["Rhinovirus -> nose and respiratory passage (not lungs)", "Symptoms usually last 3–7 days"],
  "Common Diseases in Humans",
  at="D", correct="3–7 days",
  wrong=["3–5 days", "5–10 years", "12–18 years"],
  why="3–5 days is the duration of menstrual flow; 5–10 years is the usual time-lag between HIV infection and "
      "AIDS symptoms; 12–18 years is NCERT's adolescence period.", secs=20)

Z(HHD, "Pathogens and diseases", I, MAT,
  ML(("disease", "feature in severe or chronic cases, as described in NCERT"),
     ["Typhoid", "Pneumonia", "Ascariasis", "Filariasis"],
     ["Lips and finger nails may turn grey to bluish in colour",
      "Intestinal perforation and death may occur",
      "Gross deformities, with the genital organs also often affected",
      "Blockage of the intestinal passage, with internal bleeding and anaemia"]),
  "Severe features of common diseases",
  "NCERT: in typhoid, intestinal perforation and death may occur in severe cases. In severe cases of pneumonia, "
  "the lips and finger nails may turn grey to bluish in colour. Symptoms of ascariasis include internal bleeding, "
  "muscular pain, fever, anaemia and blockage of the intestinal passage. In filariasis the worms cause chronic "
  "inflammation of the organs in which they live for many years; the genital organs are also often affected, "
  "resulting in gross deformities.",
  ["A typhoid -> II", "B pneumonia -> I", "C ascariasis -> IV", "D filariasis -> III"],
  "Common Diseases in Humans",
  at="D", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"}]),
  why="Bluish lips and nails reflect pneumonia's effect on the lungs, not typhoid; gross deformities belong to "
      "filariasis and intestinal blockage to the roundworm Ascaris; typhoid, not ascariasis, can cause intestinal "
      "perforation.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, MUL,
  MS("Which of the following does NCERT give as causes that motivate youth towards drug and alcohol use?",
     ["Curiosity, need for adventure and excitement, and experimentation",
      "The urge to escape facing problems and failures",
      "Stress from pressure to excel in academics or examinations",
      "The perception that it is 'cool' or progressive to smoke or use drugs or alcohol, promoted by television, "
      "movies, newspapers and the internet",
      "Avoiding undue peer pressure"]),
  "Why adolescents take to drugs",
  "NCERT: curiosity, need for adventure and excitement, and experimentation constitute common causes; children may "
  "also use drugs and alcohol to escape facing problems and failures; stress from pressure to excel in academics "
  "or examinations has played a significant role; the perception that it is 'cool' or progressive, promoted by "
  "television, movies, newspapers and the internet, is another factor; and unstable or unsupportive family "
  "structures and peer pressure also contribute. 'Avoiding undue peer pressure' is a PREVENTION measure.",
  ["(a)-(d): causes", "(e): a prevention measure, not a cause"],
  "Adolescence and Drug/Alcohol Abuse",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (e) only", "(b), (c) and (d) only"],
  why="(e) is listed by NCERT among ways to prevent drug abuse, so every option with (e) is wrong; '(b), (c) and (d) "
      "only' leaves out curiosity and experimentation, which NCERT calls common causes.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, D,
  "According to NCERT, the chronic use of drugs and alcohol damages which of the following?",
  "Long-term effects of alcohol and drugs",
  "NCERT: the chronic use of drugs and alcohol damages the nervous system and the liver (cirrhosis). The use of "
  "drugs and alcohol during pregnancy is also known to adversely affect the foetus.",
  ["Chronic use -> nervous system damage", "-> liver damage (cirrhosis)"],
  "Effects of Drug/Alcohol Abuse",
  at="A", correct="The nervous system and the liver (cirrhosis)",
  wrong=["Only the lymph nodes and the spleen", "Only the skin, as dry scaly lesions",
         "Only the alveoli of the lungs, which fill with fluid"],
  why="Effects on lymphoid organs are not what NCERT describes; dry scaly skin lesions are ringworm; fluid-filled "
      "alveoli are pneumonia. NCERT names the nervous system and the liver.", secs=25)

Z(HHD, "Drug and alcohol abuse", I, ASR,
  AR("Those who take drugs intravenously are much more likely to acquire serious infections like AIDS and hepatitis "
     "B.",
     "The viruses responsible for these diseases are transferred from one person to another by sharing of infected "
     "needles and syringes."),
  "Intravenous drug use and infection",
  "NCERT: those who take drugs intravenously (direct injection into the vein using a needle and syringe) are much "
  "more likely to acquire serious infections like AIDS and hepatitis B. The viruses responsible for these diseases "
  "are transferred from one person to another by sharing of infected needles and syringes. R is the route that "
  "puts intravenous users at higher risk, so it explains A.",
  ["A: true", "R: true", "Shared infected needles carry the viruses -> higher risk"],
  "Effects of Drug/Alcohol Abuse", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT gives needle sharing as "
      "the way the viruses pass between intravenous users, so R explains A.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Hashish, charas and ganja are obtained from the coca plant Erythroxylum coca.",
     "Marijuana, hashish, charas and ganja are known for their effects on the cardiovascular system of the body."),
  "Cannabinoids",
  "NCERT: natural cannabinoids are obtained from the inflorescences of the plant Cannabis sativa. The flower tops, "
  "leaves and resin of the cannabis plant are used in various combinations to produce marijuana, hashish, charas "
  "and ganja; generally taken by inhalation and oral ingestion, these are known for their effects on the "
  "cardiovascular system. Erythroxylum coca is the source of cocaine.",
  ["Statement I: false - from Cannabis sativa", "Statement II: true"],
  "Drugs and Alcohol Abuse", ans="D",
  why="Statement I gives the source of cocaine for the cannabinoids, so options calling it true are wrong; "
      "Statement II is NCERT's description, so options calling it false are wrong.", secs=30)

Z(HHD, "Pathogens and diseases", I, D,
  "Salmonella typhi causes typhoid fever. According to NCERT, how does the pathogen generally enter the body and "
  "reach other organs?",
  "Route of Salmonella typhi",
  "NCERT: Salmonella typhi is a pathogenic bacterium which causes typhoid fever in human beings. These pathogens "
  "generally enter the small intestine through food and water contaminated with them and migrate to other organs "
  "through blood.",
  ["Contaminated food/water -> small intestine", "-> migrate to other organs through blood"],
  "Common Diseases in Humans",
  at="B", correct="It enters the small intestine through contaminated food and water and migrates to other organs "
                  "through blood",
  wrong=["It enters the lungs through droplets and stays confined to the alveoli",
         "It is injected by the bite of a female Anopheles mosquito and multiplies in the liver cells",
         "It enters through the skin from soil and stays in the skin folds"],
  why="Droplets and alveoli describe pneumonia; the mosquito bite and liver multiplication describe Plasmodium; "
      "entry from soil and skin folds describe ringworm fungi.", secs=30)

Z(HHD, "Cancer", I, MAT,
  ML(("term", "meaning, as used in NCERT"),
     ["Contact inhibition", "Metastasis", "Neoplastic cells", "Biological response modifiers"],
     ["Cells sloughed from tumours reach distant sites through blood and start new tumours there",
      "Substances such as α-interferon that activate the immune system to help destroy the tumour",
      "The property by which contact with other cells inhibits uncontrolled growth; lost by cancer cells",
      "The proliferating cells of malignant tumours"]),
  "Cancer terms",
  "NCERT: in normal cells, contact with other cells inhibits their uncontrolled growth, a property called contact "
  "inhibition; cancer cells appear to have lost it. Malignant tumours are a mass of proliferating cells called "
  "neoplastic or tumour cells. Cells sloughed from such tumours reach distant sites through blood and start new "
  "tumours wherever they get lodged; this property is called metastasis. Patients are given substances called "
  "biological response modifiers such as α-interferon, which activate their immune system and help in destroying "
  "the tumour.",
  ["A -> III", "B -> I", "C -> IV", "D -> II"],
  "Cancer",
  at="A", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"}]),
  why="Contact inhibition is a property of normal cells, not the spread of tumour cells; metastasis is the "
      "spreading, not the name of the tumour cells themselves; and neoplastic cells are not immune-activating "
      "substances.", secs=45)

Z(HHD, "Pathogens and diseases", I, MUL,
  MS("Which of the following statements about health are correct, according to NCERT?",
     ["Health is a state of complete physical, mental and social well-being.",
      "Health is affected by genetic disorders, infections and life style.",
      "Balanced diet, personal hygiene and regular exercise are very important to maintain good health.",
      "Proper disposal of wastes, control of vectors and maintenance of hygienic food and water resources are "
      "necessary for achieving good health.",
      "Health simply means the absence of disease or physical fitness."]),
  "Meaning of health",
  "NCERT: health does not simply mean 'absence of disease' or 'physical fitness'; it can be defined as a state of "
  "complete physical, mental and social well-being. Health is affected by genetic disorders, infections and life "
  "style. Balanced diet, personal hygiene and regular exercise are very important to maintain good health, and "
  "awareness about diseases, vaccination, proper disposal of wastes, control of vectors and maintenance of hygienic "
  "food and water resources are necessary for achieving good health.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - NCERT rejects this narrow meaning"],
  "Human Health and Disease (introduction)",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (c) and (e) only", "(a) and (e) only"],
  why="NCERT explicitly says health does not simply mean absence of disease or physical fitness, so every option "
      "containing (e) is wrong; the correct option keeps all four NCERT statements.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, ASR,
  AR("Heroin, commonly called smack, is obtained by the acetylation of morphine.",
     "Morphine is extracted from the inflorescences of the plant Cannabis sativa."),
  "Source of opioids",
  "NCERT: heroin, commonly called smack, is chemically diacetylmorphine, a white, odourless, bitter crystalline "
  "compound obtained by acetylation of morphine, which is extracted from the latex of the poppy plant Papaver "
  "somniferum. Cannabis sativa inflorescences are the source of natural cannabinoids. A is true and R is false.",
  ["A: true", "R: false - morphine comes from the latex of Papaver somniferum"],
  "Drugs and Alcohol Abuse", ans="C",
  why="R names the cannabinoid plant as the source of morphine, so options treating R as true are wrong; A is "
      "NCERT's description of heroin, so 'A is false' is wrong.", secs=30)

Z(HHD, "Drug and alcohol abuse", A, MUL,
  MS("Which of the following statements about addiction and dependence are correct, according to NCERT?",
     ["Addiction is a psychological attachment to certain effects, such as euphoria and a temporary feeling of "
      "well-being, associated with drugs and alcohol.",
      "With repeated use of drugs, the tolerance level of the receptors present in the body increases.",
      "Consequently, the receptors respond only to higher doses of drugs or alcohol, leading to greater intake.",
      "Dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal syndrome if "
      "the regular dose is abruptly discontinued.",
      "Withdrawal symptoms are always mild, so medical supervision is never needed."]),
  "Addiction and dependence",
  "NCERT: addiction is a psychological attachment to certain effects such as euphoria and a temporary feeling of "
  "well-being associated with drugs and alcohol. With repeated use, the tolerance level of the receptors present "
  "in our body increases; consequently the receptors respond only to higher doses, leading to greater intake and "
  "addiction. Dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal "
  "syndrome if the regular dose is abruptly discontinued; in some cases withdrawal symptoms can be severe and even "
  "life threatening, and the person may need medical supervision.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - can be severe, even life threatening"],
  "Addiction and Dependence",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (e) only"],
  why="(e) contradicts NCERT's statement that withdrawal can be severe and even life threatening, so every option "
      "with (e) is wrong; (a)-(d) are all NCERT statements.", secs=55)

Z(HHD, "Drug and alcohol abuse", A, MAT,
  ML(("drug or drug group", "NCERT description"),
     ["Heroin", "Cocaine", "Cannabinoids", "Barbiturates, amphetamines and benzodiazepines"],
     ["Known for their effects on the cardiovascular system",
      "Normally used as medicines to help patients cope with mental illnesses like depression and insomnia, but "
      "often abused",
      "A depressant that slows down body functions",
      "Potent stimulating action on the central nervous system, producing a sense of euphoria and increased energy"]),
  "Commonly abused drugs",
  "NCERT: heroin is a depressant and slows down body functions. Cocaine has a potent stimulating action on the "
  "central nervous system, producing a sense of euphoria and increased energy. Cannabinoids (marijuana, hashish, "
  "charas, ganja) are known for their effects on the cardiovascular system. Drugs like barbiturates, amphetamines "
  "and benzodiazepines are normally used as medicines to help patients cope with mental illnesses like depression "
  "and insomnia, but are often abused.",
  ["A heroin -> III", "B cocaine -> IV", "C cannabinoids -> I", "D barbiturates etc. -> II"],
  "Drugs and Alcohol Abuse",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Heroin is a depressant and cocaine a stimulant, so swapping them is wrong; the cardiovascular effects belong "
      "to cannabinoids, while the medicinal use for depression and insomnia belongs to barbiturates, amphetamines "
      "and benzodiazepines.", secs=50)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Mucosa-associated lymphoid tissue (MALT) constitutes about 50 per cent of the lymphoid tissue in the human "
     "body.",
     "MALT is located only within the lining of the digestive tract."),
  "Mucosa-associated lymphoid tissue",
  "NCERT: there is lymphoid tissue also located within the lining of the major tracts (respiratory, digestive and "
  "urogenital tracts), called mucosa-associated lymphoid tissue (MALT). It constitutes about 50 per cent of the "
  "lymphoid tissue in the human body. R restricts it to the digestive tract, so R is false while A is true.",
  ["A: true - about 50 per cent", "R: false - respiratory, digestive and urogenital tracts"],
  "Immunity (Lymphoid Organs)", ans="C",
  why="R leaves out the respiratory and urogenital tracts, so options treating R as true are wrong; A is NCERT's "
      "figure, so 'A is false' is wrong.", secs=35)

Z(HHD, "Cancer", A, STP,
  SP("Cancer-causing viruses, called oncogenic viruses, have genes called viral oncogenes.",
     "Several chemotherapeutic drugs are used to kill cancerous cells, and some of these are specific for particular "
     "tumours."),
  "Oncogenic viruses and chemotherapy",
  "NCERT: cancer causing viruses called oncogenic viruses have genes called viral oncogenes; several genes called "
  "cellular oncogenes (c-onc) or proto-oncogenes have also been identified in normal cells which, when activated "
  "under certain conditions, could lead to oncogenic transformation. In treatment, several chemotherapeutic drugs "
  "are used to kill cancerous cells; some of these are specific for particular tumours, and the majority have side "
  "effects such as hair loss and anaemia.",
  ["Statement I: true", "Statement II: true"],
  "Cancer", ans="A",
  why="Both statements are NCERT's own; the trap is reading 'some are specific for particular tumours' as false. "
      "Every option calling either statement false is wrong.", secs=35)

Z(HHD, "Pathogens and diseases", A, D,
  "Which one of the following sets of pathogen, disease and mode of transmission is entirely correct according to "
  "NCERT?",
  "Pathogen-disease-transmission",
  "NCERT: Wuchereria (W. bancrofti and W. malayi), the filarial worms, cause filariasis (elephantiasis) and are "
  "transmitted to a healthy person through the bite by the female mosquito vectors. Entamoeba histolytica causes "
  "amoebiasis and spreads through food and water contaminated by faecal matter (houseflies acting as mechanical "
  "carriers). Ringworm fungi (e.g. Trichophyton) are acquired from soil or by using towels, clothes or even the "
  "comb of infected individuals. Streptococcus pneumoniae causes pneumonia, not typhoid.",
  ["Check each part of the set", "Only the Wuchereria set is right in all three parts"],
  "Common Diseases in Humans",
  at="C", correct="Wuchereria – filariasis – bite of female mosquito vectors",
  wrong=["Entamoeba histolytica – amoebiasis – inhaling droplets released by an infected person",
         "Trichophyton – ringworm – bite of the female Anopheles mosquito",
         "Streptococcus pneumoniae – typhoid – contaminated food and water"],
  why="Amoebiasis is not air-borne; ringworm spreads from soil and shared towels, clothes or combs, not by "
      "mosquitoes; and Streptococcus pneumoniae causes pneumonia, while typhoid is caused by Salmonella typhi.",
  secs=45)

Z(HHD, "Pathogens and diseases", A, D,
  "How many of the following human diseases are caused by bacteria, according to NCERT?\n\nTyphoid, pneumonia, "
  "common cold, dysentery, plague, diphtheria, malaria, ringworm, amoebiasis",
  "Bacterial diseases",
  "NCERT: typhoid (Salmonella typhi) and pneumonia (Streptococcus pneumoniae and Haemophilus influenzae) are "
  "bacterial diseases, and 'dysentery, plague, diphtheria, etc., are some of the other bacterial diseases in man'. "
  "The common cold is viral (rhinoviruses), malaria and amoebiasis are protozoan, and ringworm is fungal.",
  ["Bacterial: typhoid, pneumonia, dysentery, plague, diphtheria = 5", "Viral: common cold",
   "Protozoan: malaria, amoebiasis", "Fungal: ringworm"],
  "Common Diseases in Humans",
  at="B", correct="Five",
  wrong=["Four", "Six", "Seven"],
  why="Four usually leaves out dysentery, which NCERT lists among bacterial diseases; six or seven add the common "
      "cold (viral), ringworm (fungal) or a protozoan disease such as amoebiasis.", secs=50)

# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Restriction enzymes", B, D,
  "According to NCERT, genetic engineering refers to:",
  "Meaning of genetic engineering",
  "NCERT: the two core techniques that enabled the birth of modern biotechnology are genetic engineering and "
  "bioprocess engineering. Genetic engineering: techniques to alter the chemistry of genetic material (DNA and RNA), "
  "to introduce these into host organisms and thus change the phenotype of the host organism.",
  ["Alter the chemistry of DNA/RNA", "Introduce it into a host organism", "-> change the host's phenotype"],
  "Principles of Biotechnology",
  at="B", correct="Techniques to alter the chemistry of genetic material (DNA and RNA), introduce it into host "
                  "organisms and thus change the phenotype of the host",
  wrong=["Maintenance of a sterile ambience to grow only the desired microbe on a large scale",
         "Separation and purification of a product before it is marketed",
         "Traditional hybridisation of plants and animals to combine desirable characters"],
  why="A sterile ambience for large-scale culture is bioprocess engineering; separation and purification is "
      "downstream processing; traditional hybridisation is what genetic engineering improves upon, since it often "
      "carries undesirable genes along with the desired ones.", secs=25)

Z(BPP, "Restriction enzymes", B, D,
  "In its account of the principles of biotechnology, NCERT contrasts asexual and sexual reproduction. Which "
  "statement gives this contrast correctly?",
  "Asexual versus sexual reproduction",
  "NCERT: you have learnt that asexual reproduction preserves the genetic information, while sexual reproduction "
  "permits variation. Traditional hybridisation procedures used in plant and animal breeding very often lead to "
  "inclusion and multiplication of undesirable genes along with the desired genes; genetic engineering allows only "
  "the desired genes to be introduced.",
  ["Asexual reproduction -> preserves genetic information", "Sexual reproduction -> permits variation"],
  "Principles of Biotechnology",
  at="A", correct="Asexual reproduction preserves the genetic information, while sexual reproduction permits "
                  "variation",
  wrong=["Asexual reproduction permits variation, while sexual reproduction preserves the genetic information",
         "Both asexual and sexual reproduction only preserve the genetic information",
         "Both asexual and sexual reproduction always introduce undesirable genes"],
  why="The second option reverses NCERT's contrast; sexual reproduction permits variation, so it does not only "
      "preserve information; and the inclusion of undesirable genes is NCERT's criticism of traditional "
      "hybridisation, not a property of all reproduction.", secs=25)

Z(BPP, "Bioreactors and downstream processing", B, STP,
  SP("The cells harbouring cloned genes of interest may be grown on a small scale in the laboratory.",
     "Such cultures may be used for extracting the desired protein and then purifying it by using different "
     "separation techniques."),
  "Obtaining the foreign gene product",
  "NCERT: the cells harbouring cloned genes of interest may be grown on a small scale in the laboratory. The "
  "cultures may be used for extracting the desired protein and then purifying it by using different separation "
  "techniques. The cells can also be multiplied in a continuous culture system or in bioreactors for large-scale "
  "production.",
  ["Statement I: true", "Statement II: true"],
  "Obtaining the Foreign Gene Product", ans="A",
  why="Both statements are NCERT's own, so every option calling either of them false is wrong.", secs=25)

Z(BPP, "PCR and gel electrophoresis", B, ASR,
  AR("During the isolation of DNA, the preparation is treated with ribonuclease.",
     "Purified DNA ultimately precipitates after the addition of chilled ethanol and can be seen as a collection "
     "of fine threads in the suspension."),
  "Steps in DNA isolation",
  "NCERT: when the cell is broken open, RNA is released along with DNA; RNA can be removed by treatment with "
  "ribonuclease, whereas proteins can be removed by treatment with protease. Other molecules can be removed by "
  "appropriate treatments, and purified DNA ultimately precipitates out after the addition of chilled ethanol. "
  "Both statements are true, but the precipitation by ethanol is a later step and is not why ribonuclease is used.",
  ["A: true - ribonuclease removes RNA", "R: true - chilled ethanol precipitates DNA",
   "R does not explain the use of ribonuclease"],
  "Isolation of the Genetic Material (DNA)", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; ribonuclease is used because "
      "RNA must be removed, which R does not say, so R is not the explanation.", secs=30)

Z(BPP, "Cloning vectors", B, D,
  "The E. coli cloning vector pBR322 shown in NCERT carries two genes that are used as selectable markers. These "
  "genes give resistance to:",
  "Selectable markers of pBR322",
  "NCERT: the figure of pBR322 shows the restriction sites, ori, and the antibiotic resistance genes ampR and tetR "
  "(resistance to ampicillin and tetracycline); rop codes for proteins involved in the replication of the plasmid. "
  "Foreign DNA ligated at the BamHI site of the tetracycline resistance gene, for example, inactivates that gene "
  "while ampicillin resistance remains.",
  ["pBR322 markers: ampR and tetR", "= ampicillin and tetracycline"],
  "Cloning Vectors",
  at="C", correct="Ampicillin and tetracycline",
  wrong=["Ampicillin and kanamycin", "Chloramphenicol and kanamycin", "Tetracycline and chloramphenicol"],
  why="Chloramphenicol and kanamycin are other antibiotics whose resistance genes NCERT calls useful selectable "
      "markers for E. coli in general, but pBR322 carries ampR and tetR.", secs=25)

Z(BPP, "Restriction enzymes", I, MAT,
  ML(("organism or body", "connection with biotechnology described in NCERT"),
     ["Escherichia coli RY 13", "Thermus aquaticus", "Agrobacterium tumefaciens",
      "European Federation of Biotechnology"],
     ["Source of the thermostable DNA polymerase used in PCR",
      "Strain from which the restriction enzyme EcoRI was isolated",
      "Gave a definition of biotechnology covering both traditional and modern molecular biotechnology",
      "Its T-DNA transforms normal plant cells into tumour cells"]),
  "Organisms and bodies in biotechnology",
  "NCERT: in EcoRI, the letters come from the genus Escherichia, species coli and strain RY 13. PCR uses a "
  "thermostable DNA polymerase isolated from the bacterium Thermus aquaticus. Agrobacterium tumefaciens delivers a "
  "piece of DNA known as T-DNA that transforms normal plant cells into tumour cells. The European Federation of "
  "Biotechnology (EFB) has given a definition of biotechnology that encompasses both traditional view and modern "
  "molecular biotechnology.",
  ["A -> II", "B -> I", "C -> IV", "D -> III"],
  "Principles of Biotechnology; Restriction Enzymes; Cloning Vectors; Amplification of Gene of Interest using PCR",
  at="D", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="EcoRI, not the PCR polymerase, comes from E. coli RY 13; the T-DNA belongs to Agrobacterium, which did not "
      "define biotechnology; and Thermus aquaticus is the polymerase source, not a plant pathogen.", secs=45)

Z(BPP, "Cloning vectors", I, MUL,
  MS("Which of the following statements about alien DNA moved into a host organism are correct, according to "
     "NCERT?",
     ["In most cases, alien DNA moved into an organism would not be able to multiply in the progeny cells.",
      "When it gets integrated into the genome of the recipient, it may multiply and be inherited along with the "
      "host DNA.",
      "It can also be replicated if it is linked to an origin of replication (ori).",
      "The ori is also responsible for controlling the copy number of the linked DNA.",
      "Alien DNA always multiplies in the host on its own, without integration or an ori."]),
  "Maintaining alien DNA in a host",
  "NCERT: in a majority of cases, the alien piece of DNA would not be able to multiply itself in the progeny cells "
  "of the organism. But when it gets integrated into the genome of the recipient, it may multiply and be inherited "
  "along with the host DNA, because it has become part of a chromosome, which has the ability to replicate. The "
  "alien DNA is linked with the origin of replication, a sequence from where replication starts; the ori is also "
  "responsible for controlling the copy number of the linked DNA.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - needs integration or an ori"],
  "Principles of Biotechnology; Cloning Vectors",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (c) and (e) only", "(a) and (e) only"],
  why="(e) contradicts NCERT's point that alien DNA usually cannot multiply by itself, so every option with (e) is "
      "wrong; (a)-(d) are all NCERT statements.", secs=45)

Z(BPP, "Competent hosts and transformation", I, D,
  "Which pairing of a vector and the kind of cell into which NCERT says it is used to deliver genes is correct?",
  "Vectors for plants and animals",
  "NCERT: Agrobacterium tumefaciens, a pathogen of several dicot plants, delivers T-DNA into plant cells; its Ti "
  "plasmid has been modified into a cloning vector which is no more pathogenic to the plants but is still able to "
  "deliver genes of our interest into a variety of plants. Similarly, retroviruses have been disarmed and are now "
  "used to deliver desirable genes into animal cells. pBR322 is an E. coli cloning vector.",
  ["Ti plasmid (disarmed) -> plant cells", "Retrovirus (disarmed) -> animal cells", "pBR322 -> E. coli"],
  "Cloning Vectors",
  at="A", correct="Disarmed retroviruses – animal cells; modified Ti plasmid – plant cells",
  wrong=["Disarmed retroviruses – plant cells; modified Ti plasmid – animal cells",
         "Disarmed retroviruses – bacterial cells; pBR322 – plant cells",
         "Modified Ti plasmid – fungal cells; bacteriophage – animal cells"],
  why="The second option swaps the two vectors; pBR322 is an E. coli vector and retroviruses are used for animal "
      "cells, not bacteria; and NCERT uses the Ti plasmid for plants, not fungi, with bacteriophages as vectors for "
      "bacteria.", secs=35)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("Each restriction endonuclease recognises a specific palindromic nucleotide sequence in the DNA.",
     "The more than 900 restriction enzymes known today, isolated from over 230 strains of bacteria, all recognise "
     "the same recognition sequence."),
  "Specificity of restriction enzymes",
  "NCERT: today we know more than 900 restriction enzymes that have been isolated from over 230 strains of bacteria, "
  "each of which recognises DIFFERENT recognition sequences. Every restriction endonuclease recognises a specific "
  "palindromic nucleotide sequence in the DNA. A is true; R is false.",
  ["A: true", "R: false - each recognises a different sequence"],
  "Restriction Enzymes", ans="C",
  why="R contradicts NCERT's statement that the enzymes recognise different sequences, so options treating R as "
      "true are wrong; A is NCERT's statement, so 'A is false' is wrong.", secs=30)

Z(BPP, "Cloning vectors", I, STP,
  SP("In pBR322, the rop gene codes for the proteins involved in the replication of the plasmid.",
     "In pBR322, the recognition site for PvuI lies within the tetracycline resistance gene."),
  "Map of pBR322",
  "NCERT (pBR322 figure): rop codes for the proteins involved in the replication of the plasmid. The PstI and PvuI "
  "sites lie in the ampicillin resistance gene (ampR), while the BamHI and SalI sites lie in the tetracycline "
  "resistance gene (tetR).",
  ["Statement I: true", "Statement II: false - PvuI site is in ampR"],
  "Cloning Vectors", ans="C",
  why="Statement II places the PvuI site in the wrong resistance gene, so options calling it true are wrong; "
      "Statement I is NCERT's description of rop, so options calling it false are wrong.", secs=35)

Z(BPP, "Bioreactors and downstream processing", I, ASR,
  AR("A stirred-tank bioreactor is usually cylindrical or has a curved base.",
     "This shape facilitates the mixing of the reactor contents."),
  "Shape of stirred-tank bioreactors",
  "NCERT: the most commonly used bioreactors are of the stirring type. A stirred-tank reactor is usually cylindrical "
  "or with a curved base to facilitate the mixing of the reactor contents; the stirrer facilitates even mixing and "
  "oxygen availability throughout the bioreactor. NCERT gives mixing as the purpose of the shape, so R explains A.",
  ["A: true", "R: true", "NCERT: shape is 'to facilitate the mixing' -> R explains A"],
  "Bioreactors", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT states the shape is "
      "meant to facilitate mixing, so R is the explanation.", secs=30)

Z(BPP, "Competent hosts and transformation", I, STP,
  SP("Agrobacterium tumefaciens is a pathogen of several monocot plants.",
     "In animals, retroviruses have the ability to transform cancerous cells back into normal cells."),
  "Natural gene-transfer agents",
  "NCERT: Agrobacterium tumefaciens is a pathogen of several DICOT plants; it delivers T-DNA that transforms normal "
  "plant cells into tumours. Retroviruses in animals have the ability to transform NORMAL cells into CANCEROUS "
  "cells. Both statements reverse NCERT's description.",
  ["Statement I: false - dicot plants", "Statement II: false - normal cells into cancerous cells"],
  "Cloning Vectors", ans="B",
  why="Statement I names the wrong plant group and Statement II reverses the direction of transformation, so every "
      "option calling either statement true is wrong.", secs=35)

Z(BPP, "Bioreactors and downstream processing", A, MUL,
  MS("Which of the following statements about the processing of a biotechnological product after biosynthesis are "
     "correct?",
     ["Separation and purification of the product are collectively referred to as downstream processing.",
      "The product has to be formulated with suitable preservatives.",
      "In the case of drugs, the formulation has to undergo thorough clinical trials.",
      "Strict quality control testing for each product is required.",
      "Downstream processing and quality control testing are the same for every product."]),
  "Downstream processing",
  "NCERT: after completion of the biosynthetic stage, the product has to be subjected through a series of processes "
  "before it is ready for marketing. The processes include separation and purification, collectively referred to "
  "as downstream processing. The product has to be formulated with suitable preservatives; such formulation has to "
  "undergo thorough clinical trials as in the case of drugs. Strict quality control testing for each product is "
  "also required. The downstream processing and quality control testing vary from product to product.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - vary from product to product"],
  "Downstream Processing",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (e) only", "(c), (d) and (e) only"],
  why="(e) contradicts NCERT, which says these steps vary from product to product, so every option with (e) is "
      "wrong; (a)-(d) are all NCERT statements.", secs=45)

Z(BPP, "PCR and gel electrophoresis", A, D,
  "During the isolation of DNA, how many of the following are used to BREAK OPEN the cells (rather than for a later "
  "step)?\n\nLysozyme, ribonuclease, cellulase, protease, chitinase, chilled ethanol",
  "Breaking open cells to release DNA",
  "NCERT: to obtain DNA free from other macromolecules, the cells are broken open by treating bacterial cells, "
  "plant cells or fungal cells with enzymes such as lysozyme (bacteria), cellulase (plant cells) and chitinase "
  "(fungus). RNA is then removed by ribonuclease and proteins by protease, and purified DNA precipitates on "
  "addition of chilled ethanol.",
  ["Break open cells: lysozyme, cellulase, chitinase = 3",
   "Later steps: ribonuclease (RNA), protease (proteins), chilled ethanol (precipitation)"],
  "Isolation of the Genetic Material (DNA)",
  at="B", correct="Three",
  wrong=["Two", "Four", "Five"],
  why="Two leaves out one of the three cell-wall-degrading enzymes (often chitinase for fungi); four or five add "
      "ribonuclease, protease or chilled ethanol, which act after the cells have been opened.", secs=40)

Z(BPP, "Cloning vectors", A, ASR,
  AR("Selecting recombinants by the insertional inactivation of β-galactosidase is less cumbersome than selecting "
     "them by the inactivation of an antibiotic resistance gene.",
     "In this method, colonies that carry the recombinant DNA give a blue colour with the chromogenic substrate."),
  "Insertional inactivation of β-galactosidase",
  "NCERT: selection of recombinants due to inactivation of antibiotics is a cumbersome procedure because it requires "
  "simultaneous plating on two plates having different antibiotics; alternative markers differentiate recombinants "
  "on the basis of their ability to produce colour in the presence of a chromogenic substrate. Presence of a "
  "chromogenic substrate gives blue coloured colonies if the plasmid in the bacteria does NOT have an insert; "
  "presence of an insert results in insertional inactivation of β-galactosidase, and the colonies do not produce "
  "any colour. So A is true and R is false.",
  ["A: true - one plate, colour-based", "R: false - recombinants give no colour; non-recombinants are blue"],
  "Cloning Vectors", ans="C",
  why="R reverses which colonies turn blue, so options treating R as true are wrong; A is NCERT's comparison of the "
      "two selection methods, so 'A is false' is wrong.", secs=40)

Z(BPP, "Cloning vectors", A, STP,
  SP("The first recombinant DNA was constructed by linking a gene encoding antibiotic resistance with a native "
     "plasmid of Escherichia coli.",
     "Plasmid DNA acts as a vector to transfer the piece of DNA attached to it into the host organism."),
  "The first recombinant DNA",
  "NCERT: the construction of the first recombinant DNA emerged from the possibility of linking a gene encoding "
  "antibiotic resistance with a native plasmid (autonomously replicating circular extra-chromosomal DNA) of "
  "Salmonella typhimurium. Stanley Cohen and Herbert Boyer accomplished this in 1972. Plasmid DNA acts as a vector "
  "to transfer the piece of DNA attached to it into the host organism.",
  ["Statement I: false - native plasmid of Salmonella typhimurium", "Statement II: true"],
  "Principles of Biotechnology", ans="D",
  why="Statement I replaces Salmonella typhimurium with E. coli, so options calling it true are wrong; Statement II "
      "is NCERT's description of plasmid vectors, so options calling it false are wrong.", secs=40)

Z(BPP, "Competent hosts and transformation", A, MAT,
  ML(("term", "meaning, as used in NCERT"),
     ["Recombinant protein", "Competent host", "Elution", "Spooling"],
     ["Removing the fine threads of precipitated DNA from the suspension",
      "Extraction of DNA from the piece of gel cut out with its band",
      "Protein made when a protein-encoding gene is expressed in a heterologous host",
      "A bacterial cell made capable of taking up DNA, for example by treatment with a divalent cation"]),
  "Terms of recombinant DNA work",
  "NCERT: if any protein-encoding gene is expressed in a heterologous host, it is called a recombinant protein. "
  "Bacterial cells are made 'competent' to take up DNA by treating them with a specific concentration of a "
  "divalent cation, such as calcium. Separated DNA bands are cut out from the agarose gel and extracted from the "
  "gel piece; this step is known as elution. Purified DNA precipitating after chilled ethanol can be removed by "
  "spooling.",
  ["A -> III", "B -> IV", "C -> II", "D -> I"],
  "Isolation of the Genetic Material (DNA); Separation and Isolation of DNA Fragments; Insertion of Recombinant DNA "
  "into the Host Cell/Organism; Obtaining the Foreign Gene Product",
  at="A", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="A competent host is a cell able to take up DNA, not the protein it makes; elution extracts DNA from the gel, "
      "whereas spooling removes DNA threads from the ethanol suspension, so swapping C and D is wrong; elution is "
      "not a way of making cells competent.", secs=45)

# ================================================================ Biotechnology and its Applications (4/6/4)
Z(BTA, "Bt crops and RNAi", B, D,
  "Although the Green Revolution succeeded in tripling the food supply, NCERT says the increased yields were only "
  "partly due to improved crop varieties. What were they MAINLY due to?",
  "Green Revolution and its limits",
  "NCERT: although the Green Revolution succeeded in tripling the food supply, it was not enough to feed the growing "
  "human population. Increased yields have partly been due to the use of improved crop varieties, but mainly due to "
  "the use of better management practices and use of agrochemicals (fertilisers and pesticides).",
  ["Partly: improved crop varieties", "Mainly: better management practices + agrochemicals"],
  "Biotechnological Applications in Agriculture",
  at="D", correct="Better management practices and the use of agrochemicals (fertilisers and pesticides)",
  wrong=["Genetically modified crops such as Bt cotton", "Organic agriculture alone",
         "RNA interference against crop pests"],
  why="Bt crops and RNAi are genetically engineered approaches that NCERT presents as a further option after the "
      "Green Revolution; organic agriculture is a separate option, not the main reason for those yields.", secs=25)

Z(BTA, "Gene therapy", B, D,
  "Adenosine deaminase (ADA) deficiency was the disorder treated in the first clinical gene therapy. According to "
  "NCERT, what causes this disorder?",
  "Cause of ADA deficiency",
  "NCERT: the first clinical gene therapy was given in 1990 to a 4-year-old girl with adenosine deaminase (ADA) "
  "deficiency. This enzyme is crucial for the immune system to function. The disorder is caused due to the "
  "deletion of the gene for adenosine deaminase.",
  ["ADA crucial for the immune system", "Disorder caused by deletion of the ADA gene"],
  "Gene Therapy",
  at="A", correct="Deletion of the gene for adenosine deaminase",
  wrong=["Infection of lymphocytes by a retrovirus", "Excess production of adenosine deaminase",
         "Insertion of a Bt toxin gene into lymphocytes"],
  why="A retrovirus is the disarmed vector used in the therapy, not the cause; the disorder is a lack, not an "
      "excess, of the enzyme; and Bt toxin genes are used in crops, not linked to ADA deficiency.", secs=20)

Z(BTA, "Bt crops and RNAi", B, STP,
  SP("For farmers in the developing world, agrochemicals are often too expensive.",
     "Further increases in yield with existing varieties are not possible using conventional breeding."),
  "Why genetically engineered crops",
  "NCERT: for farmers in the developing world, agrochemicals are often too expensive, and further increases in "
  "yield with existing varieties are not possible using conventional breeding. NCERT then asks whether any "
  "alternative path exists that genetics could use to increase yields, and turns to genetically modified crops.",
  ["Statement I: true", "Statement II: true"],
  "Biotechnological Applications in Agriculture", ans="A",
  why="Both statements are NCERT's own reasons for looking beyond the Green Revolution, so every option calling "
      "either false is wrong.", secs=25)

Z(BTA, "Transgenic animals", B, ASR,
  AR("Transgenic animals have been used to produce human α-1-antitrypsin, a protein used to treat emphysema.",
     "Over 95 per cent of all existing transgenic animals are mice."),
  "Transgenic animals",
  "NCERT: although transgenic rats, rabbits, pigs, sheep, cows and fish have been produced, over 95 per cent of all "
  "existing transgenic animals are mice. Separately, under biological products, NCERT notes that transgenic "
  "animals have been used to produce human protein (α-1-antitrypsin) used to treat emphysema. Both are true, but "
  "how common transgenic mice are does not explain why transgenic animals can make this protein.",
  ["A: true", "R: true", "R is a count of transgenic species, unrelated to A"],
  "Transgenic Animals", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; the share of mice among "
      "transgenic animals says nothing about producing α-1-antitrypsin, so R is not the explanation.", secs=30)

Z(BTA, "Bt crops and RNAi", I, MAT,
  ML(("way in which genetic modification has been useful", "NCERT detail"),
     ["Tolerance to abiotic stresses", "Pest-resistant crops", "Increased efficiency of mineral usage",
      "Enhanced nutritional value of food"],
     ["Vitamin 'A' enriched rice", "Prevents early exhaustion of the fertility of the soil",
      "Cold, drought, salt and heat", "Reduced reliance on chemical pesticides"]),
  "Uses of genetically modified plants",
  "NCERT: genetic modification has (i) made crops more tolerant to abiotic stresses (cold, drought, salt, heat); "
  "(ii) reduced reliance on chemical pesticides (pest-resistant crops); (iii) helped to reduce post-harvest losses; "
  "(iv) increased efficiency of mineral usage by plants, which prevents early exhaustion of the fertility of the "
  "soil; and (v) enhanced the nutritional value of food, e.g. vitamin 'A' enriched rice.",
  ["A -> III", "B -> IV", "C -> II", "D -> I"],
  "Biotechnological Applications in Agriculture",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "I", "B": "IV", "C": "II", "D": "III"}]),
  why="Cold, drought, salt and heat are abiotic stresses, not pests; soil fertility is linked to mineral usage, "
      "not to pest resistance; and vitamin A rice is an example of better nutrition, not of stress tolerance.",
  secs=45)

Z(BTA, "Biosafety, biopiracy and patents", I, MUL,
  MS("Which of the following statements are correct according to NCERT's discussion of bio-resources and patents?",
     ["Traditional knowledge related to bio-resources can be exploited to develop modern applications.",
      "Attempts have been made to patent uses, products and processes based on Indian traditional herbal "
      "medicines, e.g. turmeric and neem.",
      "Basmati rice is distinct for its unique aroma and flavour.",
      "Industrialised nations are rich in biodiversity and traditional knowledge, but financially poor.",
      "The developing and under-developed world is rich in biodiversity and traditional knowledge related to "
      "bio-resources."]),
  "Bio-resources and patents",
  "NCERT: traditional knowledge related to bio-resources can be exploited to develop modern applications (and can "
  "save time, effort and expenditure during their commercialisation). Basmati rice is distinct for its unique aroma "
  "and flavour. Attempts have been made to patent uses, products and processes based on Indian traditional herbal medicines, e.g. turmeric and neem. The "
  "industrialised nations are rich financially but poor in biodiversity and traditional knowledge, whereas the "
  "developing and under-developed world is rich in biodiversity and traditional knowledge related to "
  "bio-resources.",
  ["(a) true", "(b) true", "(c) true", "(d) false - reversed", "(e) true"],
  "Ethical Issues",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="(d) reverses NCERT's contrast between industrialised and developing nations, so every option with (d) is "
      "wrong; the correct option keeps the other four NCERT statements.", secs=45)

Z(BTA, "Bt crops and RNAi", I, D,
  "According to NCERT, which are the three options that can be thought of for increasing food production?",
  "Options for increasing food production",
  "NCERT: let us take a look at the three options that can be thought of for increasing food production: (i) "
  "agro-chemical based agriculture; (ii) organic agriculture; and (iii) genetically engineered crop-based "
  "agriculture.",
  ["Agro-chemical based agriculture", "Organic agriculture", "Genetically engineered crop-based agriculture"],
  "Biotechnological Applications in Agriculture",
  at="A", correct="Agro-chemical based agriculture, organic agriculture and genetically engineered crop-based "
                  "agriculture",
  wrong=["Agro-chemical based agriculture, shifting cultivation and gene therapy",
         "Organic agriculture, biopiracy and transgenic animals",
         "Genetically engineered crops, MTP and organic agriculture"],
  why="Shifting cultivation is not one of NCERT's three options, gene therapy and MTP are medical procedures, and "
      "biopiracy and transgenic animals are not ways of growing more food.", secs=25)

Z(BTA, "Transgenic animals", I, ASR,
  AR("Rosie produced milk containing human α-lactalbumin, which was nutritionally a more balanced product for "
     "human babies than natural cow milk.",
     "Rosie was the first transgenic sheep, produced in 1997."),
  "Rosie",
  "NCERT: in 1997, the first transgenic COW, Rosie, produced human protein-enriched milk (2.4 grams per litre). The "
  "milk contained the human alpha-lactalbumin and was nutritionally a more balanced product for human babies than "
  "natural cow milk. A is true; R is false because Rosie was a cow.",
  ["A: true", "R: false - Rosie was a cow"],
  "Transgenic Animals", ans="C",
  why="R calls Rosie a sheep, so options treating R as true are wrong; A is NCERT's description of Rosie's milk, so "
      "'A is false' is wrong.", secs=30)

Z(BTA, "Biosafety, biopiracy and patents", I, STP,
  SP("According to NCERT, genetic modification gives fully predictable results, so genetically modified "
     "organisms can be introduced into any ecosystem without regulation.",
     "Biopiracy covers the use of bio-resources not only by multinational companies but also by other "
     "organisations, when it is done without proper authorisation and without compensatory payment."),
  "Regulation of GM organisms and the scope of biopiracy",
  "NCERT: the manipulation of living organisms cannot go on without regulation, and genetic modification of "
  "organisms can have UNPREDICTABLE results when such organisms are introduced into the ecosystem, so Statement I is "
  "false. Biopiracy is the use of bio-resources by multinational companies and other organisations without proper "
  "authorisation from the countries and people concerned and without compensatory payment, so Statement II is true.",
  ["Statement I: false - results can be unpredictable, and regulation is needed",
   "Statement II: true - 'multinational companies and other organisations'"],
  "Ethical Issues", ans="D",
  why="Statement I reverses NCERT's warning about unpredictable results, so options calling it true are wrong; "
      "Statement II is NCERT's definition of biopiracy, so options calling it false are wrong.", secs=30)

Z(BTA, "Biosafety, biopiracy and patents", I, D,
  "According to NCERT, the use of genetically modified organisms for public services (as food and medicine "
  "sources) has also created problems. When did these problems arise?",
  "GM organisms and patents",
  "NCERT: genetic modification of organisms can have unpredictable results when such organisms are introduced into "
  "the ecosystem. Moreover, the use of such organisms for public services (as food and medicine sources) has also "
  "created problems when patents are granted for the same.",
  ["Public-service use of GM organisms", "-> problems when patents are granted for the same"],
  "Ethical Issues",
  at="B", correct="When patents were granted for the same",
  wrong=["When the organisms were grown in bioreactors", "When their genes were amplified by PCR",
         "When their DNA was separated by gel electrophoresis"],
  why="Bioreactors, PCR and gel electrophoresis are laboratory and production tools; NCERT links the problems of "
      "public-service use of GM organisms to the granting of patents.", secs=25)

Z(BTA, "Human insulin", A, MUL,
  MS("Which of the following combinations of the DNA used, the host or recipient, and the purpose are correctly "
     "given, according to NCERT's examples?",
     ["cry genes of Bacillus thuringiensis - cotton plant - protection against bollworms",
      "Nematode-specific genes producing sense and anti-sense RNA - tobacco plant - protection against "
      "Meloidegyne incognitia",
      "Functional ADA cDNA - the patient's lymphocytes - treatment of ADA deficiency",
      "DNA sequences for chains A and B of insulin - plasmids of E. coli - production of human insulin",
      "Genes for human α-lactalbumin - E. coli - production of vitamin A enriched rice"]),
  "Applications compared",
  "NCERT: cry genes from Bacillus thuringiensis expressed in cotton control the cotton bollworms; nematode-specific "
  "genes introduced into tobacco (with Agrobacterium vectors) produce sense and anti-sense RNA that silence a "
  "nematode mRNA; functional ADA cDNA is introduced into the patient's lymphocytes (using a retroviral vector); "
  "and Eli Lilly introduced DNA sequences for chains A and B into plasmids of E. coli to produce insulin chains. "
  "Human α-lactalbumin was in the milk of the transgenic cow Rosie, and vitamin A enriched rice is golden rice.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - mixes Rosie's protein with golden rice"],
  "Biotechnological Applications in Agriculture; Genetically Engineered Insulin; Gene Therapy",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (e) only", "(b), (d) and (e) only"],
  why="(e) joins the human protein of Rosie's milk to E. coli and to golden rice, none of which matches NCERT, so "
      "every option containing (e) is wrong; (a)-(d) are all correct.", secs=60)

Z(BTA, "Gene therapy", A, MAT,
  ML(("approach", "what actually protects the plant or treats the patient"),
     ["Bt cotton", "RNAi-based tobacco resistant to Meloidegyne incognitia",
      "Gene therapy for ADA deficiency using lymphocytes", "Enzyme replacement therapy for ADA deficiency"],
     ["Functional ADA cDNA delivered into lymphocytes by a retroviral vector",
      "A protein toxin, inactive as a protoxin until activated in the insect gut",
      "Functional ADA enzyme given to the patient by injection",
      "dsRNA formed from complementary sense and anti-sense RNA, silencing a specific mRNA of the parasite"]),
  "What each application delivers",
  "NCERT: Bt cotton makes the Bt toxin protein, which exists as an inactive protoxin and becomes active in the "
  "alkaline gut of the insect. In the RNAi tobacco, the introduced DNA produced both sense and anti-sense RNA; these "
  "complementary RNAs formed dsRNA that silenced a specific mRNA of the nematode. In gene therapy for ADA "
  "deficiency, a functional ADA cDNA is introduced into the patient's cultured lymphocytes using a retroviral "
  "vector. In enzyme replacement therapy, functional ADA is given to the patient by injection.",
  ["A -> II", "B -> IV", "C -> I", "D -> III"],
  "Biotechnological Applications in Agriculture; Gene Therapy",
  at="C", match=({"A": "II", "B": "IV", "C": "I", "D": "III"},
                 [{"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="Bt cotton works through a protein and the RNAi tobacco through dsRNA, so swapping them is wrong; gene therapy "
      "delivers the ADA gene (cDNA), whereas enzyme replacement injects the enzyme itself, so swapping C and D is "
      "wrong; lymphocyte gene therapy does not involve dsRNA.", secs=50)

Z(BTA, "Bt crops and RNAi", A, ASR,
  AR("Bacillus thuringiensis is killed by its own Bt toxin when the toxin is present in large amounts in the "
     "bacterium.",
     "In the bacterium, the Bt toxin protein exists as an inactive protoxin."),
  "Why the Bt toxin spares the bacterium",
  "NCERT: the Bt toxin protein exists as an inactive protoxin in the bacterium; once an insect ingests it, it is "
  "converted into an active form of toxin due to the alkaline pH of the gut, which solubilises the crystals. "
  "Because it is inactive in the bacterium, the toxin does not kill Bacillus thuringiensis, so A is false while R "
  "is true.",
  ["A: false - the protoxin is inactive in the bacterium", "R: true"],
  "Biotechnological Applications in Agriculture", ans="D",
  why="A contradicts the very fact stated in R, so options calling A true are wrong; R is NCERT's own statement, so "
      "'A is false but R is true' is the answer.", secs=35)

Z(BTA, "Bt crops and RNAi", A, D,
  "How many of the following crops does NCERT name as plants in which the Bt toxin gene has been expressed to "
  "provide resistance to insects?\n\nCotton, corn, rice, tomato, potato, soyabean, wheat, mustard",
  "Bt crops named in NCERT",
  "NCERT: the Bt toxin gene has been cloned from the bacteria and expressed in plants to provide resistance to "
  "insects without the need for insecticides, in effect creating a bio-pesticide; examples are Bt cotton, Bt corn, "
  "rice, tomato, potato and soyabean. Wheat and mustard are not named.",
  ["Named: cotton, corn, rice, tomato, potato, soyabean = 6", "Not named: wheat, mustard"],
  "Biotechnological Applications in Agriculture",
  at="B", correct="Six",
  wrong=["Five", "Seven", "Eight"],
  why="Five omits one of NCERT's six examples (often soyabean or rice); seven or eight add wheat and/or mustard, "
      "which NCERT does not name.", secs=40)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 131
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "ZOO_009_p2: 131 original Zoology questions (Neural Control and Coordination, Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers and computed match/count keys re-derived in tools/batch_009/ZOO_009_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
