"""Builder for BATCH_009, package BOT_009_p2 (Botany, NEET_BOT_002124..NEET_BOT_002250, 127 questions).

Topics: Respiration in Plants; Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles
of Inheritance and Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and
Populations; Ecosystem; Biodiversity and Conservation. All questions are original and every fact is taken from
the rationalised NCERT Class 11/12 Biology textbooks. Facts already tested in BATCH_000 to BATCH_008 on these
topics were avoided or approached from a new angle (see `python tools/merge_batch.py stems 009 BOT_009_p2`).
Computable answers are re-derived below; the file is written only if every assert, the plan quota, the format
mix and the answer-key balance pass.

    cd docs/neet-bank && python tools/batch_009/BOT_009_p2.py
"""



import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
BOT = "Botany"
PACKAGE = "BOT_009_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_009_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_009_BOT_p2.json"
FIRST_ID = 2124

AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

RIP = "Respiration in Plants"
PGD = "Plant Growth and Development"
SRFP = "Sexual Reproduction in Flowering Plants"
PIV = "Principles of Inheritance and Variation"
MBI = "Molecular Basis of Inheritance"
MHW = "Microbes in Human Welfare"
OAP = "Organisms and Populations"
ECO = "Ecosystem"
BDC = "Biodiversity and Conservation"

QUESTIONS = []


def ref(cls, chapter, section):
    return f"Class {cls} Biology, '{chapter}', {section}"


def P(correct, wrong, at):
    """Options with the correct text at position `at`."""
    opts = list(wrong)
    assert len(opts) == 3
    opts.insert(LETTERS.index(at), correct)
    assert len(set(opts)) == 4, opts
    return opts, at


def AR(at):
    return list(ASSERTION_REASON), at


def SP(at):
    return list(STATEMENT_PAIR), at


def M(correct, wrong, at):
    """Match-the-list codes with the correct code at position `at` (as match_options() in the sample builder)."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    assert sorted(correct.values()) == sorted(["I", "II", "III", "IV"])
    for w in wrong:
        assert sorted(w.values()) == sorted(["I", "II", "III", "IV"]), w
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4, opts
    return opts, at


def mc(s):
    """'III,IV,I,II' -> {'A': 'III', 'B': 'IV', 'C': 'I', 'D': 'II'}"""
    return dict(zip("ABCD", s.split(",")))


def MS(correct, wrong, at):
    """Multi-statement options: each option is a set of statement letters; the correct set goes at `at`."""
    fmt = lambda s: (", ".join(f"({x})" for x in s[:-1]) + f" and ({s[-1]})" if len(s) > 1 else f"({s[0]})") + " only"
    sets = [correct] + list(wrong)
    assert len({tuple(s) for s in sets}) == 4
    return P(fmt(correct), [fmt(w) for w in wrong], at)


def ar(a, r):
    return ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {a}\nReason (R): {r}\n\n"
            "Choose the correct answer from the options given below:")


def sp(s1, s2):
    return (f"Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")


def ml(head, l1, l2):
    a = "\n".join(f"{k}. {t}" for k, t in zip("ABCD", l1))
    b = "\n".join(f"{k}. {t}" for k, t in zip(["I", "II", "III", "IV"], l2))
    return (f"Match List-I ({head[0]}) with List-II ({head[1]}).\n\nList-I:\n{a}\n\nList-II:\n{b}\n\n"
            "Choose the correct answer from the options given below:")


def ms(intro, statements):
    body = "\n".join(f"({k}) {t}" for k, t in zip("abcde", statements))
    return f"{intro}\n\n{body}\n\nChoose the correct answer from the options given below:"


def add(topic, subtopic, difficulty, fmt, text, oa, concept, explanation, steps, ncert,
        shortcut=None, why=None, seconds=45, verified_by=AUTHORED):
    options, answer = oa
    assert answer in LETTERS and len(options) == 4 and ncert
    if fmt in ("direct", "numerical", "match_list", "multi_statement"):
        assert why, (topic, text[:60])
    QUESTIONS.append({
        "question_id": None, "exam_mappings": default_mappings(BOT), "subject": BOT, "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(verified_by), "verified_at": TODAY},
    })

# ================================================================ Respiration in Plants (3 / 5 / 3)
C11_RP = lambda s: ref(11, RIP, s)

add(RIP, "Respiratory quotient", "Basic", "direct",
    "NCERT notes that carbohydrates are usually oxidised in respiration, but proteins, fats and even organic acids "
    "can also be used. The compounds that are oxidised during respiration are known as:",
    P("Respiratory substrates", ["Electron carriers", "Coenzymes", "Reducing equivalents"], "B"),
    "Respiratory substrates",
    "NCERT: during oxidation within a cell, all the energy contained in respiratory substrates is not released "
    "free all at once; the compounds that are oxidised during this process are known as respiratory substrates. "
    "Usually carbohydrates are oxidised, though proteins, fats and organic acids can be used in some plants under "
    "certain conditions. The type of substrate in turn decides the respiratory quotient.",
    ["Compounds oxidised in respiration = respiratory substrates", "Usually carbohydrates; also fats, proteins, "
     "organic acids"],
    C11_RP("introduction: respiratory substrates"),
    why="Electron carriers (ubiquinone, cytochrome c) and coenzymes (NAD⁺, FAD⁺, CoA) take part in the oxidation "
        "but are not the compounds being oxidised for energy; reducing equivalents are the hydrogen/electrons "
        "removed from the substrates.",
    seconds=20)

add(RIP, "Glycolysis and fermentation", "Basic", "statement_pair",
    sp("In glycolysis, when PGAL is oxidised (with inorganic phosphate) to 1,3-bisphosphoglyceric acid, two "
       "redox-equivalents are removed as two hydrogen atoms and transferred to NAD⁺.",
       "In glycolysis, NADH + H⁺ is also formed when phosphoenolpyruvate (PEP) is converted to pyruvic acid."),
    SP("C"),
    "Where NADH is formed in glycolysis",
    "NCERT: 3-phosphoglyceraldehyde (PGAL) is oxidised and with inorganic phosphate converted into BPGA; during "
    "this step two redox-equivalents are removed (as two hydrogen atoms) from PGAL and transferred to a molecule "
    "of NAD⁺, forming NADH + H⁺ (Statement I true). The conversion of PEP to pyruvic acid is a step at which ATP "
    "is synthesised; no NAD⁺ is reduced there (Statement II false).",
    ["PGAL → BPGA: NAD⁺ reduced", "PEP → pyruvic acid: ATP formed, not NADH"],
    C11_RP("glycolysis"),
    seconds=30)

add(RIP, "Electron transport system", "Basic", "direct",
    "In mitochondria, the metabolic pathway through which electrons pass from one carrier to another, finally "
    "reaching oxygen, is called the:",
    P("Electron transport system", ["Tricarboxylic acid cycle", "EMP pathway", "Amphibolic pathway"], "D"),
    "Definition of the ETS",
    "NCERT: the metabolic pathway through which the electron passes from one carrier to another is called the "
    "electron transport system (ETS), and it is present in the inner mitochondrial membrane. Electrons from NADH "
    "and FADH₂ pass through it to O₂, forming water.",
    ["Electron passed carrier to carrier", "= ETS, in the inner mitochondrial membrane"],
    C11_RP("electron transport system (ETS) and oxidative phosphorylation"),
    why="The TCA cycle and the EMP pathway (glycolysis) are substrate-oxidising pathways, not chains of electron "
        "carriers; 'amphibolic' describes the respiratory pathway's role in both breakdown and synthesis.",
    seconds=20)

add(RIP, "TCA cycle", "Intermediate", "direct",
    "Linking NCERT's account of the TCA cycle with that of the electron transport system: the single step of the "
    "cycle at which FAD⁺ is reduced to FADH₂ is the:",
    P("Oxidation of succinate (succinic acid)",
      ["Conversion of succinyl CoA to succinic acid", "Conversion of α-ketoglutaric acid to succinyl CoA",
       "Condensation of acetyl CoA with oxaloacetic acid"], "D"),
    "FADH₂ comes from succinate oxidation",
    "NCERT's TCA cycle has three points where NAD⁺ is reduced and one point where FAD⁺ is reduced. The ETS "
    "section identifies that point: FADH₂ is generated during the oxidation of succinate in the citric acid "
    "cycle, and its electrons are passed to ubiquinone through complex II.",
    ["One FAD⁺ reduction per turn", "ETS section: FADH₂ from oxidation of succinate"],
    C11_RP("tricarboxylic acid cycle; electron transport system (ETS)"),
    why="Succinyl CoA → succinic acid is the step that forms GTP; α-ketoglutaric acid → succinyl CoA is a "
        "decarboxylation; the condensation step forms citric acid and involves no FAD⁺.",
    seconds=35)

add(RIP, "Electron transport system", "Intermediate", "direct",
    "NCERT states that for each ATP produced, 2H⁺ pass through F₀ from the intermembrane space to the matrix "
    "down the electrochemical proton gradient. It follows that, while ATP is being made, the concentration of "
    "protons is:",
    P("Higher in the intermembrane space than in the matrix",
      ["Higher in the matrix than in the intermembrane space", "Equal on the two sides of the inner membrane",
       "Higher in the cytoplasm than in the intermembrane space"], "C"),
    "Direction of the proton gradient",
    "Movement 'down' a gradient is from the side of higher concentration to the side of lower concentration. "
    "Since protons flow through F₀ from the intermembrane space into the matrix, the intermembrane space has the "
    "higher proton concentration. The energy of this flow is used by the F₁ headpiece to make ATP.",
    ["Flow: intermembrane space → matrix", "Down a gradient = high → low", "So [H⁺] is higher in the "
     "intermembrane space"],
    C11_RP("electron transport system (ETS) and oxidative phosphorylation"),
    why="A higher matrix concentration would make protons flow the other way; with equal concentrations there "
        "would be no gradient to drive ATP synthase; the cytoplasm is not one of the two compartments NCERT "
        "describes for this flow.",
    seconds=35)

add(RIP, "Glycolysis and fermentation", "Intermediate", "assertion_reason",
    ar("Glycolysis can produce ATP even in the absence of oxygen.",
       "In glycolysis, ATP is synthesised only by oxidative phosphorylation, using the energy of the electron "
       "transport system."),
    AR("C"),
    "ATP formation in glycolysis",
    "NCERT: glycolysis is the only process of respiration in anaerobic organisms, and in fermentation there is a "
    "net gain of two ATP per glucose, so glycolysis makes ATP without oxygen (A true). This ATP is formed directly "
    "in the cytoplasm at two steps (BPGA → PGA and PEP → pyruvic acid), not by oxidative phosphorylation, which "
    "takes place in the inner mitochondrial membrane and needs oxygen as the final acceptor (R false).",
    ["A: true (anaerobes, fermentation net 2 ATP)", "R: glycolytic ATP is made directly, not by the ETS → false"],
    C11_RP("glycolysis; fermentation"),
    seconds=40)

add(RIP, "Electron transport system", "Intermediate", "match_list",
    ml(("molecule", "location described by NCERT"),
       ["Ubiquinone", "Cytochrome c", "Pyruvic dehydrogenase", "Enzymes of the EMP pathway"],
       ["Cytoplasm", "Mitochondrial matrix", "Within the inner mitochondrial membrane",
        "Attached to the outer surface of the inner mitochondrial membrane"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "B"),
    "Where the components of respiration are found",
    "NCERT: ubiquinone is located within the inner mitochondrial membrane (A-III); cytochrome c is a small protein "
    "attached to the outer surface of the inner membrane and acts as a mobile carrier between complexes III and IV "
    "(B-IV); pyruvic dehydrogenase converts pyruvic acid to acetyl CoA in the mitochondrial matrix (C-II); "
    "glycolysis (the EMP pathway) occurs in the cytoplasm of all living organisms (D-I).",
    ["Ubiquinone: in the membrane", "Cytochrome c: outer surface of inner membrane", "PDH: matrix",
     "Glycolysis: cytoplasm"],
    C11_RP("glycolysis; aerobic respiration; electron transport system"),
    why="The other codes swap ubiquinone and cytochrome c, or put pyruvic dehydrogenase in the cytoplasm and "
        "glycolysis in the matrix.",
    seconds=45)

add(RIP, "Respiratory quotient", "Intermediate", "multi_statement",
    ms("Using NCERT's values of the respiratory quotient, which of the following substrates, if completely "
       "oxidised as the respiratory substrate, would give an RQ LESS than 1?",
       ["Tripalmitin, a fat", "Glucose", "Proteins", "Sucrose"]),
    MS(["a", "c"], [["a", "b"], ["b", "d"], ["a", "c", "d"]], "D"),
    "RQ of different substrates",
    "NCERT: when carbohydrates are completely oxidised, the RQ is 1 (glucose and sucrose, b and d). When fats are "
    "used, the RQ is less than 1; tripalmitin gives 102 CO₂/145 O₂ ≈ 0.7 (a). When proteins are the substrate, "
    "the RQ is about 0.9 (c). So only fats and proteins give an RQ below 1.",
    ["Carbohydrates: RQ = 1", "Fat (tripalmitin): ≈ 0.7", "Protein: ≈ 0.9"],
    C11_RP("respiratory quotient"),
    why="Glucose and sucrose are carbohydrates, whose RQ is exactly 1, so any option containing (b) or (d) is wrong.",
    seconds=40)

_NADH, _FADH, _ATP_GLY, _GTP = 10, 2, 2, 2
_ets = _NADH * 3 + _FADH * 2
assert _ets == 34 and _ets + _ATP_GLY + _GTP == 38 and _FADH * 2 == 4

add(RIP, "ATP yield and amphibolic pathway", "Advanced", "statement_pair",
    sp("Under the assumptions of the respiratory balance sheet (10 NADH + H⁺ and 2 FADH₂ per glucose, 3 ATP per "
       "NADH and 2 ATP per FADH₂), 34 of the net 38 ATP from one glucose are made through the electron transport "
       "system and ATP synthase.",
       "Under the same assumptions, the FADH₂ formed from one glucose contributes 6 ATP."),
    SP("C"),
    "Splitting the 38 ATP by source",
    "ETS-linked ATP = 10 × 3 (NADH) + 2 × 2 (FADH₂) = 30 + 4 = 34. The remaining 4 come directly: net 2 from "
    "glycolysis and 2 GTP (as ATP) from the TCA cycle, giving 38 (Statement I true). One glucose gives two "
    "FADH₂ (one per turn of the TCA cycle), each worth 2 ATP, so FADH₂ contributes 4 ATP, not 6 (Statement II "
    "false: 6 comes from counting 3 ATP per FADH₂).",
    ["NADH: 10 × 3 = 30", "FADH₂: 2 × 2 = 4", "ETS total 34; + 2 + 2 direct = 38"],
    C11_RP("the respiratory balance sheet"),
    seconds=60, verified_by=RECOMPUTED)

_link_co2, _tca_nadh, _tca_co2 = 2 * 1, 2 * 3, 2 * 2
_total_nadh = 2 + 2 + _tca_nadh
assert (_link_co2, _tca_co2, _tca_nadh, _total_nadh) == (2, 4, 6, 10)

add(RIP, "TCA cycle", "Advanced", "match_list",
    ml(("quantity formed from ONE molecule of glucose in aerobic respiration", "number"),
       ["CO₂ released in the conversion of pyruvic acid to acetyl CoA",
        "CO₂ released in the TCA cycle itself",
        "NADH + H⁺ formed in the TCA cycle itself",
        "NADH + H⁺ formed in all, from glycolysis to the end of the TCA cycle"],
       ["2", "4", "6", "10"]),
    M(mc("I,II,III,IV"), [mc("I,III,II,IV"), mc("II,I,III,IV"), mc("I,II,IV,III")], "D"),
    "Counting products per glucose",
    "One glucose gives two pyruvic acids. Link reaction: 1 CO₂ and 1 NADH per pyruvate → 2 CO₂ (A-I). Each turn "
    "of the TCA cycle has two decarboxylations and three NAD⁺ reductions; two turns per glucose give 4 CO₂ (B-II) "
    "and 6 NADH (C-III). Total NADH = 2 (glycolysis) + 2 (link) + 6 (TCA) = 10 (D-IV).",
    ["Two pyruvates, two acetyl CoA", "Link: 2 CO₂, 2 NADH", "TCA: 4 CO₂, 6 NADH", "Glycolysis: 2 NADH; total 10"],
    C11_RP("aerobic respiration; tricarboxylic acid cycle"),
    why="The wrong codes count the TCA cycle for one turn only or confuse the TCA NADH (6) with the total (10).",
    seconds=70, verified_by=RECOMPUTED)

add(RIP, "ATP yield and amphibolic pathway", "Advanced", "direct",
    "A step of aerobic respiration has these features: it takes place in the mitochondrial matrix, it releases "
    "CO₂, and it reduces NAD⁺ to NADH + H⁺, but it is NOT a step of the TCA cycle. The step is the:",
    P("Conversion of pyruvic acid to acetyl CoA",
      ["Conversion of α-ketoglutaric acid to succinyl CoA", "Conversion of pyruvic acid to CO₂ and ethanol",
       "Conversion of PGAL to 1,3-bisphosphoglyceric acid"], "D"),
    "Identifying the link reaction",
    "NCERT: pyruvic acid, after entering the mitochondrial matrix, undergoes oxidative decarboxylation by "
    "pyruvic dehydrogenase, which needs NAD⁺ and coenzyme A; CO₂ is released and NADH is formed. This link step "
    "makes acetyl CoA, which then enters the TCA cycle, so it is not itself part of the cycle.",
    ["Matrix + CO₂ + NADH", "Not in the TCA cycle → link reaction (pyruvic acid → acetyl CoA)"],
    C11_RP("aerobic respiration"),
    why="α-Ketoglutaric acid → succinyl CoA fits the first three features but is a TCA-cycle step; pyruvic acid → "
        "ethanol takes place in the cytoplasm and oxidises NADH; PGAL → BPGA reduces NAD⁺ but is a glycolytic "
        "step in the cytoplasm and releases no CO₂.",
    seconds=50)

# ================================================================ Plant Growth and Development (3 / 4 / 3)
C11_PG = lambda s: ref(11, PGD, s)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "NCERT classifies plant growth regulators by chemical nature. Which pair belongs to the SAME chemical group?",
    P("Indole-3-acetic acid (IAA) and indole butyric acid (IBA)",
      ["Indole-3-acetic acid (IAA) and gibberellic acid (GA₃)", "Kinetin and abscisic acid (ABA)",
       "Ethylene and gibberellic acid (GA₃)"], "C"),
    "Chemical groups of PGRs",
    "NCERT: PGRs are of diverse chemical composition: indole compounds (indole-3-acetic acid, IAA; indole butyric "
    "acid, IBA), adenine derivatives (N6-furfurylamino purine, kinetin), derivatives of carotenoids (abscisic "
    "acid, ABA), terpenes (gibberellic acid, GA₃) and gases (ethylene). Only IAA and IBA share a group.",
    ["Indoles: IAA, IBA", "Adenine derivative: kinetin", "Carotenoid derivative: ABA", "Terpene: GA₃; gas: "
     "ethylene"],
    C11_PG("plant growth regulators: characteristics"),
    why="GA₃ is a terpene, not an indole; kinetin is an adenine derivative while ABA is a carotenoid derivative; "
        "ethylene is a gas.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "Cousins confirmed the release of a volatile substance from ripened oranges that hastened the ripening of "
    "stored unripe bananas. This volatile substance was later identified as:",
    P("Ethylene", ["Abscisic acid", "Gibberellic acid", "Zeatin"], "B"),
    "Discovery of ethylene",
    "NCERT: Cousins confirmed the release of a volatile substance from ripened oranges that hastened the "
    "ripening of stored unripe bananas; later this volatile substance was identified as ethylene, a gaseous PGR.",
    ["Volatile from ripe oranges", "Hastened banana ripening", "= ethylene"],
    C11_PG("plant growth regulators: the discovery of plant growth regulators"),
    why="Only ethylene is a gas; ABA came from studies of inhibitors (dormin, abscission II), gibberellic acid "
        "from the bakanae fungus, and zeatin from corn kernels and coconut milk.",
    seconds=20)

add(PGD, "Growth rate", "Basic", "statement_pair",
    sp("When a cell population grows geometrically on a limited nutrient supply, the phases of its growth follow "
       "the sequence lag phase, then log (exponential) phase, then stationary phase.",
       "A root elongating at a constant rate is an example of arithmetic growth."),
    SP("A"),
    "Geometric and arithmetic growth",
    "NCERT: in geometric growth, the initial growth is slow (lag phase), and it increases rapidly thereafter at an "
    "exponential rate (log or exponential phase); with limited nutrient supply the growth slows down, leading to "
    "a stationary phase (Statement I true). In arithmetic growth, following mitosis only one daughter cell "
    "continues to divide, and NCERT's example is a root elongating at a constant rate (Statement II true).",
    ["Geometric: lag → log → stationary", "Arithmetic: constant rate, e.g. root elongation"],
    C11_PG("growth: growth rates"),
    seconds=30)

add(PGD, "Plant growth regulators", "Intermediate", "statement_pair",
    sp("Both gibberellins and ethylene can bring about elongation of internodes (in rosette plants and in "
       "deep-water rice, respectively).",
       "Both cytokinins and abscisic acid stimulate the closure of stomata."),
    SP("C"),
    "Comparing the effects of PGRs",
    "NCERT: gibberellins promote bolting (internode elongation just prior to flowering) in beet, cabbages and "
    "other rosette plants, and ethylene promotes rapid internode/petiole elongation in deep-water rice plants "
    "(Statement I true). Stimulating the closure of stomata is listed only for abscisic acid; NCERT gives no such "
    "role for cytokinins, whose effects include new leaves, chloroplasts, lateral shoot growth and delay of leaf "
    "senescence (Statement II false).",
    ["GA: bolting; ethylene: deep-water rice → I true", "Stomatal closure: ABA only → II false"],
    C11_PG("plant growth regulators: physiological effects"),
    seconds=40)

add(PGD, "Differentiation and redifferentiation", "Intermediate", "match_list",
    ml(("example", "term"),
       ["Interfascicular cambium arising from fully differentiated parenchyma cells",
        "Cells cut off by the cork cambium losing the capacity to divide and maturing as cork cells",
        "Cells derived from the root apical meristem maturing into tracheary elements",
        "Leaves of buttercup formed in air differing in shape from those formed in water"],
       ["Plasticity", "Dedifferentiation", "Redifferentiation", "Differentiation"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,IV,III,I"), mc("II,III,I,IV")], "D"),
    "Differentiation, dedifferentiation, redifferentiation and plasticity",
    "NCERT: cells derived from root and shoot apical meristems and cambium differentiate and mature to perform "
    "specific functions (differentiation, C-IV). Living differentiated cells that regain the capacity to divide "
    "show dedifferentiation, e.g. formation of interfascicular cambium and cork cambium from fully differentiated "
    "parenchyma (A-II). Cells produced by such dedifferentiated meristems (e.g. cork cells cut off by the cork "
    "cambium) again lose the capacity to divide and mature: redifferentiation (B-III). Heterophylly in "
    "buttercup, caused by the environment, illustrates plasticity (D-I).",
    ["Parenchyma → cambium: dedifferentiation", "Cork cambium products maturing: redifferentiation",
     "Apical meristem products maturing: differentiation", "Heterophylly: plasticity"],
    C11_PG("differentiation, dedifferentiation and redifferentiation; development"),
    why="The wrong codes swap dedifferentiation with redifferentiation, or differentiation with "
        "redifferentiation, or plasticity with differentiation.",
    seconds=50)

add(PGD, "Plant growth regulators", "Intermediate", "multi_statement",
    ms("In which of the following pairs do the two PGRs have OPPOSITE effects on the process named, according to "
       "NCERT?",
       ["Auxin and cytokinin: apical dominance",
        "Abscisic acid and gibberellins: in most situations, as NCERT generalises",
        "Abscisic acid and ethylene: seed germination (ethylene in peanut seeds)",
        "Auxin and ethylene: flowering in pineapple",
        "Gibberellins and cytokinins: senescence"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "d", "e"], ["a", "c", "e"]], "A"),
    "Antagonistic and similar PGR effects",
    "Auxin causes apical dominance while cytokinins help to overcome it (a, opposite). NCERT: in most situations "
    "ABA acts as an antagonist to GAs (b, opposite). ABA inhibits seed germination, whereas ethylene initiates "
    "germination in peanut seeds (c, opposite). Both auxin and ethylene promote flowering in pineapple (d, same "
    "effect), and both gibberellins and cytokinins delay senescence (e, same effect).",
    ["(a), (b), (c): opposite", "(d), (e): same direction"],
    C11_PG("plant growth regulators: physiological effects"),
    why="(d) and (e) are pairs that act in the same direction, so any option containing them is wrong; '(a), (c) "
        "and (e)' also omits (b).",
    seconds=50)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Gardeners use 2,4-D to prepare weed-free lawns.",
       "Natural auxins are generally produced by the growing apices of stems and roots, from where they migrate "
       "to the regions of their action."),
    AR("B"),
    "2,4-D as a herbicide",
    "NCERT: 2,4-D, widely used to kill dicotyledonous weeds, does not affect mature monocotyledonous plants, and "
    "gardeners use it to prepare weed-free lawns (A true): the lawn grass is a monocot. R is a true NCERT line "
    "about where natural auxins are made and how they move, but 2,4-D is a synthetic auxin sprayed on the lawn; "
    "its use rests on its selective killing of dicot weeds, not on where natural auxins are produced. So R does "
    "not explain A.",
    ["A: true (2,4-D kills dicot weeds, spares grasses)", "R: true, about natural auxin synthesis", "R unrelated "
     "to A"],
    C11_PG("plant growth regulators: auxins"),
    seconds=40)

add(PGD, "Plant growth regulators", "Advanced", "multi_statement",
    ms("A grower has only gibberellins available. Which of the following results can the grower obtain with them, "
       "according to NCERT?",
       ["Longer grape stalks",
        "Speeding up of the malting process in brewing",
        "Bolting of cabbage plants",
        "Early seed production by juvenile conifers",
        "Sprouting of potato tubers"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["b", "c", "d", "e"], ["a", "c", "d"]], "C"),
    "Uses of gibberellins",
    "NCERT lists for gibberellins: increasing the length of grape stalks (a); speeding up the malting process in "
    "the brewing industry (b); bolting in beet, cabbages and other rosette plants (c); and hastening maturity of "
    "juvenile conifers, leading to early seed production (d). Sprouting of potato tubers is an effect of "
    "ethylene (e), which breaks seed and bud dormancy.",
    ["GA: (a), (b), (c), (d)", "Potato sprouting: ethylene"],
    C11_PG("plant growth regulators: gibberellins; ethylene"),
    why="Options with (e) credit gibberellins with an ethylene effect; '(a), (c) and (d)' leaves out malting.",
    seconds=55)

add(PGD, "Growth rate", "Advanced", "statement_pair",
    sp("Two leaves can show the same absolute increase in area in a given time and yet have different relative "
       "growth rates.",
       "In geometric growth, the absolute increase per unit time stays constant throughout the exponential phase."),
    SP("C"),
    "Absolute versus relative growth rate",
    "NCERT: absolute growth rate is the total growth per unit time; relative growth rate is the growth per unit "
    "time per unit initial parameter. NCERT's figure shows leaves A and B both increasing their area by 5 cm² in "
    "a given time, yet with different relative growth rates because their initial sizes differ (Statement I "
    "true). In geometric growth, W₁ = W₀e^(rt): r is constant, so the absolute increase per unit time keeps rising "
    "as the size rises; a constant absolute increase describes arithmetic growth (Statement II false).",
    ["Same absolute growth, different initial size → different RGR", "Geometric: constant r, rising absolute "
     "rate"],
    C11_PG("growth: growth rates"),
    seconds=50)

_aims = {"thinning cotton by fruit abscission": "ethylene (ethephon)", "female flowers in cucumber": "ethylene (ethephon)",
         "rooting of stem cuttings": "auxin"}
assert len(set(_aims.values())) == 2

add(PGD, "Plant growth regulators", "Advanced", "direct",
    "A grower wants to (i) thin a cotton crop by accelerating the abscission of flowers and fruits, (ii) increase "
    "the number of female flowers in cucumbers, and (iii) initiate rooting in stem cuttings. Using NCERT's "
    "accounts, what is the minimum number of different plant growth regulators needed?",
    P("Two", ["One", "Three", "Four"], "B"),
    "Matching aims to PGRs",
    "NCERT: ethephon (which releases ethylene) accelerates abscission in flowers and fruits, used for thinning of "
    "cotton, cherry and walnut (i), and ethylene promotes female flowers in cucumbers, thereby increasing the yield "
    "(ii). Initiating rooting in stem cuttings is a use of auxins (iii). So two PGRs, ethylene and an auxin, are "
    "enough.",
    ["(i) ethylene", "(ii) ethylene", "(iii) auxin", "Distinct PGRs = 2"],
    C11_PG("plant growth regulators: auxins; ethylene"),
    why="One PGR cannot do all three, since rooting of cuttings is an auxin effect; three or four would count "
        "ethylene twice or add PGRs that are not needed.",
    seconds=45)

# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "In a transverse section, a typical microsporangium is surrounded by four wall layers. Which layer lies "
    "immediately inside the epidermis?",
    P("Endothecium", ["Tapetum", "Middle layers", "Sporogenous tissue"], "D"),
    "Wall layers of the microsporangium",
    "NCERT: a typical microsporangium is generally surrounded by four wall layers, from outside inwards the "
    "epidermis, endothecium, middle layers and the tapetum. The outer three layers protect the anther and help in "
    "dehiscence; the innermost tapetum nourishes the developing pollen grains. The sporogenous tissue occupies "
    "the centre and is not a wall layer.",
    ["Order: epidermis → endothecium → middle layers → tapetum", "Just inside the epidermis: endothecium"],
    C12_SR("pre-fertilisation: structure of microsporangium"),
    why="The tapetum is the innermost wall layer and the middle layers lie between the endothecium and the "
        "tapetum; the sporogenous tissue fills the centre.",
    seconds=20)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "In flowering plants, the female gametophyte is the:",
    P("Embryo sac", ["Ovule", "Nucellus", "Megaspore mother cell"], "D"),
    "Female gametophyte",
    "NCERT: the functional megaspore develops into the female gametophyte (embryo sac). The ovule is the "
    "megasporangium, the nucellus is the mass of cells within the integuments in which the embryo sac lies, and "
    "the megaspore mother cell is the diploid cell that undergoes meiosis to give the megaspores.",
    ["Functional megaspore → female gametophyte", "= embryo sac"],
    C12_SR("pre-fertilisation: female gametophyte"),
    why="The ovule is the megasporangium, the nucellus is sporangial tissue enclosing the embryo sac, and the "
        "megaspore mother cell is diploid and precedes the gametophyte.",
    seconds=20)

add(SRFP, "Pollination", "Basic", "direct",
    "A bee visiting a bisexual flower transfers pollen grains from the anthers of that flower to the stigma of "
    "the same flower. This kind of pollination is:",
    P("Autogamy", ["Geitonogamy", "Xenogamy", "Cleistogamy"], "B"),
    "Kinds of pollination",
    "NCERT: autogamy is the transfer of pollen grains from the anther to the stigma of the same flower. "
    "Geitonogamy is transfer to another flower of the same plant, and xenogamy to the stigma of a different "
    "plant. The agent involved does not change the definition; what matters is the source and destination of "
    "the pollen.",
    ["Same flower → autogamy", "Another flower, same plant → geitonogamy", "Different plant → xenogamy"],
    C12_SR("pollination: kinds of pollination"),
    why="Geitonogamy and xenogamy need a different flower or a different plant; cleistogamy is a kind of flower "
        "that never opens, not a term for pollen transfer in an open flower.",
    seconds=20)

add(SRFP, "Endosperm and embryo", "Basic", "statement_pair",
    sp("In a typical dicotyledonous embryo, the cylindrical portion of the embryonal axis below the level of the "
       "cotyledons is the hypocotyl, which terminates at its lower end in the radicle or root tip.",
       "In a dicotyledonous embryo, the root tip is covered with a root cap."),
    SP("A"),
    "Parts of the dicot embryo",
    "NCERT: a typical dicotyledonous embryo consists of an embryonal axis and two cotyledons. The portion above "
    "the cotyledons is the epicotyl, ending in the plumule; the cylindrical portion below is the hypocotyl, which "
    "terminates at its lower end in the radicle or root tip (Statement I true). The root tip is covered with a "
    "root cap (Statement II true).",
    ["Above cotyledons: epicotyl → plumule", "Below: hypocotyl → radicle", "Root tip has a root cap"],
    C12_SR("post-fertilisation: embryo"),
    seconds=25)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Basic", "assertion_reason",
    ar("Parthenocarpic fruits, such as those of banana, are seedless.",
       "Parthenocarpic fruits develop without fertilisation."),
    AR("A"),
    "Parthenocarpy",
    "NCERT: in a few species such as banana, fruits develop without fertilisation; such fruits are called "
    "parthenocarpic fruits, and parthenocarpy can also be induced through growth hormones, giving seedless "
    "fruits. Since there is no fertilisation, ovules do not mature into seeds, so the fruit is seedless: R "
    "directly explains A.",
    ["No fertilisation → no seeds", "So parthenocarpic fruits are seedless"],
    C12_SR("apomixis and polyembryony; post-fertilisation: seed and fruit (parthenocarpy)"),
    seconds=25)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "Pollen grains of a large number of species can be stored for years in pollen banks for use in crop breeding "
    "programmes. NCERT states that they are stored in:",
    P("Liquid nitrogen at −196 °C", ["A refrigerator at 4 °C", "A 10 per cent sugar solution",
                                      "Dry air at room temperature"], "C"),
    "Storage of pollen",
    "NCERT: it is possible to store pollen grains of a large number of species for years in liquid nitrogen "
    "(−196 °C). Such stored pollen can be used as pollen banks, similar to seed banks, in crop breeding "
    "programmes.",
    ["Storage medium: liquid nitrogen", "Temperature: −196 °C", "Use: pollen banks for breeding"],
    C12_SR("pre-fertilisation: pollen grain (viability and storage)"),
    why="NCERT names only liquid nitrogen for long-term storage; a 10 per cent sugar solution is used for "
        "germinating pollen on a slide, and pollen of many species loses viability within minutes to months at "
        "ordinary conditions.",
    seconds=20)

_cells = {"synergids": 2, "antipodals": 3, "cells": 7, "nuclei": 8}
assert _cells["cells"] == 3 + 2 + 1 + 1 and _cells["nuclei"] == 3 + 2 + 1 + 2

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "match_list",
    ml(("feature of a typical mature embryo sac", "number"),
       ["Synergids", "Antipodal cells", "Cells in all", "Nuclei in all"],
       ["2", "3", "7", "8"]),
    M(mc("I,II,III,IV"), [mc("II,I,III,IV"), mc("I,II,IV,III"), mc("II,I,IV,III")], "B"),
    "Counting the cells of the embryo sac",
    "NCERT: of the eight nuclei, three at the micropylar end form the egg apparatus (two synergids and one egg "
    "cell), three at the chalazal end form the antipodals, and the two polar nuclei lie in the large central "
    "cell. Cells: 2 + 1 + 3 + 1 = 7; nuclei: 2 + 1 + 3 + 2 = 8. So the embryo sac is 8-nucleate and 7-celled.",
    ["Synergids 2, egg 1, antipodals 3, central cell 1 (2 nuclei)", "7 cells, 8 nuclei"],
    C12_SR("pre-fertilisation: female gametophyte"),
    why="The wrong codes swap the synergids (2) with the antipodals (3) or the cells (7) with the nuclei (8).",
    seconds=40, verified_by=RECOMPUTED)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "multi_statement",
    ms("Which of the following events are included in what NCERT calls pollen-pistil interaction?",
       ["Recognition of the pollen by the pistil as compatible or incompatible",
        "Germination of a compatible pollen grain on the stigma",
        "Growth of the pollen tube through the tissues of the stigma and style",
        "Fusion of a male gamete with the egg cell",
        "Formation of the primary endosperm cell"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Scope of pollen-pistil interaction",
    "NCERT: all the events from pollen deposition on the stigma until the pollen tubes enter the ovule are "
    "together referred to as pollen-pistil interaction. These include recognition by the pistil (a), germination "
    "of a compatible pollen grain (b) and growth of the pollen tube through stigma and style (c). Syngamy (d) and "
    "the formation of the primary endosperm cell by triple fusion (e) occur later, inside the embryo sac.",
    ["From pollen deposition to entry of the tube into the ovule", "(d), (e) happen inside the embryo sac"],
    C12_SR("pre-fertilisation: pollen-pistil interaction"),
    why="Options with (d) or (e) include fertilisation events, which come after pollen-pistil interaction.",
    seconds=40)

add(SRFP, "Double fertilisation", "Intermediate", "assertion_reason",
    ar("In flowering plants, the pollen tube must deliver two male gametes into an embryo sac.",
       "One male gamete fuses with the egg cell, and the other fuses with the two polar nuclei in the central "
       "cell."),
    AR("A"),
    "Why two male gametes are needed",
    "NCERT: the pollen tube releases the two male gametes into the cytoplasm of a synergid. One male gamete fuses "
    "with the egg nucleus (syngamy) to form the zygote; the other fuses with the two polar nuclei (triple fusion) "
    "to form the primary endosperm nucleus. Since two separate fusions occur, two male gametes are needed: R is "
    "the reason for A.",
    ["Syngamy uses one male gamete", "Triple fusion uses the other", "Hence two per embryo sac"],
    C12_SR("double fertilisation"),
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "In a species with bisexual flowers, the pollen of each flower is released well before the stigma of that "
    "flower becomes receptive. This lack of synchrony mainly discourages:",
    P("Self-pollination (autogamy) within the same flower",
      ["Cross-pollination between different plants", "Germination of compatible pollen on a receptive stigma",
       "Pollination by insects"], "D"),
    "Non-synchronous pollen release and stigma receptivity",
    "NCERT: flowering plants have devices to discourage self-pollination and encourage cross-pollination. In "
    "some species, pollen release and stigma receptivity are not synchronised: either the pollen is released "
    "before the stigma becomes receptive, or the stigma becomes receptive much before pollen release. By the "
    "time the stigma is ready, the flower's own pollen is gone, so pollination within the same flower is "
    "discouraged.",
    ["Own pollen shed before own stigma is receptive", "Autogamy discouraged"],
    C12_SR("outbreeding devices"),
    why="The device is meant to encourage, not prevent, cross-pollination; compatible pollen still germinates on "
        "a receptive stigma; and nothing here affects which agent carries the pollen.",
    seconds=35)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "In which of the following seeds does a triploid storage tissue persist at maturity?",
    P("Castor", ["Pea", "Groundnut", "Beans"], "D"),
    "Albuminous and non-albuminous seeds",
    "The endosperm develops from the triploid primary endosperm nucleus. NCERT: in pea, groundnut and beans the "
    "endosperm is completely consumed by the developing embryo before seed maturation (non-albuminous seeds), "
    "whereas in castor a portion of the endosperm persists in the mature seed (albuminous seed). So only castor "
    "retains a triploid tissue.",
    ["Endosperm = triploid", "Persists in castor (albuminous)", "Consumed in pea, groundnut, beans"],
    C12_SR("post-fertilisation: endosperm; seed"),
    why="Pea, groundnut and beans are NCERT's examples of non-albuminous seeds, whose food reserves lie in the "
        "cotyledons of the diploid embryo.",
    seconds=30)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "assertion_reason",
    ar("The tapetum performs the function of protection and helps in the dehiscence of the anther.",
       "Cells of the tapetum possess dense cytoplasm and generally have more than one nucleus."),
    AR("D"),
    "Functions of the anther wall layers",
    "NCERT: the outer three wall layers (epidermis, endothecium and middle layers) perform the function of "
    "protection and help in dehiscence of the anther to release the pollen. The innermost tapetum nourishes the "
    "developing pollen grains, so A is false. R is a true NCERT description of tapetal cells.",
    ["Protection and dehiscence: outer three layers → A false", "Tapetum: dense cytoplasm, often multinucleate "
     "→ R true"],
    C12_SR("pre-fertilisation: structure of microsporangium"),
    seconds=35)

add(SRFP, "Double fertilisation", "Intermediate", "statement_pair",
    sp("After entering one of the synergids, the pollen tube releases the two male gametes into the cytoplasm of "
       "that synergid.",
       "Following fertilisation, the synergids and antipodals degenerate."),
    SP("A"),
    "Events in the embryo sac at fertilisation",
    "NCERT: the pollen tube enters one of the synergids through the filiform apparatus and releases the two male "
    "gametes into the cytoplasm of the synergid (Statement I true). After double fertilisation, the zygote "
    "develops into the embryo and the primary endosperm cell into the endosperm, while the synergids and "
    "antipodals degenerate (Statement II true).",
    ["Male gametes released into a synergid", "Synergids and antipodals then degenerate"],
    C12_SR("double fertilisation"),
    seconds=30)

add(SRFP, "Double fertilisation", "Intermediate", "direct",
    "In an ovule, a male gamete fuses with the egg, but the second male gamete fails to fuse with the polar "
    "nuclei. Which structure that normally results from double fertilisation will NOT be formed in this embryo sac?",
    P("The primary endosperm cell", ["The zygote", "The pollen tube", "The filiform apparatus"], "C"),
    "Products of the two fusions",
    "NCERT: fusion of a male gamete with the egg (syngamy) forms the diploid zygote; fusion of the other male "
    "gamete with the two polar nuclei (triple fusion) forms the triploid primary endosperm nucleus, making the "
    "central cell the primary endosperm cell. If triple fusion fails, the primary endosperm cell (and the "
    "endosperm that comes from it) is not formed, though syngamy has produced a zygote.",
    ["Syngamy happened → zygote formed", "Triple fusion failed → no primary endosperm cell"],
    C12_SR("double fertilisation"),
    why="The zygote comes from syngamy, which took place; the pollen tube and the filiform apparatus exist "
        "before fertilisation and are not its products.",
    seconds=35)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Advanced", "multi_statement",
    ms("A flowering plant has the genotype Aa. Which of the following statements about its progeny are correct?",
       ["Seeds from its cleistogamous flowers can contain embryos of genotype AA, Aa or aa.",
        "Seeds formed by geitonogamy have the same possible embryo genotypes as seeds formed by autogamy.",
        "Its nucellar embryos, in a species with nucellar polyembryony, can be of genotype aa.",
        "The seed coat of every seed it bears is of genotype Aa.",
        "Embryos formed apomictically from a diploid egg made without reduction division can be AA or aa."]),
    MS(["a", "b", "d"], [["a", "b", "c", "d"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
    "Genetic consequences of modes of seed formation",
    "Cleistogamous flowers are invariably autogamous, so the embryos come from self-fertilisation of Aa and may "
    "be AA, Aa or aa (a). NCERT: geitonogamy is genetically similar to autogamy, since the pollen comes from the "
    "same plant (b). The seed coat develops from the integuments of the mother plant, so it is Aa (d). Nucellar "
    "embryos arise from diploid nucellar cells of the mother without fertilisation, so they are Aa, not aa (c "
    "false). An apomictic embryo from a diploid egg formed without reduction division keeps the mother's "
    "genotype Aa; there is no segregation (e false).",
    ["Self/geitonogamy: Aa × Aa → AA, Aa, aa", "Maternal tissues and apomicts: Aa"],
    C12_SR("pollination; apomixis and polyembryony; post-fertilisation: seed"),
    why="Options with (c) or (e) let apomictic or nucellar embryos segregate; '(b), (d) and (e)' also omits (a).",
    seconds=60)

_spor, _pmc = 4, 25
_grains = _spor * _pmc * 4
_male = _grains * 2
assert (_grains, _male) == (400, 800)

add(SRFP, "Microsporogenesis and male gametophyte", "Advanced", "numerical",
    "An anther has four microsporangia, each with 25 pollen mother cells. All of them complete microsporogenesis "
    "normally, and the species sheds its pollen at the 3-celled stage. How many male gametes are present in all "
    "the pollen grains of this anther at the time of shedding?",
    P("800", ["400", "200", "1600"], "D"),
    "Counting male gametes in 3-celled pollen",
    "Pollen mother cells = 4 × 25 = 100. Each undergoes meiosis to give a tetrad of four microspores, so there are "
    "400 pollen grains. A pollen grain shed at the 3-celled stage contains one vegetative cell and two male "
    "gametes, so male gametes = 400 × 2 = 800.",
    ["PMCs = 4 × 25 = 100", "Pollen grains = 100 × 4 = 400", "Male gametes = 400 × 2 = 800"],
    C12_SR("pre-fertilisation: microsporogenesis; pollen grain"),
    why="400 counts one male gamete per pollen grain; 200 forgets that each PMC gives four microspores and uses "
        "two; 1600 counts four male gametes per pollen grain instead of two.",
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Endosperm and embryo", "Advanced", "multi_statement",
    ms("Which of the following pairs of structures have the SAME ploidy in a typical flowering plant?",
       ["Perisperm and seed coat",
        "Zygote and a cell of the nucellus",
        "Endosperm and pericarp",
        "A synergid and an antipodal cell",
        "Primary endosperm nucleus and a polar nucleus"]),
    MS(["a", "b", "d"], [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "d", "e"]], "D"),
    "Ploidy of seed and embryo-sac tissues",
    "Perisperm is the persistent nucellus and the seed coat comes from the integuments: both are diploid "
    "maternal tissues (a). The zygote (syngamy) and nucellar cells are both diploid (b). Synergids and antipodals "
    "are cells of the haploid embryo sac (d). The endosperm is triploid while the pericarp (ovary wall) is diploid "
    "(c, different). The primary endosperm nucleus is triploid, but each polar nucleus is haploid (e, different).",
    ["2n: perisperm, seed coat, zygote, nucellus, pericarp", "n: synergid, antipodal, polar nucleus",
     "3n: endosperm, PEN"],
    C12_SR("pre-fertilisation: female gametophyte; double fertilisation; post-fertilisation: seed"),
    why="Options with (c) or (e) pair a triploid tissue with a diploid or haploid one.",
    seconds=55)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Advanced", "statement_pair",
    sp("In many Citrus varieties, the development of embryos from nucellar cells that protrude into the embryo sac "
       "is a form of apomixis.",
       "The development of a banana fruit without fertilisation is an example of apomixis."),
    SP("C"),
    "Apomixis versus parthenocarpy",
    "NCERT describes apomixis as the production of seeds without fertilisation, a form of asexual reproduction "
    "that mimics sexual reproduction. It names two routes: a diploid egg formed without reduction division "
    "developing into the embryo, and, more often, nucellar cells dividing and protruding into the embryo sac to "
    "form embryos, as in many Citrus and mango varieties (Statement I true). A banana fruit developing without "
    "fertilisation is parthenocarpy: a fruit, not a seed, is formed without fertilisation (Statement II false).",
    ["Apomixis: seeds without fertilisation (Citrus nucellar embryos)", "Parthenocarpy: fruit without "
     "fertilisation (banana)"],
    C12_SR("apomixis and polyembryony; post-fertilisation: fruit"),
    seconds=45)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "match_list",
    ml(("device", "effect"),
       ["Dioecy, as in papaya", "Unisexual flowers on a monoecious plant, as in castor",
        "Self-incompatibility", "Cleistogamy"],
       ["Prevents autogamy but not geitonogamy",
        "Prevents both autogamy and geitonogamy",
        "Inhibits pollen germination or pollen-tube growth of self-pollen in the pistil",
        "Gives assured seed set by autogamy even in the absence of pollinators"]),
    M(mc("II,I,III,IV"), [mc("I,II,III,IV"), mc("II,I,IV,III"), mc("II,III,I,IV")], "D"),
    "Comparing outbreeding devices",
    "NCERT: when male and female flowers are on different plants (dioecy, papaya), both autogamy and geitonogamy "
    "are prevented (A-II). Unisexual flowers on the same plant (castor, maize) prevent autogamy but not "
    "geitonogamy (B-I). Self-incompatibility is a genetic mechanism that prevents self-pollen from fertilising "
    "the ovules by inhibiting pollen germination or pollen-tube growth in the pistil (C-III). Cleistogamous "
    "flowers never open, are invariably autogamous and produce assured seed set even without pollinators (D-IV).",
    ["Dioecy: blocks both", "Monoecy: blocks autogamy only", "SI: blocks self-pollen in pistil",
     "Cleistogamy: assured selfing"],
    C12_SR("outbreeding devices; pollination (cleistogamous flowers)"),
    why="The wrong codes swap dioecy and monoecy, or the effects of self-incompatibility and cleistogamy, or "
        "credit monoecy with the pistil's rejection of self-pollen.",
    seconds=55)

add(SRFP, "Endosperm and embryo", "Advanced", "assertion_reason",
    ar("In every angiosperm seed, a persistent endosperm nourishes the embryo up to and beyond seed maturity.",
       "The cells of the endosperm are filled with reserve food materials, which are used for the nutrition of "
       "the developing embryo."),
    AR("D"),
    "Fate of the endosperm",
    "NCERT: endosperm cells are filled with reserve food materials used for the nutrition of the developing "
    "embryo (R true). But the endosperm does not persist in every seed: in pea, groundnut and beans it is "
    "completely consumed by the developing embryo before seed maturation (non-albuminous seeds), and the food is "
    "stored in the cotyledons. Only in albuminous seeds such as wheat, maize, barley, castor and coconut does a "
    "part of it persist. So A is false.",
    ["R: true NCERT statement", "A: false; non-albuminous seeds lack endosperm at maturity"],
    C12_SR("post-fertilisation: endosperm; seed"),
    seconds=40)

# ================================================================ Principles of Inheritance and Variation (7 / 9 / 7)
C12_PI = lambda s: ref(12, PIV, s)


def cross(p1, p2):
    """Offspring genotypes (sorted allele tuples per gene) of two multi-gene genotypes given as lists of pairs."""
    out = Counter()
    g1 = list(product(*p1))
    g2 = list(product(*p2))
    for a in g1:
        for b in g2:
            out[tuple("".join(sorted(x + y)) for x, y in zip(a, b))] += F(1, len(g1) * len(g2))
    return out


def abo(p1, p2):
    res = Counter()
    for a in p1:
        for b in p2:
            s = {a, b}
            grp = "AB" if s == {"A", "B"} else ("A" if "A" in s else ("B" if "B" in s else "O"))
            res[grp] += F(1, 4)
    return res


add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Which of the following was NOT one of the seven characters of the garden pea that Mendel studied?",
    P("Leaf shape", ["Pod colour", "Flower position", "Seed shape"], "A"),
    "Mendel's seven characters",
    "NCERT's table of the contrasting traits studied by Mendel lists seven characters: stem height, flower "
    "colour, flower position, pod shape, pod colour, seed shape and seed colour. Leaf shape is not among them.",
    ["Seven characters: stem height, flower colour, flower position, pod shape, pod colour, seed shape, seed "
     "colour", "Leaf shape is absent"],
    C12_PI("Mendel's laws of inheritance (table of contrasting traits)"),
    why="Pod colour (green/yellow), flower position (axial/terminal) and seed shape (round/wrinkled) are all in "
        "Mendel's list.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "In his dihybrid cross, Mendel crossed a pea plant with round, yellow seeds (RRYY) with one with wrinkled, "
    "green seeds (rryy). The F1 seeds were:",
    P("All round and yellow",
      ["Round yellow, round green, wrinkled yellow and wrinkled green in the ratio 9 : 3 : 3 : 1",
       "All wrinkled and green", "Round yellow and wrinkled green in the ratio 1 : 1"], "C"),
    "F1 of a dihybrid cross",
    "NCERT: in the cross between round yellow and wrinkled green parents, the F1 seeds were round and yellow, "
    "because round (R) is dominant over wrinkled and yellow (Y) over green. All F1 plants are RrYy. The 9 : 3 : 3 : "
    "1 ratio appears only in the F2, after the F1 is self-pollinated.",
    ["F1 genotype: RrYy", "R and Y dominant → all round yellow"],
    C12_PI("inheritance of two genes"),
    why="9 : 3 : 3 : 1 is the F2 ratio; wrinkled green is the recessive parental phenotype, hidden in the F1; a 1 : 1 "
        "ratio would need a heterozygous parent.",
    seconds=20)

add(PIV, "Multiple alleles and pleiotropy", "Basic", "statement_pair",
    sp("In the ABO blood group system, the allele i does not produce any sugar on the surface of red blood cells.",
       "The alleles Iᴬ and Iᴮ produce slightly different forms of the sugar."),
    SP("A"),
    "Products of the ABO alleles",
    "NCERT: the plasma membrane of red blood cells has sugar polymers protruding from its surface, and the kind of "
    "sugar is controlled by the gene I, which has three alleles, Iᴬ, Iᴮ and i. The alleles Iᴬ and Iᴮ produce a "
    "slightly different form of the sugar (Statement II true), while allele i does not produce any sugar "
    "(Statement I true).",
    ["Iᴬ, Iᴮ: two forms of the sugar", "i: no sugar"],
    C12_PI("inheritance of one gene: co-dominance"),
    seconds=25)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "assertion_reason",
    ar("Sickle-cell anaemia is an autosome-linked recessive trait.",
       "Thalassemia is a quantitative problem of synthesising too few globin molecules."),
    AR("B"),
    "Sickle-cell anaemia and thalassemia",
    "NCERT: sickle-cell anaemia is an autosome-linked recessive trait that can be transmitted from parents to "
    "offspring when both partners are carriers (A true). NCERT also says thalassemia differs from sickle-cell "
    "anaemia in that it is a quantitative problem of synthesising too few globin molecules (R true). R describes "
    "a different disorder and says nothing about why sickle-cell anaemia is autosomal recessive, so R does not "
    "explain A.",
    ["A: true", "R: true, about thalassemia", "R unrelated to A"],
    C12_PI("genetic disorders: Mendelian disorders"),
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "match_list",
    ml(("disorder", "chromosome involved, as given in NCERT"),
       ["β-Thalassemia", "α-Thalassemia", "Colour blindness", "Down's syndrome"],
       ["Chromosome 11", "Chromosome 16", "X chromosome", "Chromosome 21"]),
    M(mc("I,II,III,IV"), [mc("II,I,III,IV"), mc("I,II,IV,III"), mc("II,I,IV,III")], "D"),
    "Chromosomes involved in genetic disorders",
    "NCERT: β-thalassemia is controlled by a single gene, HBB, on chromosome 11 of each parent (A-I); "
    "α-thalassemia by two closely linked genes, HBA1 and HBA2, on chromosome 16 of each parent (B-II). Colour "
    "blindness is sex-linked recessive, due to a mutation in certain genes on the X chromosome (C-III). Down's "
    "syndrome is caused by an additional copy of chromosome 21 (D-IV).",
    ["β: chr 11 (HBB)", "α: chr 16 (HBA1, HBA2)", "Colour blindness: X", "Down's: trisomy 21"],
    C12_PI("genetic disorders: Mendelian disorders; chromosomal disorders"),
    why="The wrong codes swap chromosomes 11 and 16 between the two thalassemias, or swap the X chromosome with "
        "chromosome 21.",
    seconds=35)

add(PIV, "Polygenic inheritance", "Basic", "direct",
    "In NCERT's model of human skin colour controlled by three genes (A, B and C), with dominant alleles "
    "responsible for dark skin colour, how many dominant alleles does a person with the darkest skin colour carry?",
    P("Six", ["Three", "One", "Two"], "B"),
    "Additive effect in polygenic inheritance",
    "NCERT: the genotype with all dominant alleles (AABBCC) has the darkest skin colour and the one with all "
    "recessive alleles (aabbcc) the lightest. Three genes in a diploid give six alleles, so the darkest person "
    "carries six dominant alleles. AaBbCc, with three dominant alleles, has an intermediate skin colour.",
    ["Three genes × 2 alleles = 6", "Darkest = AABBCC → 6 dominant alleles"],
    C12_PI("polygenic inheritance"),
    why="Three is the intermediate AaBbCc; one or two dominant alleles give lighter shades.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "assertion_reason",
    ar("A true-breeding tall pea plant (TT), on self-pollination, gives only tall progeny.",
       "A homozygous parent produces two kinds of gametes in equal proportion."),
    AR("C"),
    "Gametes of a homozygous parent",
    "NCERT: in a homozygous parent all the gametes are similar, while a heterozygous parent produces two kinds of "
    "gametes, each having one allele, in equal proportion. TT forms only T gametes, so all progeny of selfing are "
    "TT and tall (A true). R is false: two kinds of gametes come only from a heterozygote.",
    ["TT → only T gametes → TT progeny, all tall", "Two kinds of gametes: heterozygote only → R false"],
    C12_PI("inheritance of one gene: law of segregation"),
    seconds=25)

_tc = cross([("A", "a"), ("B", "b"), ("C", "c")], [("a", "a"), ("b", "b"), ("c", "c")])
_pheno = Counter()
for _g, _p in _tc.items():
    _pheno[tuple(any(ch.isupper() for ch in x) for x in _g)] += _p
assert len(_pheno) == 8 and _pheno[(False, False, False)] == F(1, 8)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "A plant heterozygous for three independently assorting genes (AaBbCc), each with complete dominance, is "
    "test-crossed with aabbcc. How many phenotypic classes appear in the progeny, and what fraction of the "
    "progeny shows all three recessive traits?",
    P("8 classes; 1/8", ["8 classes; 1/64", "27 classes; 1/8", "4 classes; 1/4"], "B"),
    "Test cross of a trihybrid",
    "The heterozygote AaBbCc forms 2³ = 8 kinds of gametes in equal proportion (independent assortment); the "
    "aabbcc parent forms only abc. In a test cross, each gamete of the heterozygote shows up directly as a "
    "phenotype, so there are 8 classes, each 1/8. The all-recessive class (aabbcc) is 1/8.",
    ["Gametes of AaBbCc: 2³ = 8, each 1/8", "Test cross: phenotype classes = gamete kinds", "aabbcc = 1/8"],
    C12_PI("inheritance of two genes: law of independent assortment; test cross"),
    why="1/64 is the aabbcc fraction for AaBbCc × AaBbCc, not a test cross; 27 is the number of genotypes in a "
        "trihybrid self; 4 classes and 1/4 fit a dihybrid test cross.",
    seconds=60, verified_by=RECOMPUTED)

_ab, _bc = 12, 5
assert _ab + _bc == 17

add(PIV, "Linkage and crossing over", "Intermediate", "numerical",
    "Sturtevant used the frequency of recombination between gene pairs on the same chromosome as a measure of "
    "the distance between them. Genes A, B and C lie on one chromosome, with B between A and C. The recombination "
    "frequency is 12 per cent between A and B and 5 per cent between B and C. On this map, the distance between "
    "A and C is:",
    P("17 units", ["7 units", "60 units", "8.5 units"], "A"),
    "Gene mapping by recombination frequency",
    "Since recombination frequency is used as a measure of distance and B lies between A and C, the map "
    "distances add: A–C = A–B + B–C = 12 + 5 = 17 units.",
    ["B between A and C", "Distances add: 12 + 5 = 17"],
    C12_PI("linkage and recombination"),
    why="7 subtracts the distances (correct only if C lay between A and B); 60 multiplies them; 8.5 averages them.",
    seconds=40, verified_by=RECOMPUTED)

assert set(abo("BB", "AB")) == {"B", "AB"}

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "direct",
    "A woman of genotype IᴮIᴮ marries a man with blood group AB. Which blood groups are possible among their "
    "children?",
    P("B and AB only", ["A, B and AB", "B only", "A, B, AB and O"], "C"),
    "ABO crosses",
    "The woman forms only Iᴮ gametes; the man forms Iᴬ and Iᴮ gametes in equal numbers. Children are IᴬIᴮ "
    "(blood group AB, since Iᴬ and Iᴮ are co-dominant) or IᴮIᴮ (blood group B), in a 1 : 1 ratio. No child can "
    "be A or O, because every child receives Iᴮ from the mother.",
    ["Mother: Iᴮ only", "Father: Iᴬ or Iᴮ", "Children: IᴬIᴮ (AB) or IᴮIᴮ (B)"],
    C12_PI("inheritance of one gene: co-dominance (ABO blood groups)"),
    why="Group A needs no Iᴮ from the mother, which is impossible; group O needs i from both parents; 'B only' "
        "ignores the father's Iᴬ gametes.",
    seconds=35, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "statement_pair",
    sp("Failure of cytokinesis after the telophase stage of cell division results in an increase in a whole set "
       "of chromosomes, a condition called polyploidy.",
       "Failure of segregation of chromatids during the cell division cycle results in the gain or loss of a "
       "chromosome, a condition called aneuploidy."),
    SP("A"),
    "Polyploidy and aneuploidy",
    "NCERT: failure of segregation of chromatids during cell division results in the gain or loss of a "
    "chromosome(s), called aneuploidy (Statement II true). Failure of cytokinesis after telophase results in an "
    "increase in a whole set of chromosomes in an organism, known as polyploidy, often seen in plants (Statement "
    "I true).",
    ["Cytokinesis failure → whole sets → polyploidy", "Chromatid non-segregation → single chromosomes → "
     "aneuploidy"],
    C12_PI("genetic disorders: chromosomal disorders"),
    seconds=30)

add(PIV, "Sex-linked inheritance", "Intermediate", "multi_statement",
    ms("A colour-blind man marries a woman with normal vision who is a carrier of colour blindness. Which of the "
       "following statements about their children are correct?",
       ["Half of their daughters are expected to be colour blind.",
        "Half of their sons are expected to be colour blind.",
        "Every daughter will carry at least one allele for colour blindness.",
        "No son receives the allele for colour blindness from the father.",
        "None of their children will have normal vision."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "X-linked recessive inheritance",
    "Father XᶜY; mother XᶜX. Daughters get Xᶜ from the father and Xᶜ or X from the mother: half XᶜXᶜ (colour "
    "blind) and half XᶜX (carriers), so every daughter carries the allele (a, c). Sons get Y from the father and "
    "Xᶜ or X from the mother: half colour blind (b), and none gets the allele from the father (d). Normal-vision "
    "children exist (the XY sons and the carrier daughters), so (e) is false.",
    ["Daughters: ½ XᶜXᶜ, ½ XᶜX", "Sons: ½ XᶜY, ½ XY", "Father's Xᶜ goes only to daughters"],
    C12_PI("genetic disorders: colour blindness"),
    why="Options with (e) are wrong because the carrier daughters and half the sons see normally; '(b), (c) and "
        "(d)' leaves out (a).",
    seconds=55)

assert sum(c.isupper() for c in "AABbcc") == sum(c.isupper() for c in "aaBbCC") == 3

add(PIV, "Polygenic inheritance", "Intermediate", "assertion_reason",
    ar("In NCERT's three-gene model of human skin colour, persons of genotypes AABbcc and aaBbCC have the same "
       "skin colour.",
       "In polygenic inheritance the effect of each allele is additive, and both genotypes carry three dominant "
       "alleles."),
    AR("A"),
    "Additive alleles",
    "NCERT: in polygenic inheritance the phenotype reflects the contribution of each allele, i.e. the effect of "
    "each allele is additive. AABbcc has A, A, B (three dominant alleles) and aaBbCC has B, C, C (also three). "
    "Since only the number of dominant alleles matters, the two have the same intermediate skin colour, as does "
    "AaBbCc. R gives exactly why A is true.",
    ["Count dominant alleles: 3 and 3", "Additive effect → same phenotype"],
    C12_PI("polygenic inheritance"),
    seconds=40)

_o = {k: abo(*v)["O"] for k, v in {"A": ("Ai", "Bi"), "B": ("Ai", "ii"), "C": ("ii", "ii"), "D": ("AB", "ii")}.items()}
assert _o == {"A": F(1, 4), "B": F(1, 2), "C": F(1), "D": F(0)}

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "match_list",
    ml(("parents' genotypes", "probability that a child has blood group O"),
       ["Iᴬi × Iᴮi", "Iᴬi × ii", "ii × ii", "IᴬIᴮ × ii"],
       ["0", "1/4", "1/2", "1"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,III,I,IV"), mc("I,III,IV,II")], "A"),
    "Probability of blood group O",
    "Blood group O needs genotype ii, i.e. an i allele from each parent. Iᴬi × Iᴮi: ½ × ½ = 1/4 (A-II). Iᴬi × ii: "
    "½ × 1 = 1/2 (B-III). ii × ii: 1 (C-IV). IᴬIᴮ × ii: the AB parent has no i, so 0 (D-I).",
    ["O = ii", "Multiply each parent's chance of giving i"],
    C12_PI("inheritance of one gene: co-dominance (ABO blood groups)"),
    why="The wrong codes swap 1/4 and 1/2, or give the AB × O cross a chance of O although the AB parent carries "
        "no i.",
    seconds=50, verified_by=RECOMPUTED)

assert Counter("".join(g) for g in product("Aa", "Bb"))["ab"] == 1

add(PIV, "Sex determination", "Intermediate", "direct",
    "In honey bees, a queen of genotype AaBb (the two genes assort independently) lays unfertilised eggs. What "
    "fraction of the drones (males) produced from these eggs is expected to be of genotype ab?",
    P("1/4", ["1/16", "1/2", "0"], "D"),
    "Drones are haploid and come from the queen's eggs",
    "NCERT: in honey bees an unfertilised egg develops as a male (drone) by parthenogenesis, so a drone is "
    "haploid and carries just the genotype of the egg. The queen (AaBb) forms four kinds of eggs, AB, Ab, aB and "
    "ab, in equal proportion. Hence 1/4 of the drones are ab.",
    ["Drone = unfertilised egg (haploid)", "Eggs of AaBb: AB, Ab, aB, ab, each 1/4"],
    C12_PI("sex determination (honey bee)"),
    why="1/16 treats drones as diploid offspring of a self-cross (aabb); 1/2 counts only one gene; 0 assumes "
        "drones need a father.",
    seconds=40, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "multi_statement",
    ms("Which of the following comparisons are correct according to NCERT?",
       ["Phenylketonuria and sickle-cell anaemia are both autosomal recessive disorders.",
        "Haemophilia and colour blindness are both sex-linked recessive disorders.",
        "Sickle-cell anaemia and thalassemia both affect the globin chains of haemoglobin.",
        "Down's syndrome and Klinefelter's syndrome are both caused by point mutations.",
        "α-Thalassemia and β-thalassemia are both controlled by genes on chromosome 11."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "C"),
    "Comparing genetic disorders",
    "NCERT: phenylketonuria is an inborn error of metabolism inherited as an autosomal recessive trait, and "
    "sickle-cell anaemia is an autosome-linked recessive trait (a). Haemophilia and colour blindness are "
    "sex-linked recessive disorders (b). Sickle-cell anaemia involves a defective β-globin chain, and thalassemia "
    "a reduced synthesis of α- or β-globin (c). Down's (trisomy 21) and Klinefelter's (XXY) are chromosomal "
    "disorders from aneuploidy, not point mutations (d false). α-Thalassemia genes are on chromosome 16; only "
    "β-thalassemia's HBB is on chromosome 11 (e false).",
    ["(a), (b), (c) true", "(d): chromosomal, not point mutation", "(e): α on chromosome 16"],
    C12_PI("genetic disorders"),
    why="Options with (d) or (e) contain a false comparison; '(b), (c) and (d)' also leaves out (a).",
    seconds=50)

_cnt = sum(1 for g in product(*[["AA", "Aa", "aa"], ["BB", "Bb", "bb"], ["CC", "Cc", "cc"]])
           if sum(ch.isupper() for ch in "".join(g)) == 3)
assert _cnt == 7

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "In NCERT's three-gene model of skin colour (genes A, B and C, additive dominant alleles), how many different "
    "genotypes in total, counting AaBbCc itself, carry exactly three dominant alleles and so share its skin colour?",
    P("7", ["20", "3", "1"], "B"),
    "Counting genotypes with three dominant alleles",
    "AaBbCc has three dominant alleles, and with additive effects any genotype with exactly three dominant "
    "alleles has the same colour. Genotypes with three dominant alleles: one gene homozygous dominant, another "
    "heterozygous and the third homozygous recessive (AABbcc type): 3 × 2 = 6 arrangements; plus all three "
    "heterozygous (AaBbCc): 1. Total = 6 + 1 = 7.",
    ["(2, 1, 0) arrangements: 3! = 6", "(1, 1, 1): AaBbCc = 1", "Total 7"],
    C12_PI("polygenic inheritance"),
    why="20 is the number of the 64 F2 combinations of AaBbCc × AaBbCc that have three dominant alleles (20/64), "
        "not the number of distinct genotypes; 3 counts only one arrangement per gene (e.g. AABbcc, aaBBCc, "
        "AabbCC) and misses the rest; 1 counts only AaBbCc.",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "assertion_reason",
    ar("A colour-blind woman married to a man with normal colour vision can have colour-blind daughters.",
       "A daughter receives one X chromosome from each parent."),
    AR("D"),
    "X-linked recessive traits in daughters",
    "A daughter gets one X from her mother and one from her father (R true). A colour-blind daughter needs the "
    "recessive allele on both her X chromosomes. A father with normal vision has a normal allele on his single "
    "X, and he passes that X to every daughter; so every daughter has at least one normal allele and is a carrier "
    "with normal vision. NCERT: a daughter will normally not be colour blind unless her mother is at least a "
    "carrier and her father is colour blind. A is false.",
    ["Father's normal X → every daughter", "Daughters: carriers, not colour blind → A false", "R true"],
    C12_PI("genetic disorders: colour blindness"),
    seconds=45)

assert abo("Ai", "Bi").keys() == {"A", "B", "AB", "O"} and "O" in abo("Ai", "Ai")

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "statement_pair",
    sp("Parents with blood groups A and B can have children of all four blood groups, A, B, AB and O.",
       "Two parents who both have blood group A can have a child with blood group O."),
    SP("A"),
    "Hidden i alleles",
    "Blood group A can be IᴬIᴬ or Iᴬi, and B can be IᴮIᴮ or Iᴮi. If the parents are Iᴬi and Iᴮi, the children can "
    "be IᴬIᴮ (AB), Iᴬi (A), Iᴮi (B) or ii (O) (Statement I true). If both A parents are Iᴬi, a quarter of their "
    "children are expected to be ii, blood group O (Statement II true).",
    ["Iᴬi × Iᴮi → AB, A, B, O", "Iᴬi × Iᴬi → ¼ ii (O)"],
    C12_PI("inheritance of one gene: co-dominance (ABO blood groups)"),
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "direct",
    "A father has normal colour vision and a mother is a carrier of colour blindness (normal vision). Their "
    "daughter has Turner's syndrome (45, X0) and is colour blind. Assuming no new mutation, which explanation "
    "fits?",
    P("An egg carrying the X with the colour-blindness allele was fertilised by a sperm carrying no sex chromosome",
      ["An egg carrying no X chromosome was fertilised by an X-bearing sperm of the father",
       "A Y-bearing sperm fertilised an egg carrying no sex chromosome",
       "An egg carrying two X chromosomes was fertilised by a Y-bearing sperm"], "C"),
    "Turner's syndrome and an X-linked trait",
    "NCERT: Turner's syndrome is caused by the absence of one of the X chromosomes (45 with X0). With a single X, "
    "a recessive X-linked allele is expressed. The father's X carries the normal allele, so the lone X must have "
    "come from the mother and must be the one with the colour-blindness allele; the sperm contributed no sex "
    "chromosome.",
    ["X0: one X only", "Colour blind → that X carries the allele", "Father's X is normal → X is maternal"],
    C12_PI("genetic disorders: chromosomal disorders; colour blindness"),
    why="The father's X would give a normal-vision X0 girl; a Y with no X does not give Turner's syndrome; XX + "
        "Y gives an XXY male (Klinefelter's syndrome), not a 45, X0 female.",
    seconds=60)

_counts = {"A": len(cross([("A", "a"), ("B", "b")], [("a", "a"), ("b", "b")])),
           "B": len(cross([("A", "a"), ("B", "B")], [("A", "a"), ("B", "b")])),
           "C": len(cross([("A", "a"), ("B", "b")], [("A", "a"), ("B", "b")])),
           "D": len(cross([("A", "a"), ("B", "b"), ("C", "c")], [("A", "a"), ("B", "b"), ("C", "c")]))}
assert _counts == {"A": 4, "B": 6, "C": 9, "D": 27}

add(PIV, "Mendelian inheritance", "Advanced", "match_list",
    ml(("cross (genes assort independently)", "number of different genotypes among the progeny"),
       ["AaBb × aabb", "AaBB × AaBb", "AaBb × AaBb", "AaBbCc × AaBbCc"],
       ["4", "6", "9", "27"]),
    M(mc("I,II,III,IV"), [mc("II,I,III,IV"), mc("I,III,II,IV"), mc("I,II,IV,III")], "B"),
    "Counting genotypes gene by gene",
    "Multiply the number of genotypes for each gene. AaBb × aabb: Aa × aa gives 2 (Aa, aa) and Bb × bb gives 2, "
    "so 4 (A-I). AaBB × AaBb: Aa × Aa gives 3 and BB × Bb gives 2 (BB, Bb), so 6 (B-II). AaBb × AaBb: 3 × 3 = 9 "
    "(C-III). AaBbCc × AaBbCc: 3³ = 27 (D-IV).",
    ["Aa × aa → 2; Aa × Aa → 3; BB × Bb → 2", "Multiply across genes"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="The wrong codes treat AaBB × AaBb as giving 4 or 9 genotypes, or swap the dihybrid (9) and trihybrid "
        "(27) counts.",
    seconds=70, verified_by=RECOMPUTED)

_f2 = cross([("R", "r"), ("Y", "y")], [("R", "r"), ("Y", "y")])
_new = sum(p for g, p in _f2.items() if (g[0] != "rr") != (g[1] != "yy"))
_het = sum(p for g, p in _f2.items() if g[0] == "Rr" or g[1] == "Yy")
_rg = sum(p for g, p in _f2.items() if g[0] != "rr" and g[1] == "yy")
assert (len(_f2), _new, _het, _rg) == (9, F(3, 8), F(3, 4), F(3, 16))

add(PIV, "Mendelian inheritance", "Advanced", "multi_statement",
    ms("In Mendel's dihybrid cross RRYY × rryy, the F1 is self-pollinated. Which of the following statements about "
       "the F2 are correct?",
       ["Nine different genotypes are present.",
        "Three-eighths of the F2 show combinations of traits not seen in either parent (round green or wrinkled "
        "yellow).",
        "Three-fourths of the F2 are heterozygous for at least one of the two genes.",
        "Round, green seeds form 1/16 of the F2.",
        "All the round, yellow F2 plants are of genotype RrYy."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
    "Analysing the dihybrid F2",
    "Genotypes: 3 × 3 = 9 (a). New combinations: round green 3/16 + wrinkled yellow 3/16 = 6/16 = 3/8 (b). "
    "Homozygous at both loci: RRYY, RRyy, rrYY, rryy = 4/16, so 12/16 = 3/4 are heterozygous at one or both "
    "loci (c). Round green = 3/16, not 1/16 (d false; 1/16 is rryy). Round yellow plants include RRYY, RRYy, RrYY "
    "and RrYy, so not all are RrYy (e false).",
    ["9 genotypes", "Recombinant phenotypes 6/16", "Double homozygotes 4/16 → 12/16 heterozygous somewhere",
     "Round green 3/16"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (e)' also omits (a).",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Incomplete and co-dominance", "Advanced", "multi_statement",
    ms("Compare a pink-flowered snapdragon (Rr, incomplete dominance) with a person of blood group AB (IᴬIᴮ, "
       "co-dominance). Which statements are correct?",
       ["In both cases, the heterozygote has a phenotype different from both homozygotes.",
        "In both cases, a cross between two such heterozygotes gives three phenotypes in the ratio 1 : 2 : 1.",
        "The pink flower is in between red and white, whereas the AB person expresses both kinds of sugar.",
        "In both cases, the two alleles blend permanently, so the parental phenotypes are never recovered.",
        "In both cases, one allele completely masks the other in the heterozygote."]),
    MS(["a", "b", "c"], [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "c", "e"]], "D"),
    "Incomplete dominance versus co-dominance",
    "Snapdragon: RR red, Rr pink, rr white; NCERT notes the F2 phenotypic ratio is 1 red : 2 pink : 1 white. ABO: "
    "IᴬIᴬ (A), IᴬIᴮ (AB), IᴮIᴮ (B), and IᴬIᴮ × IᴬIᴮ gives A : AB : B = 1 : 2 : 1. So in both, the heterozygote "
    "differs from both homozygotes (a) and the 1 : 2 : 1 ratio appears (b). The pink flower is intermediate, while "
    "co-dominant Iᴬ and Iᴮ each express their own sugar (c). Red and white (or A and B) reappear in the F2, so "
    "there is no permanent blending (d false), and neither case shows complete dominance (e false).",
    ["Both: heterozygote distinct, 1 : 2 : 1", "Incomplete: intermediate; co-dominance: both expressed",
     "No blending, no masking"],
    C12_PI("inheritance of one gene: incomplete dominance; co-dominance"),
    why="Options with (d) or (e) are wrong, since parental phenotypes reappear and neither allele masks the "
        "other; '(a), (c) and (d)' also omits (b).",
    seconds=60)

# ================================================================ Molecular Basis of Inheritance (7 / 9 / 7)
C12_MB = lambda s: ref(12, MBI, s)
_COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "When a nucleoside is converted into a nucleotide, the phosphate group becomes attached at which carbon of "
    "its pentose sugar?",
    P("The 5' carbon (through its OH group)",
      ["The 1' carbon, which carries the nitrogenous base", "The 2' carbon", "The 4' carbon"], "D"),
    "From nucleoside to nucleotide",
    "NCERT: a nitrogenous base is linked to the OH of the 1' carbon of the pentose sugar through an N-glycosidic "
    "linkage to form a nucleoside. When a phosphate group is linked to the OH of the 5' carbon of the nucleoside "
    "through a phosphoester linkage, a nucleotide is formed. Two nucleotides are then joined through a 3'-5' "
    "phosphodiester linkage.",
    ["1' carbon: base (N-glycosidic linkage) → nucleoside", "5' carbon: phosphate (phosphoester) → nucleotide"],
    C12_MB("structure of polynucleotide chain"),
    why="The 1' carbon carries the base; the 2' carbon bears H in DNA or OH in RNA and is not the phosphate site; "
        "NCERT does not attach the phosphate at the 4' carbon.",
    seconds=20)

add(MBI, "DNA packaging", "Basic", "direct",
    "In a eukaryotic nucleus, histones are organised into a unit around which the DNA is wrapped. According to "
    "NCERT, this unit consists of:",
    P("Eight histone molecules (a histone octamer)",
      ["Four histone molecules (a tetramer)", "Two histone molecules (a dimer)",
       "Sixteen histone molecules"], "B"),
    "The histone octamer",
    "NCERT: histones are organised to form a unit of eight molecules called a histone octamer. The negatively "
    "charged DNA is wrapped around this positively charged octamer to form the nucleosome, which typically "
    "contains about 200 bp of DNA helix.",
    ["Histones → unit of eight = octamer", "DNA wrapped around it → nucleosome"],
    C12_MB("packaging of DNA helix"),
    why="NCERT names the unit an octamer, i.e. eight molecules, not two, four or sixteen.",
    seconds=20)

add(MBI, "Lac operon", "Basic", "direct",
    "According to NCERT, the 'lac' in the name of the lac operon refers to:",
    P("Lactose", ["Lactic acid", "Lactate dehydrogenase", "The lac insect"], "A"),
    "Naming of the lac operon",
    "NCERT: the 'lac' here refers to lactose. The lac operon of E. coli consists of the regulatory i gene and the "
    "structural genes z, y and a, whose products (β-galactosidase, permease and transacetylase) are needed to "
    "take up and use the disaccharide lactose; lactose (the substrate) also acts as the inducer.",
    ["lac = lactose", "Operon for lactose uptake and use"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Lactic acid and lactate dehydrogenase belong to fermentation, not to this operon, and the name has "
        "nothing to do with the lac insect.",
    seconds=20)

add(MBI, "Genetic code and translation", "Basic", "statement_pair",
    sp("For initiation of translation, the ribosome binds to the mRNA at the start codon AUG, which is recognised "
       "only by the initiator tRNA.",
       "There are no tRNAs for the stop codons."),
    SP("A"),
    "Initiator tRNA and stop codons",
    "NCERT: for initiation, the ribosome binds to the mRNA at the start codon (AUG) that is recognised only by "
    "the initiator tRNA (Statement I true). In discussing tRNA, NCERT notes that there are specific tRNAs for "
    "every amino acid and an initiator tRNA, but there are no tRNAs for stop codons; at the stop codon a release "
    "factor binds and terminates translation (Statement II true).",
    ["Start: AUG, initiator tRNA", "Stop codons: no tRNA; release factor"],
    C12_MB("tRNA - the adapter molecule; translation"),
    seconds=25)

add(MBI, "Replication", "Basic", "assertion_reason",
    ar("DNA ligase is required during the replication of E. coli DNA.",
       "E. coli, with 4.6 × 10⁶ bp of DNA, completes replication in about 38 minutes."),
    AR("B"),
    "Role of DNA ligase",
    "NCERT: DNA polymerases polymerise only in the 5'→3' direction, so replication is continuous on one template "
    "strand and discontinuous on the other; the discontinuously synthesised fragments are later joined by DNA "
    "ligase (A true). R is a true NCERT statement about the speed of replication (an average rate of about "
    "2000 bp per second), but speed has nothing to do with why ligase is needed. R does not explain A.",
    ["A: ligase joins the discontinuous fragments", "R: true, about the rate of replication", "R unrelated"],
    C12_MB("replication: the machinery and the enzymes"),
    seconds=30)

add(MBI, "DNA and RNA structure", "Basic", "match_list",
    ml(("nitrogenous base", "description"),
       ["Uracil", "Thymine", "Guanine", "Adenine"],
       ["Pyrimidine found in RNA in place of thymine",
        "Pyrimidine found in DNA; chemically 5-methyl uracil",
        "Purine that pairs with cytosine through three hydrogen bonds",
        "Purine that pairs with thymine through two hydrogen bonds"]),
    M(mc("I,II,III,IV"), [mc("II,I,III,IV"), mc("I,II,IV,III"), mc("II,I,IV,III")], "C"),
    "Purines, pyrimidines and base pairing",
    "NCERT: the purines are adenine and guanine; the pyrimidines are cytosine, uracil and thymine. Uracil is "
    "found in RNA at the place of thymine (A-I); thymine, present in DNA, is 5-methyl uracil (B-II). Guanine pairs "
    "with cytosine through three hydrogen bonds (C-III) and adenine with thymine through two (D-IV).",
    ["Uracil: RNA", "Thymine: DNA, 5-methyl uracil", "G≡C: three H-bonds", "A=T: two H-bonds"],
    C12_MB("structure of polynucleotide chain"),
    why="The wrong codes swap uracil with thymine, or guanine with adenine.",
    seconds=35)

add(MBI, "DNA packaging", "Basic", "assertion_reason",
    ar("In a eukaryotic nucleus, DNA is wrapped around the histone octamer to form the nucleosome.",
       "DNA is negatively charged, whereas the histone octamer is positively charged."),
    AR("A"),
    "Why DNA wraps around histones",
    "NCERT: histones are positively charged, being rich in the basic residues lysine and arginine. The "
    "negatively charged DNA is wrapped around the positively charged histone octamer to form the nucleosome. "
    "The opposite charges allow the DNA to wrap around the octamer, so R explains A.",
    ["DNA: negative (phosphates)", "Histone octamer: positive", "Opposite charges → wrapping → nucleosome"],
    C12_MB("packaging of DNA helix"),
    seconds=25)

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "NCERT uses the sentence RAM HAS RED CAP, read as three-letter words, to explain mutations. Inserting the two "
    "letters BI between HAS and RED gives RAM HAS BIR EDC AP. In a gene, this corresponds to:",
    P("Insertion of two bases, shifting the reading frame from the point of insertion",
      ["Insertion of one codon, adding one amino acid with the reading frame unaltered",
       "A base substitution that changes a single amino acid",
       "Deletion of two bases, with the reading frame restored at once"], "C"),
    "Frame-shift insertion",
    "NCERT: inserting one or two bases changes the reading frame from the point of insertion, as RAM HAS BIR EDC "
    "AP shows: every word after the insertion is altered. Inserting or deleting three (or a multiple of three) "
    "bases adds or removes one or more codons (RAM HAS BIG RED CAP), and the reading frame remains unaltered from "
    "that point onwards. Such insertions and deletions are frame-shift insertion or deletion mutations.",
    ["Two letters inserted", "All later three-letter words changed", "= insertion of 2 bases → frame shift"],
    C12_MB("genetic code: mutations and genetic code"),
    why="Adding a whole codon corresponds to inserting three letters (BIG); a substitution would change one "
        "word only; nothing was deleted here.",
    seconds=40)

add(MBI, "Lac operon", "Intermediate", "multi_statement",
    ms("Wild-type E. coli growing without glucose is given lactose. Which of the following take place, according "
       "to NCERT?",
       ["Lactose enters the cell through the permease made by the low level of lac operon expression always "
        "present.",
        "The repressor is inactivated by interaction with the inducer.",
        "RNA polymerase gains access to the promoter and transcribes the z, y and a genes.",
        "The i gene stops making the repressor.",
        "β-Galactosidase hydrolyses lactose into galactose and glucose."]),
    MS(["a", "b", "c", "e"], [["a", "b", "c", "d"], ["b", "c", "d", "e"], ["a", "c", "e"]], "B"),
    "Induction of the lac operon",
    "NCERT: a very low level of lac operon expression is always present, since without permease lactose cannot "
    "enter the cell (a). In the presence of the inducer, the repressor is inactivated by interaction with it "
    "(b), allowing RNA polymerase access to the promoter, and transcription of the polycistronic z, y, a genes "
    "proceeds (c). β-Galactosidase hydrolyses lactose into galactose and glucose (e). The repressor is "
    "synthesised all the time (constitutively) from the i gene; it is inactivated, not stopped (d false).",
    ["Permease (basal) → lactose in", "Inducer inactivates repressor", "z, y, a transcribed", "Repressor still "
     "made → (d) false"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Options with (d) wrongly stop repressor synthesis; '(a), (c) and (e)' omits the inactivation of the "
        "repressor.",
    seconds=55)

add(MBI, "DNA as genetic material", "Intermediate", "assertion_reason",
    ar("In the Hershey–Chase experiment, bacteriophages grown on a medium containing radioactive sulphur had "
       "radioactive protein but not radioactive DNA.",
       "Proteins contain sulphur, whereas DNA does not contain sulphur."),
    AR("A"),
    "Labelling with radioactive sulphur",
    "NCERT: viruses grown on radioactive sulphur contained radioactive protein but not radioactive DNA, because "
    "DNA does not contain sulphur. In the same way, phosphorus labelled only the DNA, because DNA contains "
    "phosphorus but protein does not. R is exactly the reason for A.",
    ["Sulphur: in protein, not in DNA", "So ³⁵S labels only the protein coat"],
    C12_MB("the search for genetic material: the genetic material is DNA"),
    seconds=30)

add(MBI, "Genetic code and translation", "Intermediate", "statement_pair",
    sp("Since 61 codons code for only 20 amino acids, some amino acids are coded by more than one codon.",
       "Codons in an mRNA are separated from one another by punctuations."),
    SP("C"),
    "Degenerate and comma-less code",
    "NCERT: of the 64 triplet codons, 61 code for amino acids and 3 are stop codons. With 61 codons for 20 amino "
    "acids, some amino acids are coded by more than one codon; hence the code is degenerate (Statement I true). "
    "The codon is read in mRNA in a contiguous fashion; there are no punctuations (Statement II false).",
    ["61 codons, 20 amino acids → degenerate", "Read contiguously → comma-less"],
    C12_MB("genetic code"),
    seconds=30)

add(MBI, "Genetic code and translation", "Intermediate", "match_list",
    ml(("stage of translation", "event"),
       ["Charging of tRNA", "Initiation", "Elongation", "Termination"],
       ["A release factor binds to the stop codon",
        "Amino acids are activated in the presence of ATP and linked to their cognate tRNA",
        "The ribosome binds to the mRNA at the start codon, recognised only by the initiator tRNA",
        "Amino acid–tRNA complexes sequentially bind to the appropriate codons by base pairing with the "
        "anticodons"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,IV,III,I"), mc("I,III,IV,II")], "D"),
    "Stages of translation",
    "NCERT: amino acids are activated in the presence of ATP and linked to their cognate tRNA, called charging or "
    "aminoacylation of tRNA (A-II). For initiation, the ribosome binds to the mRNA at the start codon AUG, "
    "recognised only by the initiator tRNA (B-III). During elongation, complexes of an amino acid linked to tRNA "
    "sequentially bind to the appropriate codon by forming complementary base pairs with the tRNA anticodon "
    "(C-IV). At the end, a release factor binds to the stop codon, terminating translation (D-I).",
    ["Charging: ATP, cognate tRNA", "Initiation: AUG, initiator tRNA", "Elongation: aa-tRNA on codons",
     "Termination: release factor"],
    C12_MB("translation"),
    why="The wrong codes swap charging with initiation, initiation with elongation, or charging with termination.",
    seconds=45)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("Regulation of the lac operon by the repressor is referred to as negative regulation.",
       "The lac repressor acts by binding to the promoter of the operon."),
    AR("C"),
    "Where the lac repressor binds",
    "NCERT: in the absence of an inducer, the repressor binds to the operator region of the operon and prevents "
    "RNA polymerase from transcribing it; regulation by the repressor is therefore negative regulation (A true). "
    "The repressor binds to the operator, not the promoter; the promoter is the binding site of RNA polymerase "
    "(R false).",
    ["Repressor binds operator → A true", "Promoter: RNA polymerase site → R false"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "multi_statement",
    ms("Which of the following statements comparing the classic experiments are correct, according to NCERT?",
       ["Griffith showed transformation but could not establish the biochemical nature of the 'transforming "
        "principle'.",
        "Avery, MacLeod and McCarty found that digestion with DNase inhibited transformation.",
        "Hershey and Chase provided the unequivocal proof that DNA is the genetic material.",
        "Meselson and Stahl's experiment proved that DNA, not protein, is the genetic material.",
        "Griffith used bacteriophages infecting E. coli in his experiments."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "A"),
    "The search for genetic material",
    "NCERT: Griffith's experiments showed that R strain bacteria were transformed by heat-killed S strain, but "
    "the biochemical nature of the transforming principle was not defined (a). Avery, MacLeod and McCarty found "
    "that proteases and RNases did not affect transformation, but DNase did inhibit it (b). The unequivocal proof "
    "that DNA is the genetic material came from Hershey and Chase (c). Meselson and Stahl showed that DNA "
    "replicates semiconservatively (d false), and Griffith worked with Streptococcus pneumoniae and mice (e false).",
    ["Griffith: transformation, nature unknown", "Avery et al.: DNase blocks it", "Hershey–Chase: proof",
     "Meselson–Stahl: semiconservative replication"],
    C12_MB("the search for genetic material; replication: the experimental proof"),
    why="Options with (d) or (e) misassign the Meselson–Stahl finding or Griffith's organism; '(b), (c) and (e)' "
        "also omits (a).",
    seconds=50)

add(MBI, "Replication", "Intermediate", "direct",
    "At a replication fork, one new strand is synthesised continuously and the other discontinuously. Which "
    "feature is common to BOTH?",
    P("The new strand is polymerised in the 5'→3' direction by DNA-dependent DNA polymerase",
      ["The template strand has 3'→5' polarity", "The new fragments must be joined later by DNA ligase",
       "The new strand is polymerised in the 3'→5' direction"], "C"),
    "Continuous and discontinuous synthesis",
    "NCERT: DNA-dependent DNA polymerases catalyse polymerisation only in one direction, 5'→3'. Consequently, on "
    "the template with 3'→5' polarity replication is continuous, while on the template with 5'→3' polarity it is "
    "discontinuous, and these discontinuous fragments are later joined by DNA ligase. Both new strands are made "
    "5'→3'.",
    ["Polymerase works only 5'→3'", "Template 3'→5': continuous", "Template 5'→3': discontinuous + ligase"],
    C12_MB("replication: the machinery and the enzymes"),
    why="A 3'→5' template and continuous synthesis go together, so that feature belongs to one strand only; "
        "ligase joins only the discontinuous fragments; and no strand is made 3'→5'.",
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "direct",
    "NCERT calls the Human Genome Project a 'mega project'. Which reason does it give?",
    P("The human genome has about 3 × 10⁹ bp, and at an estimated US $3 per bp sequencing would cost about "
      "9 billion US dollars, with an enormous amount of data to store",
      ["It was carried out by a single laboratory over a period of 50 years",
       "It sequenced the genomes of all living organisms on earth",
       "It required the sequencing of only the protein-coding 2 per cent of the genome"], "A"),
    "Why the HGP was a mega project",
    "NCERT: the human genome is said to have approximately 3 × 10⁹ bp; if the cost of sequencing was US $3 per "
    "bp (the estimated cost in the beginning), the total cost would be approximately 9 billion US dollars. "
    "Further, if the sequence were stored in typed form in books, 3300 books of 1000 pages each would be needed. "
    "These huge numbers made it a mega project.",
    ["3 × 10⁹ bp × $3 = $9 billion", "Data equal to 3300 large books"],
    C12_MB("Human Genome Project"),
    why="The HGP was an international effort (1990–2003), was not about all organisms (though several model "
        "organisms were also sequenced), and sequenced the whole genome, coding and non-coding.",
    seconds=35)


def _replicate(mols, heavy):
    out = []
    for a, b in mols:
        new = "H" if heavy else "L"
        out += [(a, new), (b, new)]
    return out


_m = [("H", "H")]
for _gen_heavy in (False, False, True):
    _m = _replicate(_m, _gen_heavy)
_kinds = Counter("heavy" if m == ("H", "H") else ("light" if m == ("L", "L") else "hybrid") for m in _m)
assert len(_m) == 8 and _kinds == Counter({"hybrid": 6, "heavy": 2})

add(MBI, "Replication", "Advanced", "numerical",
    "E. coli grown for many generations in ¹⁵NH₄Cl medium is transferred to ¹⁴NH₄Cl medium for two generations "
    "and then returned to ¹⁵NH₄Cl medium for one more generation. Replication is semiconservative. What fractions "
    "of the DNA molecules are now heavy (¹⁵N/¹⁵N), hybrid (¹⁵N/¹⁴N) and light (¹⁴N/¹⁴N)?",
    P("1/4 heavy, 3/4 hybrid, none light",
      ["1/2 heavy, 1/2 hybrid, none light", "None heavy, 1/4 hybrid, 3/4 light", "1/4 heavy, 1/2 hybrid, 1/4 light"],
      "B"),
    "Tracking strands through semiconservative replication",
    "Start: one H/H molecule. Generation 1 in ¹⁴N: 2 H/L. Generation 2 in ¹⁴N: each H/L gives one H/L and one L/L "
    "→ 2 H/L + 2 L/L. Generation 3 in ¹⁵N: every old strand pairs with a new heavy strand; H/L gives H/H + L/H, "
    "and L/L gives L/H + L/H. Total 8 molecules: 2 H/H (heavy) and 6 hybrid, none light → 1/4 heavy, 3/4 hybrid.",
    ["After 2 generations in ¹⁴N: 2 hybrid, 2 light", "In ¹⁵N every new strand is heavy",
     "Hybrid → heavy + hybrid; light → 2 hybrid", "8 molecules: 2 heavy, 6 hybrid"],
    C12_MB("replication: the experimental proof"),
    why="1/2 heavy, 1/2 hybrid is the result of only one generation in ¹⁴N before the return to ¹⁵N; the "
        "'3/4 light' answer ignores the last generation in ¹⁵N; a light class cannot remain because every "
        "molecule made in ¹⁵N carries a new heavy strand.",
    seconds=90, verified_by=RECOMPUTED)

add(MBI, "Genetic code and translation", "Advanced", "assertion_reason",
    ar("A single base substitution within the coding region of a gene always changes the amino acid sequence of "
       "the polypeptide.",
       "Some amino acids are coded by more than one codon."),
    AR("D"),
    "Degeneracy and silent substitutions",
    "NCERT: the code is degenerate, since some amino acids are coded by more than one codon (R true); e.g. UUU and "
    "UUC both code for phenylalanine. A substitution that turns one such codon into another codon for the same "
    "amino acid leaves the polypeptide unchanged, so a base substitution does not always change the sequence "
    "(A false). (A substitution can change an amino acid, as GAG → GUG in sickle-cell anaemia, but not always.)",
    ["R: degenerate code, true", "UUU → UUC: still phenylalanine", "A: 'always' is false"],
    C12_MB("genetic code; mutations and genetic code"),
    seconds=40)

_sample = {"A": 20, "U": 30, "G": 25, "C": 25}
assert sum(_sample.values()) == 100 and _sample["A"] != _sample["U"] and _sample["A"] + _sample["G"] != 50

add(MBI, "DNA and RNA structure", "Advanced", "multi_statement",
    ms("A nucleic acid sample has the base composition: adenine 20%, uracil 30%, guanine 25% and cytosine 25%. "
       "Which inferences are correct?",
       ["The sample is RNA.",
        "It cannot be a double-stranded molecule in which all bases are paired complementarily.",
        "Its sugar is 2'-deoxyribose.",
        "Chargaff's rule A = T applies to it.",
        "Its purines equal its pyrimidines in amount."]),
    MS(["a", "b"], [["a", "b", "e"], ["c", "d"], ["a", "d"]], "C"),
    "Reading a base composition",
    "Uracil is found in RNA at the place of thymine, so the sample is RNA (a), with ribose rather than "
    "2'-deoxyribose (c false). If every base were paired complementarily, A would equal U and G would equal C; "
    "here A (20%) ≠ U (30%), so the molecule is not fully double-stranded (b). There is no thymine, so A = T "
    "cannot apply (d false). Purines A + G = 45% while pyrimidines U + C = 55% (e false).",
    ["Uracil → RNA, ribose", "A ≠ U → not fully paired", "Purines 45% ≠ pyrimidines 55%"],
    C12_MB("structure of polynucleotide chain"),
    why="(c), (d) and (e) are false: the sugar is ribose, the sample has no thymine, and purines (45%) do not equal "
        "pyrimidines (55%).",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "DNA as genetic material", "Advanced", "direct",
    "According to NCERT's comparison of DNA and RNA as genetic material, which statement is correct?",
    P("DNA, being more stable, is preferred for the storage of genetic information, whereas RNA, which can "
      "directly code for the synthesis of proteins, is better for the transmission (expression) of genetic "
      "information",
      ["RNA, being more stable, is preferred for storage, whereas DNA is better for the transmission of genetic "
       "information",
       "DNA can directly code for the synthesis of proteins, whereas RNA depends on DNA to express characters",
       "DNA and RNA are equally stable and equally suited to both storage and transmission"], "D"),
    "Storage versus transmission of genetic information",
    "NCERT: both DNA and RNA can mutate, but RNA, being unstable, mutates at a faster rate. RNA can directly code "
    "for the synthesis of proteins and hence can easily express the characters; DNA depends on RNA for protein "
    "synthesis. DNA, being more stable, is preferred for the storage of genetic information; for the "
    "transmission of genetic information, RNA is better.",
    ["DNA: stable → storage", "RNA: codes directly for proteins → transmission/expression"],
    C12_MB("the search for genetic material: properties of genetic material (DNA versus RNA)"),
    why="The first and second distractors swap the roles of DNA and RNA; NCERT states that DNA is more stable "
        "than RNA, so they are not equally stable or equally suited.",
    seconds=45)

add(MBI, "DNA packaging", "Advanced", "direct",
    "By a chromosomal rearrangement, an actively expressed gene comes to lie in a region of chromatin that is "
    "densely packed and stains dark. On the basis of NCERT's account of chromatin, the most likely result is that "
    "the gene:",
    P("Becomes transcriptionally inactive, as such chromatin (heterochromatin) is inactive",
      ["Becomes more actively transcribed, as dark-staining chromatin is euchromatin",
       "Is lost from the cell, since heterochromatin is not replicated",
       "Is transcribed only by RNA polymerase III, which acts on heterochromatin"], "A"),
    "Euchromatin and heterochromatin",
    "NCERT: in a typical nucleus, some regions of chromatin are loosely packed and stain light (euchromatin), and "
    "others are densely packed and stain dark (heterochromatin). Euchromatin is said to be transcriptionally "
    "active, and heterochromatin inactive. A gene moved into heterochromatin is therefore expected to be "
    "inactive.",
    ["Dense, dark → heterochromatin", "Heterochromatin: transcriptionally inactive"],
    C12_MB("packaging of DNA helix"),
    why="Euchromatin is the loosely packed, light-staining, active form; NCERT does not say heterochromatin is "
        "lost or left unreplicated, and RNA polymerase III makes tRNA, 5S rRNA and snRNAs, not genes in "
        "heterochromatin.",
    seconds=40)

_coding = "ATGCATTGA"
_mrna = _coding.replace("T", "U")
_template_53 = "".join(_COMP[b] for b in reversed(_coding))
_codon2 = _mrna[3:6]
_anti_53 = "".join({"A": "U", "U": "A", "G": "C", "C": "G"}[b] for b in reversed(_codon2))
assert (_mrna, _template_53, _anti_53, _mrna[6:9]) == ("AUGCAUUGA", "TCAATGCAT", "AUG", "UGA")

add(MBI, "Transcription", "Advanced", "match_list",
    ml(("item for a gene whose coding strand reads 5'-ATGCATTGA-3'", "sequence"),
       ["The mRNA", "The template strand, written 5'→3'",
        "Anticodon of the tRNA for the second codon, written 5'→3'", "The last codon of the mRNA"],
       ["5'-AUGCAUUGA-3'", "5'-TCAATGCAT-3'", "5'-AUG-3'", "UGA"]),
    M(mc("I,II,III,IV"), [mc("II,I,III,IV"), mc("I,II,IV,III"), mc("I,III,II,IV")], "C"),
    "Coding strand, template strand, mRNA and anticodon",
    "NCERT: the mRNA has the same sequence as the coding strand, with uracil in place of thymine: 5'-AUGCAUUGA-3' "
    "(A-I). The template strand is complementary and antiparallel; written 5'→3' it is 5'-TCAATGCAT-3' (B-II). "
    "The second codon is CAU; its anticodon, complementary and antiparallel, is 5'-AUG-3' (C-III). The last codon "
    "UGA is a stop codon (D-IV).",
    ["mRNA = coding strand with U", "Template = reverse complement", "Codon 2 = CAU → anticodon 5'-AUG-3'",
     "Codon 3 = UGA (stop)"],
    C12_MB("transcription; genetic code; tRNA"),
    why="The wrong codes take the template for the mRNA, or confuse the anticodon of codon 2 with the stop codon, "
        "or write the template strand as the anticodon.",
    seconds=80, verified_by=RECOMPUTED)

add(MBI, "Replication", "Advanced", "assertion_reason",
    ar("In eukaryotes, a failure of cell division after DNA replication results in polyploidy.",
       "Deoxyribonucleoside triphosphates serve both as substrates and as a source of energy for DNA "
       "polymerisation."),
    AR("B"),
    "Coordination of replication and division",
    "NCERT: in eukaryotes, DNA replication takes place in the S-phase, and replication and cell division must be "
    "highly coordinated; a failure in cell division after DNA replication results in polyploidy (A true). R is "
    "also a true NCERT line, about the dual role of dNTPs, but it concerns the chemistry of polymerisation, not "
    "the consequence of failed division. R does not explain A.",
    ["A: replicated DNA without division → polyploidy", "R: dNTPs as substrate and energy, unrelated"],
    C12_MB("replication: the machinery and the enzymes"),
    seconds=35)

# ================================================================ Microbes in Human Welfare (2 / 3 / 2)
C12_MW = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "direct",
    "NCERT lists diseases, with their common Indian names, that antibiotics have greatly improved our capacity "
    "to treat. The disease called 'gal ghotu' is:",
    P("Diphtheria", ["Whooping cough", "Leprosy", "Plague"], "C"),
    "Diseases treated with antibiotics",
    "NCERT: antibiotics have greatly improved our capacity to treat deadly diseases such as plague, whooping "
    "cough (kali khansi), diphtheria (gal ghotu) and leprosy (kusht rog), which used to kill millions all over "
    "the globe.",
    ["Kali khansi: whooping cough", "Gal ghotu: diphtheria", "Kusht rog: leprosy"],
    C12_MW("microbes in industrial products: antibiotics"),
    why="Whooping cough is 'kali khansi' and leprosy is 'kusht rog'; NCERT gives no such local name for plague.",
    seconds=20)

add(MHW, "Biogas", "Basic", "direct",
    "According to NCERT, biogas plants are more often built in:",
    P("Rural areas, where cattle dung is available in large quantities",
      ["Large cities, near industrial areas", "Deserts, where there is plenty of sunlight",
       "Coastal areas, where sea water is available"], "A"),
    "Where biogas plants are built",
    "NCERT: the excreta (dung) of cattle, commonly called gobar, is rich in methanogenic bacteria and is used to "
    "generate biogas (gobar gas). Biogas plants are more often built in rural areas, where cattle dung is "
    "available in large quantities. The gas is used for cooking and lighting.",
    ["Raw material: cattle dung (gobar)", "Abundant in rural areas → plants built there"],
    C12_MW("microbes in production of biogas"),
    why="The plant needs a regular supply of cattle dung, which is available in rural areas; sunlight or sea "
        "water plays no part in biogas production.",
    seconds=20)

add(MHW, "Household and industrial products", "Intermediate", "assertion_reason",
    ar("'Toddy', a traditional drink of some parts of southern India, is made by fermenting sap from palms.",
       "Lactic acid bacteria improve the nutritional quality of curd by increasing its vitamin B₁₂ content."),
    AR("B"),
    "Microbes in household products",
    "NCERT: toddy is made by fermenting sap from palms (A true). It also says that lactic acid bacteria increase "
    "vitamin B₁₂ in curd (R true). R concerns a different product and a different microbe, so it does not "
    "explain how toddy is made.",
    ["A: true (fermented palm sap)", "R: true, about curd", "Different products → R does not explain A"],
    C12_MW("microbes in household products"),
    seconds=30)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "direct",
    "A farmer wants to protect a cabbage crop (a brassica) from butterfly caterpillars without harming the other "
    "insects in the field. Which measure described in NCERT suits this aim?",
    P("Spraying a suspension of Bacillus thuringiensis spores on the plants",
      ["Releasing dragonflies into the field", "Inoculating the soil with Glomus",
       "Spraying a broad-spectrum chemical insecticide"], "B"),
    "Bt as a selective biocontrol agent",
    "NCERT: Bacillus thuringiensis (Bt) is available as dried spores, mixed with water and sprayed onto "
    "vulnerable plants such as brassicas and fruit trees, where they are eaten by insect larvae. In the gut the "
    "toxin is released and the larvae are killed. The bacterial disease kills the caterpillars but leaves other "
    "insects unharmed.",
    ["Bt spores on brassicas", "Toxin kills caterpillars", "Other insects unharmed"],
    C12_MW("microbes as biocontrol agents"),
    why="Dragonflies control mosquitoes; Glomus is a mycorrhizal fungus that helps absorb phosphorus; and "
        "broad-spectrum chemicals kill useful insects as well.",
    seconds=35)

add(MHW, "Sewage treatment", "Intermediate", "multi_statement",
    ms("Compare the aeration tanks with the anaerobic sludge digesters of a sewage treatment plant. Which "
       "statements are correct?",
       ["Aerobic microbes grow in the aeration tanks, whereas bacteria that grow anaerobically act in the "
        "digesters.",
        "The growth of flocs in the aeration tanks reduces the BOD of the effluent.",
        "The digestion in the digesters produces gases such as methane, hydrogen sulphide and carbon dioxide, "
        "which form biogas.",
        "Both are part of the primary treatment of sewage.",
        "The digesters receive the effluent, while the aeration tanks receive the activated sludge."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "D"),
    "Aeration tanks and sludge digesters",
    "NCERT: in secondary (biological) treatment, the primary effluent is passed into aeration tanks, where "
    "vigorous growth of useful aerobic microbes into flocs consumes organic matter and reduces the BOD (a, b). "
    "The major part of the activated sludge from the settling tank is pumped into anaerobic sludge digesters, "
    "where bacteria growing anaerobically digest the bacteria and fungi in the sludge, producing methane, "
    "hydrogen sulphide and CO₂ (biogas) (a, c). Both steps belong to secondary treatment (d false), and it is the "
    "effluent that goes to the aeration tank and the sludge to the digester (e false).",
    ["Aeration tank: effluent, aerobic flocs, BOD down", "Digester: sludge, anaerobic bacteria, biogas",
     "Both: secondary treatment"],
    C12_MW("microbes in sewage treatment"),
    why="Options with (d) or (e) put the steps in primary treatment or reverse what each unit receives; '(b), (c) "
        "and (e)' also omits (a).",
    seconds=50)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "multi_statement",
    ms("A village wants to set up a biogas plant on cattle dung and to farm organically. Which of the following "
       "NCERT statements support this plan?",
       ["The spent slurry removed from a biogas plant can be used as fertiliser.",
        "Cattle dung is rich in methanogenic bacteria.",
        "The biogas produced can be used for cooking and lighting.",
        "Bt spores can control caterpillars on brassicas without harming other insects.",
        "Biogas consists predominantly of carbon dioxide and so cannot be burnt."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["b", "c", "d", "e"], ["a", "c", "d"]], "C"),
    "Biogas and biocontrol in a village",
    "NCERT: cattle dung (gobar) is rich in methanogenic bacteria (b) and is fed as a slurry into the biogas plant; "
    "the spent slurry is removed through another outlet and may be used as fertiliser (a); the biogas is supplied "
    "to nearby houses for cooking and lighting (c). Bt spores kill caterpillars but leave other insects unharmed, "
    "suiting an organic farm (d). Biogas is predominantly methane and is inflammable (e false).",
    ["Dung → methanogens → biogas", "Slurry → fertiliser", "Biogas: cooking, lighting", "Bt: selective control"],
    C12_MW("microbes in production of biogas; microbes as biocontrol agents"),
    why="Options with (e) are wrong because biogas is mainly methane and burns; '(a), (c) and (d)' leaves out (b).",
    seconds=50)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "statement_pair",
    sp("Rhizobium and Anabaena both fix atmospheric nitrogen, but only Rhizobium does so in symbiotic association "
       "with the root nodules of leguminous plants.",
       "Glomus and Trichoderma are both fungi, but only Glomus is described by NCERT as forming mycorrhiza that "
       "helps the plant absorb phosphorus."),
    SP("A"),
    "Comparing biofertilisers and biocontrol fungi",
    "NCERT: Rhizobium fixes nitrogen in the root nodules of leguminous plants, while cyanobacteria such as "
    "Anabaena, Nostoc and Oscillatoria fix nitrogen as autotrophic microbes in aquatic and terrestrial "
    "environments, e.g. in paddy fields (Statement I true). Many members of the genus Glomus form mycorrhiza and "
    "absorb phosphorus from the soil for the plant; Trichoderma species are free-living fungi in root ecosystems, "
    "used as biocontrol agents against plant pathogens (Statement II true).",
    ["Rhizobium: nodules; Anabaena: free, paddy fields", "Glomus: mycorrhiza, phosphorus; Trichoderma: "
     "biocontrol"],
    C12_MW("microbes as biofertilisers; microbes as biocontrol agents"),
    seconds=45)

# ================================================================ Organisms and Populations (4 / 5 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population interactions", "Basic", "direct",
    "According to NCERT, it is not surprising that parasitism has evolved in so many taxonomic groups, from "
    "plants to higher vertebrates, because the parasitic mode of life:",
    P("Ensures free lodging and meals",
      ["Always benefits both the parasite and the host", "Requires no adaptation by the parasite",
       "Allows the parasite to avoid having any host"], "B"),
    "Why parasitism is widespread",
    "NCERT: considering that the parasitic mode of life ensures free lodging and meals, it is not surprising "
    "that parasitism has evolved in so many taxonomic groups from plants to higher vertebrates. Parasites have in "
    "turn evolved special adaptations, such as loss of unnecessary sense organs, adhesive organs or suckers, loss "
    "of the digestive system and high reproductive capacity.",
    ["Parasite gets shelter (lodging) and food (meals) from the host", "Hence parasitism is widespread"],
    C12_OP("population interactions: parasitism"),
    why="In parasitism the host is harmed, not benefited; parasites show many special adaptations; and a "
        "parasite by definition depends on a host.",
    seconds=20)

add(OAP, "Population interactions", "Basic", "direct",
    "NCERT gives two most familiar examples of ectoparasites. They are:",
    P("Lice on humans and ticks on dogs",
      ["Liver fluke in humans and the malarial parasite", "Cuscuta on hedge plants and the koel in a crow's nest",
       "Copepods on marine fish and tapeworms in humans"], "D"),
    "Ectoparasites",
    "NCERT: parasites that feed on the external surface of the host organism are called ectoparasites; the most "
    "familiar examples are the lice on humans and ticks on dogs. Many marine fish are also infested with "
    "ectoparasitic copepods. Endoparasites, such as the liver fluke and the malarial parasite, live inside the "
    "host body.",
    ["Ectoparasite: feeds on the external surface", "Examples: lice on humans, ticks on dogs"],
    C12_OP("population interactions: parasitism"),
    why="The liver fluke and malarial parasite are endoparasites; the koel is a brood parasite; the tapeworm "
        "lives inside the host, so the pair with copepods is mixed.",
    seconds=20)

add(OAP, "Population attributes", "Basic", "statement_pair",
    sp("Birth rates and death rates of a population are expressed as per capita births and deaths respectively.",
       "An age pyramid with a broad base of pre-reproductive individuals shows a declining population."),
    SP("C"),
    "Population attributes",
    "NCERT: a population has birth rates and death rates, which refer to per capita births and deaths "
    "respectively, expressed as change in numbers with respect to members of the population (Statement I true). "
    "The shape of the age pyramid reflects the growth status: a broad base (many pre-reproductive individuals) "
    "shows an expanding population, a bell shape a stable one and an urn shape (narrow base) a declining one "
    "(Statement II false).",
    ["Rates: per capita", "Broad base → expanding; urn → declining"],
    C12_OP("populations: population attributes"),
    seconds=25)

add(OAP, "Population attributes", "Basic", "multi_statement",
    ms("Which of the following are attributes that a population has but an individual organism does not?",
       ["Birth rate", "Death rate", "Sex ratio", "Age distribution", "Body size"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["b", "c", "d", "e"], ["a", "c", "d"]], "A"),
    "Population versus individual attributes",
    "NCERT: a population has certain attributes that an individual organism does not. An individual may have "
    "births and deaths, but a population has birth rates and death rates; a population also has a sex ratio and "
    "an age distribution. Body size belongs to each individual organism.",
    ["Population: birth rate, death rate, sex ratio, age distribution", "Individual: body size"],
    C12_OP("populations: population attributes"),
    why="Options with (e) include body size, an attribute of individuals; '(a), (c) and (d)' leaves out the "
        "death rate.",
    seconds=30)

_K = 800
_N = _K * (1 - F(1, 4))
assert _N == 600 and F(_K - 600, _K) == F(1, 4)

add(OAP, "Population growth", "Intermediate", "numerical",
    "A population grows according to the logistic model, dN/dt = rN[(K − N)/K], in a habitat with carrying "
    "capacity K = 800. At what population size will its per capita growth rate, (1/N)(dN/dt), be one-fourth of r?",
    P("600", ["200", "400", "800"], "C"),
    "Per capita growth rate in logistic growth",
    "Per capita growth rate = (1/N)(dN/dt) = r(K − N)/K. Setting this equal to r/4: (K − N)/K = 1/4, so "
    "K − N = 200 and N = 800 − 200 = 600.",
    ["(1/N)(dN/dt) = r(K − N)/K", "(K − N)/K = 1/4 → K − N = 200", "N = 600"],
    C12_OP("population growth: growth models (logistic growth)"),
    why="200 solves N/K = 1/4 instead of (K − N)/K = 1/4; 400 (= K/2) is where dN/dt, not the per capita rate, is "
        "highest; at 800 (= K) the per capita rate is zero.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("In which of the following does NCERT describe co-evolution (or the need for it) between the interacting "
       "species?",
       ["Many parasites and their hosts, since parasites tend to be host-specific",
        "The fig and its partner wasp species",
        "The Mediterranean orchid Ophrys and the bee that pollinates it",
        "The introduced goats and the Abingdon tortoise of the Galapagos Islands",
        "Cattle egrets and grazing cattle"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Co-evolution in interactions",
    "NCERT: many parasites have evolved to be host-specific (they can parasitise only a single species of host) "
    "in such a way that both host and parasite tend to co-evolve (a). Plant-animal interactions often involve "
    "co-evolution of the mutualists, as with the fig and its pollinating wasp (b). In Ophrys, if the female bee's "
    "colour patterns change even slightly during evolution, pollination success will be reduced unless the "
    "orchid flower co-evolves (c). The goats and the tortoise illustrate competition, and cattle egrets and "
    "cattle illustrate commensalism; NCERT does not describe co-evolution for them.",
    ["Host-specific parasites", "Fig–wasp mutualism", "Ophrys–bee"],
    C12_OP("population interactions: parasitism; mutualism"),
    why="Options with (d) or (e) include interactions for which NCERT speaks of competition or commensalism, not "
        "co-evolution.",
    seconds=50)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("Lichens represent an intimate mutualistic relationship between a fungus and photosynthesising algae or "
       "cyanobacteria.",
       "Mycorrhizae are associations between fungi and the roots of higher plants."),
    AR("B"),
    "Two mutualistic associations of fungi",
    "NCERT: lichens represent an intimate mutualistic relationship between a fungus and photosynthesising algae "
    "or cyanobacteria (A true). Mycorrhizae are associations between fungi and the roots of higher plants (R "
    "true). R describes a different association, involving plant roots, and says nothing about the partners in "
    "a lichen, so it does not explain A.",
    ["A: lichen = fungus + alga/cyanobacterium", "R: mycorrhiza = fungus + plant root", "Separate examples"],
    C12_OP("population interactions: mutualism"),
    seconds=30)

add(OAP, "Population growth", "Intermediate", "statement_pair",
    sp("Both the exponential and the logistic models of population growth contain the intrinsic rate of natural "
       "increase, r.",
       "The integral form Nₜ = N₀e^(rt) describes logistic growth."),
    SP("C"),
    "Exponential and logistic equations",
    "NCERT: exponential growth is dN/dt = rN, whose integral form is Nₜ = N₀e^(rt); logistic growth is "
    "dN/dt = rN[(K − N)/K]. Both contain r (Statement I true). The integral form Nₜ = N₀e^(rt) is that of "
    "exponential growth; it has no carrying capacity K, so it cannot describe logistic growth (Statement II false).",
    ["Exponential: dN/dt = rN; Nₜ = N₀e^(rt)", "Logistic: dN/dt = rN(K − N)/K"],
    C12_OP("population growth: growth models"),
    seconds=30)

add(OAP, "Population growth", "Intermediate", "match_list",
    ml(("phase of logistic (sigmoid) growth", "description"),
       ["Lag phase", "Phase of acceleration", "Phase of deceleration", "Asymptote"],
       ["The population density reaches the carrying capacity",
        "Initial phase of slow growth",
        "Growth slows as the limited resources begin to restrict the population",
        "Population numbers increase rapidly"]),
    M(mc("II,IV,III,I"), [mc("IV,II,III,I"), mc("II,IV,I,III"), mc("II,III,IV,I")], "A"),
    "Phases of logistic growth",
    "NCERT: a population growing in a habitat with limited resources shows initially a lag phase (A-II), followed "
    "by phases of acceleration (B-IV) and deceleration (C-III), and finally an asymptote, when the population "
    "density reaches the carrying capacity (D-I). Plotting N against time gives a sigmoid curve.",
    ["Lag → acceleration → deceleration → asymptote (K)"],
    C12_OP("population growth: growth models (logistic growth)"),
    why="The wrong codes swap the lag and acceleration phases, the deceleration phase and the asymptote, or "
        "acceleration and deceleration.",
    seconds=40)

_n0 = 1000
_p = _n0 * math.exp(0.03 * 46.2)
_q = _n0 * math.exp(0.015 * 46.2)
assert math.isclose(0.03 * 46.2, 2 * 0.693) and math.isclose(0.015 * 46.2, 0.693)   # ln 2 = 0.693 as given
assert abs(_p - 4000) < 2 and abs(_q - 2000) < 1

add(OAP, "Population growth", "Advanced", "numerical",
    "Two populations, P and Q, each start with 1000 individuals and grow exponentially (Nₜ = N₀e^(rt)), P with "
    "r = 0.03 per year and Q with r = 0.015 per year. Taking ln 2 = 0.693, what will be their sizes after "
    "46.2 years?",
    P("P: 4000; Q: 2000", ["P: 2000; Q: 1000", "P: 2386; Q: 1693", "P: 4000; Q: 1000"], "D"),
    "Exponential growth with different r",
    "rt for P = 0.03 × 46.2 = 1.386 = 2 × 0.693 = 2 ln 2, so e^(rt) = 2² = 4 and P = 4000. For Q, rt = 0.015 × "
    "46.2 = 0.693 = ln 2, so e^(rt) = 2 and Q = 2000. Halving r halves the number of doublings in the same time.",
    ["P: rt = 1.386 = 2 ln 2 → ×4", "Q: rt = 0.693 = ln 2 → ×2", "P = 4000, Q = 2000"],
    C12_OP("population growth: growth models (exponential growth)"),
    why="'2000 and 1000' leaves Q unchanged and doubles P only once; '2386 and 1693' adds 1000 × rt as if growth "
        "were linear; '4000 and 1000' ignores Q's growth.",
    seconds=75, verified_by=RECOMPUTED)

_n, _b, _d, _i, _e = 500, 60, 40, 10, 30
assert _n + (_b + _i) - (_d + _e) == 500 and F(_b, _n) == F(3, 25) and _b - _d == 20

add(OAP, "Population attributes", "Advanced", "multi_statement",
    ms("A population of 500 individuals shows, during one year, 60 births, 40 deaths, 10 immigrants and 30 "
       "emigrants. Using N(t+1) = N(t) + [(B + I) − (D + E)], which statements are correct?",
       ["The population size at the end of the year is again 500.",
        "The per capita birth rate is 0.12 per individual per year.",
        "Without any migration, the population would have increased by 20.",
        "Immigration exceeded emigration during the year.",
        "The per capita death rate is 0.4 per individual per year."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Natality, mortality and migration",
    "N(t+1) = 500 + (60 + 10) − (40 + 30) = 500 (a). Per capita birth rate = 60/500 = 0.12 (b). Natural increase "
    "= births − deaths = 60 − 40 = 20 (c). Emigrants (30) exceeded immigrants (10), and this net loss of 20 "
    "cancelled the natural increase (d false). Per capita death rate = 40/500 = 0.08, not 0.4 (e false).",
    ["N(t+1) = 500 + 70 − 70 = 500", "b = 0.12; d = 0.08", "Natural increase 20 = net emigration 20"],
    C12_OP("populations: population density; population growth"),
    why="Options with (d) or (e) contain a false statement: emigration exceeded immigration, and the death rate is "
        "0.08; '(b), (c) and (e)' also omits (a).",
    seconds=75, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "statement_pair",
    sp("Both the monarch butterfly and Calotropis protect themselves with chemicals: the butterfly acquires a "
       "chemical from a poisonous weed eaten by its caterpillar, while Calotropis produces poisonous cardiac "
       "glycosides.",
       "Both the cryptic colouration of some insects and frogs and the thorns of Acacia and cactus are chemical "
       "means of defence."),
    SP("C"),
    "Morphological, chemical and cryptic defences",
    "NCERT: the monarch butterfly is highly distasteful to its predator (bird) because of a special chemical "
    "present in its body, acquired during its caterpillar stage by feeding on a poisonous weed; Calotropis "
    "produces highly poisonous cardiac glycosides, which is why cattle and goats do not browse it (Statement I "
    "true). Cryptic colouration (camouflage) helps prey avoid being detected, and thorns are the most common "
    "morphological means of defence; neither is chemical (Statement II false).",
    ["Monarch: acquired chemical; Calotropis: cardiac glycosides", "Camouflage: cryptic; thorns: morphological"],
    C12_OP("population interactions: predation"),
    seconds=50)

_Kx = F(1)
_rate = lambda n: n * (_Kx - n) / _Kx
assert _rate(F(1, 4)) == _rate(F(3, 4)) != _rate(F(1, 2))

add(OAP, "Population growth", "Advanced", "direct",
    "For a population growing according to dN/dt = rN[(K − N)/K], at which pair of population sizes is the "
    "growth rate dN/dt the SAME?",
    P("N = K/4 and N = 3K/4", ["N = K/4 and N = K/2", "N = K/2 and N = 3K/4", "N = K/2 and N = K"], "A"),
    "Symmetry of the logistic growth rate",
    "dN/dt = (r/K) × N(K − N). At N = K/4: (r/K)(K/4)(3K/4) = 3rK/16. At N = 3K/4: (r/K)(3K/4)(K/4) = 3rK/16, "
    "the same. The product N(K − N) is symmetrical about K/2, where it is largest (rK/4); at N = K it is zero.",
    ["dN/dt ∝ N(K − N)", "K/4 and 3K/4 give the same product", "Maximum at K/2; zero at K"],
    C12_OP("population growth: growth models (logistic growth)"),
    why="At K/2 the rate is the maximum (rK/4), which no other listed size matches; at K it is zero.",
    seconds=60, verified_by=RECOMPUTED)

# ================================================================ Ecosystem (3 / 4 / 3)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "During decomposition, humus is further degraded by some microbes, and inorganic nutrients are released. "
    "This process is called:",
    P("Mineralisation", ["Humification", "Fragmentation", "Leaching"], "B"),
    "Steps of decomposition",
    "NCERT: humification leads to the accumulation of humus, which is highly resistant to microbial action. Humus "
    "is further degraded by some microbes, and the release of inorganic nutrients occurs by the process known as "
    "mineralisation.",
    ["Humification → humus", "Humus degraded by microbes → nutrients released = mineralisation"],
    C12_EC("decomposition"),
    why="Humification forms humus rather than breaking it down; fragmentation is the breaking of detritus into "
        "small particles by detritivores; leaching carries water-soluble nutrients down the soil.",
    seconds=20)

add(ECO, "Ecological pyramids", "Basic", "assertion_reason",
    ar("The pyramid of biomass in a sea is generally inverted.",
       "Decomposition is largely an oxygen-requiring process."),
    AR("B"),
    "Inverted biomass pyramid",
    "NCERT: the pyramid of biomass in the sea is generally inverted because the biomass of fishes far exceeds "
    "that of phytoplankton (A true). NCERT also states that decomposition is largely an oxygen-requiring process "
    "(R true). R concerns the breakdown of detritus and has nothing to do with the relative biomass of producers "
    "and consumers in the sea, so it does not explain A.",
    ["A: true (fish biomass > phytoplankton biomass)", "R: true, about decomposition", "R unrelated"],
    C12_EC("ecological pyramids; decomposition"),
    seconds=25)

add(ECO, "Energy flow", "Basic", "statement_pair",
    sp("The flow of energy in an ecosystem is unidirectional, from the sun to producers and then to consumers.",
       "Some organisms of the detritus food chain are prey to the animals of the grazing food chain."),
    SP("A"),
    "Energy flow and linked food chains",
    "NCERT: there is a unidirectional flow of energy from the sun to producers and then to consumers (Statement I "
    "true). The detritus food chain may be connected with the grazing food chain at some levels: some organisms "
    "of the DFC are prey to the GFC animals, and in a natural ecosystem some animals, like cockroaches and "
    "crows, are omnivores (Statement II true).",
    ["Energy: one direction", "DFC and GFC are linked (DFC organisms eaten by GFC animals)"],
    C12_EC("energy flow"),
    seconds=25)

add(ECO, "Productivity and decomposition", "Intermediate", "assertion_reason",
    ar("Leaching during decomposition can make some nutrients unavailable to plants.",
       "In leaching, water-soluble inorganic nutrients go down into the soil horizon and get precipitated as "
       "unavailable salts."),
    AR("A"),
    "Leaching",
    "NCERT: by the process of leaching, water-soluble inorganic nutrients go down into the soil horizon and get "
    "precipitated as unavailable salts. Since the precipitated salts are unavailable, plants cannot use those "
    "nutrients: R directly explains A.",
    ["Soluble nutrients move down", "Precipitate as unavailable salts", "So plants lose access to them"],
    C12_EC("decomposition"),
    seconds=30)

add(ECO, "Structure and components", "Intermediate", "direct",
    "NCERT divides ecosystems into natural and man-made ones. Which pair are BOTH examples of man-made "
    "ecosystems given in NCERT?",
    P("Crop fields and an aquarium", ["A pond and a lake", "A grassland and a desert", "An estuary and a wetland"],
      "A"),
    "Man-made ecosystems",
    "NCERT: ecosystems are grouped into terrestrial (forest, grassland, desert) and aquatic (pond, lake, wetland, "
    "river, estuary) ones; crop fields and an aquarium may also be considered man-made ecosystems.",
    ["Natural: forest, grassland, desert, pond, lake, wetland, river, estuary", "Man-made: crop fields, "
     "aquarium"],
    C12_EC("ecosystem: structure and function"),
    why="Ponds, lakes, grasslands, deserts, estuaries and wetlands are NCERT's examples of natural ecosystems.",
    seconds=20)

add(ECO, "Energy flow", "Intermediate", "match_list",
    ml(("group in an ecosystem", "other name used in NCERT"),
       ["Producers", "Decomposers", "Primary consumers", "Secondary consumers"],
       ["Primary carnivores", "Herbivores", "Saprotrophs", "Autotrophs"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("IV,II,III,I")], "C"),
    "Names of trophic groups",
    "NCERT: producers, such as green plants, are autotrophs (A-IV). Decomposers secrete digestive enzymes and "
    "absorb the simple inorganic products, so they are also known as saprotrophs (B-III). Consumers that feed on "
    "producers are herbivores, the primary consumers (C-II); those that eat the herbivores are carnivores, more "
    "correctly primary carnivores, which are secondary consumers (D-I).",
    ["Producers: autotrophs", "Decomposers: saprotrophs", "Primary consumers: herbivores",
     "Secondary consumers: primary carnivores"],
    C12_EC("energy flow; decomposition"),
    why="The wrong codes swap autotrophs with saprotrophs, herbivores with primary carnivores, or saprotrophs "
        "with herbivores.",
    seconds=35)

add(ECO, "Productivity and decomposition", "Intermediate", "multi_statement",
    ms("Which of the following statements about humus are correct, according to NCERT?",
       ["It is a dark-coloured, amorphous substance formed by humification.",
        "It is highly resistant to microbial action and decomposes at an extremely slow rate.",
        "Being colloidal in nature, it serves as a reservoir of nutrients.",
        "It is rapidly degraded by earthworms through catabolism.",
        "It is formed by the leaching of water-soluble nutrients into the soil."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "D"),
    "Humus",
    "NCERT: humification leads to the accumulation of a dark-coloured amorphous substance called humus (a), "
    "which is highly resistant to microbial action and undergoes decomposition at an extremely slow rate (b). "
    "Being colloidal in nature, it serves as a reservoir of nutrients (c). It is degraded slowly by some microbes "
    "(mineralisation), not rapidly by earthworms (d false), and leaching is a separate process that carries "
    "soluble nutrients down the soil (e false).",
    ["Humification → humus", "Resistant, slow to decompose", "Colloidal reservoir of nutrients"],
    C12_EC("decomposition"),
    why="Options with (d) or (e) are wrong: humus is degraded very slowly by microbes, and it is formed by "
        "humification, not leaching; '(b), (c) and (e)' also omits (a).",
    seconds=40)

_snake = 10
_from_frog, _from_rabbit = _snake * F(6, 10), _snake * F(4, 10)
_grass = _from_frog * 10 * 10 * 10 + _from_rabbit * 10 * 10
assert _grass == 6400

add(ECO, "Energy flow", "Advanced", "numerical",
    "In a food web, grasshoppers and rabbits eat grass, frogs eat grasshoppers, and snakes eat frogs and rabbits. "
    "A snake population obtains 10 kJ of energy: 60 per cent of it from frogs and 40 per cent from rabbits. "
    "Assuming that only 10 per cent of the energy passes from each trophic level to the next, how much energy "
    "must the grass have fixed to support this?",
    P("6400 kJ", ["10,000 kJ", "1000 kJ", "4600 kJ"], "A"),
    "Energy needs in a food web",
    "Via frogs (grass → grasshopper → frog → snake): 6 kJ to the snakes needs 60 kJ in frogs, 600 kJ in "
    "grasshoppers and 6000 kJ in grass. Via rabbits (grass → rabbit → snake): 4 kJ to the snakes needs 40 kJ in "
    "rabbits and 400 kJ in grass. Total grass energy = 6000 + 400 = 6400 kJ.",
    ["Frog path: 6 × 10³ = 6000 kJ", "Rabbit path: 4 × 10² = 400 kJ", "Total 6400 kJ"],
    C12_EC("energy flow; food chains and food web"),
    why="10,000 kJ treats all the snake's food as coming through three transfers; 1000 kJ treats it all as two "
        "transfers; 4600 kJ swaps the two percentages.",
    seconds=90, verified_by=RECOMPUTED)

add(ECO, "Ecological pyramids", "Advanced", "statement_pair",
    sp("Ecological pyramids do not take into account a species that belongs to two or more trophic levels at the "
       "same time.",
       "Although saprophytes play a vital role in the ecosystem, they are not given any place in ecological "
       "pyramids."),
    SP("A"),
    "Limitations of ecological pyramids",
    "NCERT lists limitations of ecological pyramids: they do not take into account the same species belonging to "
    "two or more trophic levels (Statement I true); they assume a simple food chain, which almost never exists in "
    "nature, and do not accommodate a food web; and saprophytes are not given any place in ecological pyramids "
    "even though they play a vital role in the ecosystem (Statement II true).",
    ["Species at two levels: not handled", "Simple food chain assumed", "Saprophytes: no place"],
    C12_EC("ecological pyramids"),
    seconds=40)

_gpp = 1000
_npp = _gpp * F(7, 10)
assert (_gpp - _npp, _npp, _npp / 10, _npp / 100) == (300, 700, 70, 7)

add(ECO, "Productivity and decomposition", "Advanced", "match_list",
    ml(("quantity for a grassland whose producers have a GPP of 1000 kJ m⁻² yr⁻¹ and use 30 per cent of it in "
        "respiration (10 per cent energy transfer between trophic levels)", "value (kJ m⁻² yr⁻¹)"),
       ["Respiration loss of the producers", "Net primary productivity",
        "Energy reaching the herbivores", "Energy reaching the primary carnivores"],
       ["7", "70", "300", "700"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("IV,III,I,II")], "B"),
    "From GPP to the carnivores",
    "Respiration loss = 30% of 1000 = 300 (A-III). NPP = GPP − respiration = 700 (B-IV); this is the biomass "
    "available to heterotrophs. With 10 per cent transfer, herbivores get 70 (C-II) and primary carnivores 7 "
    "(D-I).",
    ["R = 300", "NPP = 1000 − 300 = 700", "Herbivores 70; primary carnivores 7"],
    C12_EC("productivity; energy flow"),
    why="The wrong codes swap the respiration loss with NPP, or the herbivore and carnivore values, or apply the "
        "10 per cent to GPP instead of NPP.",
    seconds=70, verified_by=RECOMPUTED)

# ================================================================ Biodiversity and Conservation (3 / 4 / 3)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "According to NCERT, of all the species recorded on earth:",
    P("More than 70 per cent are animals, while plants (including algae, fungi, bryophytes, gymnosperms and "
      "angiosperms) make up no more than 22 per cent",
      ["More than 70 per cent are plants, while animals make up no more than 22 per cent",
       "Animals and plants each make up about half",
       "Fungi make up more than 70 per cent"], "D"),
    "Proportions of recorded species",
    "NCERT: of all the species recorded, more than 70 per cent are animals, while plants (including algae, fungi, "
    "bryophytes, gymnosperms and angiosperms) comprise no more than 22 per cent of the total. Among animals, "
    "insects are the most species-rich group, making up more than 70 per cent of the total.",
    ["Animals > 70%", "Plants (with algae, fungi, bryophytes, gymnosperms, angiosperms) ≤ 22%"],
    C12_BD("biodiversity: how many species are there on earth and how many in India?"),
    why="The second option reverses the proportions; the split is far from equal; and fungi are only part of the "
        "22 per cent that NCERT groups as plants.",
    seconds=25)

add(BDC, "Hotspots and Red Data Book", "Basic", "direct",
    "NCERT describes the identification of certain 'biodiversity hotspots' for maximum protection. This is part "
    "of which approach to conservation?",
    P("In situ conservation", ["Ex situ conservation", "Cryopreservation", "Bioprospecting"], "C"),
    "Hotspots and in situ conservation",
    "NCERT: in in situ (on site) conservation, endangered species are protected in their natural habitat so that "
    "the entire ecosystem is protected. Under this approach, certain 'biodiversity hotspots' have been "
    "identified as regions with very high levels of species richness and a high degree of endemism, for maximal "
    "protection.",
    ["In situ = protection in natural habitat", "Hotspots chosen for maximal protection → in situ"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity?"),
    why="Ex situ conservation and cryopreservation take species or gametes out of their habitat; bioprospecting "
        "is the search for economically important products, not a conservation approach.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Basic", "assertion_reason",
    ar("Insects are the most species-rich taxonomic group among animals, making up more than 70 per cent of the "
       "total.",
       "The term 'biodiversity' was popularised by the sociobiologist Edward Wilson."),
    AR("B"),
    "Insect species richness",
    "NCERT: among animals, insects are the most species-rich taxonomic group, making up more than 70 per cent of "
    "the total; out of every 10 animals on this planet, 7 are insects (A true). Edward Wilson popularised the "
    "term biodiversity (R true). Who popularised a term has nothing to do with why insects are so numerous, so R "
    "does not explain A.",
    ["A: true", "R: true, a historical fact about the term", "R unrelated to A"],
    C12_BD("biodiversity"),
    seconds=25)

add(BDC, "Importance and loss", "Intermediate", "statement_pair",
    sp("The extinction of more than 200 species of cichlid fish after the Nile perch was introduced into Lake "
       "Victoria, and the threat to indigenous catfishes from the illegal introduction of the African catfish "
       "Clarias gariepinus, are both examples of alien species invasions.",
       "The extinctions of Steller's sea cow and the passenger pigeon are both examples of co-extinction."),
    SP("C"),
    "Classifying causes of biodiversity loss",
    "NCERT gives the Nile perch in Lake Victoria and the illegal introduction of Clarias gariepinus for "
    "aquaculture as examples of alien species invasions (Statement I true). Steller's sea cow and the passenger "
    "pigeon became extinct in the last 500 years through over-exploitation by humans, not co-extinction, which "
    "refers to obligatorily associated species (such as a host fish's parasites) dying out along with another "
    "species (Statement II false).",
    ["Nile perch, Clarias: alien invasions", "Steller's sea cow, passenger pigeon: over-exploitation"],
    C12_BD("loss of biodiversity: causes of biodiversity losses"),
    seconds=40)

add(BDC, "Patterns of biodiversity", "Intermediate", "assertion_reason",
    ar("Temperate regions have a greater species diversity than the tropics because more solar energy is "
       "available in temperate regions.",
       "More solar energy is available in the tropics, which contributes to higher productivity and might, in "
       "turn, contribute indirectly to greater diversity."),
    AR("D"),
    "Latitudinal gradients",
    "NCERT: in general, species diversity decreases as we move away from the equator towards the poles, so the "
    "tropics, not the temperate regions, have greater diversity; and more solar energy is available in the "
    "tropics (A false on both counts). R is one of NCERT's hypotheses for the greater biological diversity of "
    "the tropics and is true.",
    ["Diversity: tropics > temperate", "Solar energy: more in tropics", "A false, R true"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    seconds=35)

add(BDC, "Importance and loss", "Intermediate", "match_list",
    ml(("cause of biodiversity loss", "description given in NCERT"),
       ["Habitat loss and fragmentation", "Over-exploitation", "Alien species invasions", "Co-extinctions"],
       ["When a species becomes extinct, the plant and animal species associated with it in an obligatory way "
        "also become extinct",
        "Introduced species turn invasive and cause the decline or extinction of indigenous species",
        "When 'need' turns to 'greed', natural resources are used beyond what they can sustain",
        "Mammals and birds requiring large territories, and animals with migratory habits, are badly affected"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,II,III,I"), mc("IV,III,I,II")], "A"),
    "The Evil Quartet",
    "NCERT: when large habitats are broken up into small fragments, mammals and birds requiring large "
    "territories and certain animals with migratory habits are badly affected (A-IV). Humans have always depended "
    "on nature, but when 'need' turns to 'greed' it leads to over-exploitation (B-III). When alien species are "
    "introduced, some turn invasive and cause decline or extinction of indigenous species (C-II). When a species "
    "becomes extinct, the species associated with it in an obligatory way also become extinct (D-I).",
    ["Fragmentation → large-territory and migratory animals", "Greed → over-exploitation",
     "Invasive aliens", "Obligate partners → co-extinction"],
    C12_BD("loss of biodiversity: causes of biodiversity losses"),
    why="The wrong codes swap habitat loss with over-exploitation, over-exploitation with alien invasions, or "
        "alien invasions with co-extinction.",
    seconds=45)

add(BDC, "In situ and ex situ conservation", "Intermediate", "statement_pair",
    sp("Wildlife safari parks and botanical gardens are both means of ex situ conservation.",
       "Biosphere reserves and sacred groves are both means of in situ conservation."),
    SP("A"),
    "Classifying conservation measures",
    "NCERT: in ex situ conservation, threatened species are taken out of their natural habitat and placed in "
    "special settings; zoological parks, botanical gardens and wildlife safari parks serve this purpose "
    "(Statement I true). In situ conservation protects species in their natural habitat; India has biosphere "
    "reserves, national parks and sanctuaries, and sacred groves (tracts of forest given total protection) are "
    "also in situ (Statement II true).",
    ["Ex situ: zoos, botanical gardens, safari parks", "In situ: biosphere reserves, national parks, "
     "sanctuaries, sacred groves"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity?"),
    seconds=30)

_ratio = 10 ** (0.2 * 5)
assert abs(_ratio - 10) < 1e-9

add(BDC, "Patterns of biodiversity", "Advanced", "multi_statement",
    ms("The species–area relationship is log S = log C + Z log A. Which of the following statements are correct?",
       ["For areas within a region, NCERT gives Z in the range 0.1 to 0.2.",
        "With Z = 0.2, an area 10⁵ times larger is expected to have 10 times as many species.",
        "For very large areas such as entire continents, Z lies in the range 0.6 to 1.2.",
        "Plotted on ordinary (linear) axes, species richness against area gives a straight line.",
        "In this equation, C is the slope of the line (regression coefficient)."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Using the species–area relationship",
    "From the equation, S₂/S₁ = (A₂/A₁)^Z = (10⁵)^0.2 = 10¹ = 10 (b). NCERT: Z lies between 0.1 and 0.2 within a "
    "region (a) and is much steeper, 0.6 to 1.2, for very large areas such as continents (c). On a logarithmic "
    "scale the relationship is a straight line; on linear axes it is a curve (rectangular hyperbola) (d false). Z "
    "is the slope (regression coefficient), and C is the Y-intercept (e false).",
    ["(10⁵)^0.2 = 10", "Z: 0.1–0.2 regional, 0.6–1.2 continental", "Straight line only on log scale; C = "
     "intercept"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    why="Options with (d) or (e) contain a false statement: the line is straight only on log axes and C is the "
        "intercept; '(b), (c) and (e)' also omits (a).",
    seconds=60, verified_by=RECOMPUTED)

add(BDC, "Hotspots and Red Data Book", "Advanced", "direct",
    "Two forest regions have similar species richness. In region X, a large share of the species are found "
    "nowhere else and the habitat is being lost rapidly; in region Y, almost no species are endemic and the "
    "habitat is stable. On NCERT's description of biodiversity hotspots, which region fits the description of a "
    "hotspot?",
    P("Region X only", ["Region Y only", "Both X and Y, since they have similar species richness",
                         "Neither, since species richness alone defines a hotspot"], "A"),
    "Criteria of a biodiversity hotspot",
    "NCERT: biodiversity hotspots are regions with very high levels of species richness and a high degree of "
    "endemism (species confined to that region and not found anywhere else), and they are also regions of "
    "accelerated habitat loss. Region X has high richness, high endemism and rapid habitat loss; region Y lacks "
    "endemism and habitat loss.",
    ["Hotspot = high richness + high endemism + accelerated habitat loss", "X has all three; Y lacks endemism"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity? (biodiversity hotspots)"),
    why="Species richness alone is not enough: endemism and accelerated habitat loss are also part of NCERT's "
        "description, which Y does not meet.",
    seconds=45)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("On an island, a tree species is pollinated by only one bird species. A plant species brought from another "
       "continent then turns invasive and spreads, people start hunting the bird for food, and part of the forest "
       "is cleared for farming. Using NCERT's 'Evil Quartet', which of the following statements are correct?",
       ["The introduced plant that has turned invasive represents alien species invasion.",
        "Clearing the forest for farming represents habitat loss and fragmentation.",
        "If the bird becomes extinct, the tree may also become extinct, which would be co-extinction.",
        "Hunting the bird beyond what its population can sustain represents over-exploitation.",
        "These changes will make the island's community more stable and productive."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["b", "c", "d", "e"], ["a", "c", "d"]], "D"),
    "Applying the Evil Quartet",
    "NCERT's four major causes of biodiversity loss: habitat loss and fragmentation (forest clearing, b), "
    "over-exploitation (hunting when need turns to greed, d), alien species invasions (an introduced species that turns "
    "invasive, as carrot grass, Lantana and water hyacinth have done in India, a) and co-extinctions (an obligate mutualist dying out with its partner, as in a "
    "plant-pollinator mutualism, c). Loss of biodiversity lowers stability and may lower plant production, so (e) "
    "is false.",
    ["Invasive introduced plant: alien invasion", "Clearing: habitat loss", "Bird–tree: co-extinction", "Hunting: over-exploitation"],
    C12_BD("loss of biodiversity: causes of biodiversity losses; consequences of loss of biodiversity"),
    why="Options with (e) contradict NCERT's account that biodiversity loss reduces stability and production; "
        "'(a), (c) and (d)' omits habitat loss (b).",
    seconds=60)
# ---------------------------------------------------------------- checks and output
def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    quota = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                     for d, n in t["quota"].items() if n})
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}

    for i, q in enumerate(QUESTIONS):
        q["question_id"] = f"NEET_BOT_{FIRST_ID + i:06d}"
        assert q["subtopic"] in subtopics[q["topic"]], (q["topic"], q["subtopic"])
    have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
    assert have == quota, {k: (have[k], quota[k]) for k in set(have) | set(quota) if have[k] != quota[k]}
    assert len(QUESTIONS) == pkg["count"] == 127, len(QUESTIONS)
    assert [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]] == pkg["question_ids"]
    order = [q["topic"] for q in QUESTIONS]
    assert sorted(order, key=pkg["topics"].index) == order       # topics in plan order

    fmts = Counter(q["format"] for q in QUESTIONS)
    keys = Counter(q["correct_answer"] for q in QUESTIONS)
    n = len(QUESTIONS)
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))
    for f in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f] >= 0.08 * n, (f, fmts[f])
    assert 0.04 * n <= fmts["numerical"] <= 0.08 * n, fmts["numerical"]
    assert all(0.22 * n <= keys[k] <= 0.28 * n for k in LETTERS), keys
    for q in QUESTIONS:
        if q["format"] == "numerical":
            assert "script:recompute" in q["verification"]["verified_by"], q["question_id"]
        if q["format"] == "assertion_reason":
            assert q["question_text"].count("Assertion (A):") == 1
    texts = [q["question_text"] for q in QUESTIONS]
    assert len(set(texts)) == len(texts)

    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "BATCH_009 package BOT_009_p2: 127 original Botany questions (Respiration in Plants to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 to "
                    "BATCH_008 were avoided or approached from a new angle. Numerical and other computable answers "
                    "re-derived by tools/batch_009/BOT_009_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()
