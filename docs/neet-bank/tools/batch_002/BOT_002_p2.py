"""Builder for BATCH_002, package BOT_002_p2 (Botany, NEET_BOT_000376..NEET_BOT_000500, 125 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Facts already tested in BATCH_000/BATCH_001 on these topics were avoided.
Numerical answers are re-derived below; the file is written only if every assert, the plan quota and the format
mix pass.

    cd docs/neet-bank && python tools/batch_002/BOT_002_p2.py
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
PACKAGE = "BOT_002_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_002_BOT_p2.json"
FIRST_ID = 376

AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

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


# ---------------------------------------------------------------- verification of computable answers
# PGD: geometric growth W1 = W0 e^(rt); W0 = 2 g, r = 0.231 per day, t = 9 days, ln 2 = 0.693
W0, r_g, t_g = 2, 0.231, 9
assert abs(r_g * t_g - 3 * 0.693) < 1e-9                  # rt = 3 ln 2, so e^(rt) = 2^3 = 8
assert W0 * 2 ** 3 == 16 and abs(W0 * math.exp(r_g * t_g) - 16) < 0.01
assert round(W0 * (1 + r_g * t_g), 1) == 6.2              # distractor: arithmetic formula W0(1 + rt)
assert 2 ** 3 == 8 and W0 * 2 * 3 == 12                    # distractors: forgot W0; multiplied instead of powered

# SRFP: 40 microspore mother cells -> tetrads -> pollen grains -> two male gametes each
mmc = 40
assert mmc * 4 == 160 and mmc * 4 * 2 == 320 and mmc * 2 == 80 and mmc * 4 * 4 == 640

# SRFP: plant with 2n = 24: nucellus (2n), functional megaspore (n), endosperm (3n), synergid (n)
n_ = 12
assert (2 * n_, n_, 3 * n_, n_) == (24, 12, 36, 12)

# PIV: F1 RrYy gametes
gam = Counter(a + b for a, b in product("Rr", "Yy"))
assert len(gam) == 4 and all(F(v, 4) == F(1, 4) for v in gam.values())

# PIV: I^A I^B x I^A i -> fraction blood group A
kids = [a + b for a, b in product(["A", "B"], ["A", "i"])]   # alleles from each parent
def blood(g):
    s = set(g)
    if s == {"A", "B"}:
        return "AB"
    if "A" in s:
        return "A"
    if "B" in s:
        return "B"
    return "O"
groups = Counter(blood(k) for k in kids)
assert F(groups["A"], 4) == F(1, 2) and F(groups["AB"], 4) == F(1, 4) and F(groups["B"], 4) == F(1, 4)

# PIV: test cross recombination frequency
parental, recomb = 440 + 430, 65 + 65
assert parental + recomb == 1000 and F(recomb, 1000) == F(13, 100)

# PIV: RrTt x RrTt, R incompletely dominant (pink heterozygote), T completely dominant
pheno = Counter()
for g1, g2 in product(product("Rr", "Tt"), repeat=2):
    rr = "".join(sorted(g1[0] + g2[0]))
    tt = "".join(sorted(g1[1] + g2[1]))
    colour = {"RR": "red", "Rr": "pink", "rr": "white"}[rr]
    height = "tall" if "T" in tt else "dwarf"
    pheno[(colour, height)] += 1
assert len(pheno) == 6 and F(pheno[("pink", "tall")], 16) == F(3, 8)

# PIV: dihybrid F2 genotype/phenotype fractions
f2 = Counter()
for g1, g2 in product(product("Rr", "Yy"), repeat=2):
    f2["".join(sorted(g1[0] + g2[0])) + "".join(sorted(g1[1] + g2[1]))] += 1
assert F(f2["RrYy"], 16) == F(1, 4) and F(f2["RRYy"], 16) == F(1, 8) and F(f2["rryy"], 16) == F(1, 16)
assert F(sum(v for k, v in f2.items() if "R" in k[:2]), 16) == F(3, 4)

# PIV: colour-blind woman (XcXc) x normal man (XY)
cb_kids = [m + f for m, f in product("cc", ["+", "Y"])]     # mother X^c X^c; father X^+ or Y
sons = [k for k in cb_kids if k.endswith("Y")]
daughters = [k for k in cb_kids if not k.endswith("Y")]
assert all(s == "cY" for s in sons) and all(d == "c+" for d in daughters)   # all sons affected, daughters carriers

# MBI: length of a 5 x 10^6 bp duplex at 0.34 nm per bp
length_m = F(5 * 10 ** 6) * F(34, 100) * F(1, 10 ** 9)
assert length_m == F(17, 10000)                           # 1.7 x 10^-3 m = 1.7 mm

# OAP: N(t+1) = N(t) + [(B + I) - (D + E)]
N0, B_, I_, D_, E_ = 500, 80, 30, 50, 20
assert N0 + (B_ + I_) - (D_ + E_) == 540
assert N0 + (B_ + E_) - (D_ + I_) == 520 and N0 + B_ - D_ == 530 and N0 + B_ + I_ + D_ + E_ == 680

# OAP: logistic dN/dt = rN(K - N)/K
r_l, K, N = F(2, 10), 1000, 250
assert r_l * N * F(K - N, K) == F(75, 2)                  # 37.5
assert r_l * N == 50 and r_l * N * F(N, K) == F(25, 2) and r_l * (K - N) == 150


# ================================================================ Plant Growth and Development (4 / 5 / 4)
C11_PGD = lambda s: ref(11, PGD, s)

add(PGD, "Growth rate", "Basic", "direct",
    "When a cell population grows geometrically in a limited nutrient supply and its growth is plotted against "
    "time, a sigmoid curve is obtained. In which phase of this curve is the growth fastest?",
    P("Log (exponential) phase", ["Lag phase", "Stationary phase", "Phase of maturation"], "B"),
    "Sigmoid growth curve",
    "In geometric growth the initial growth is slow (lag phase), then it increases rapidly at an exponential rate "
    "(log or exponential phase), when both progeny cells of each division keep dividing. With limited nutrients, "
    "growth then slows down and levels off in the stationary phase.",
    ["Lag phase: slow initial growth", "Log/exponential phase: rapid growth, both daughter cells keep dividing",
     "Stationary phase: growth slows because nutrients become limiting"],
    C11_PGD("growth rates: geometric growth and the sigmoid curve"),
    why="The lag and stationary phases are the slow parts of the curve. The phase of maturation is a zone of the "
        "growing root or shoot, not a phase of the sigmoid curve.",
    seconds=30)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "Grape growers use a plant growth regulator to increase the length of grape stalks. The regulator used is:",
    P("Gibberellins", ["Abscisic acid", "Ethylene", "Cytokinins"], "D"),
    "Physiological effects of gibberellins",
    "Gibberellins cause an increase in the length of the axis. This ability is used commercially to increase the "
    "length of grape stalks.",
    ["Increase in length of axis → gibberellins", "Application: longer grape stalks"],
    C11_PGD("gibberellins: physiological effects"),
    why="ABA is a growth inhibitor; ethylene promotes ripening and abscission; cytokinins promote cell division "
        "and lateral shoot growth, not axis elongation.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "statement_pair",
    sp("Abscisic acid is also called the stress hormone because it increases the tolerance of plants to various "
       "kinds of stresses.",
       "Abscisic acid promotes seed germination."),
    SP("C"),
    "Abscisic acid",
    "ABA acts as a general plant growth inhibitor and an inhibitor of plant metabolism. It inhibits seed "
    "germination, stimulates closure of stomata and increases tolerance to various stresses, which is why it is "
    "called the stress hormone.",
    ["Statement I: true (stress hormone)", "Statement II: false, ABA inhibits seed germination"],
    C11_PGD("abscisic acid"),
    seconds=30)

add(PGD, "Germination and growth phases", "Basic", "direct",
    "Growth in plants can be measured as an increase in cell number. According to NCERT, a single maize root "
    "apical meristem can give rise to more than:",
    P("17,500 new cells per hour", ["1,750 new cells per day", "3,50,000 new cells per hour",
                                    "17,500 new cells per day"], "B"),
    "Growth is measurable",
    "Growth at the cellular level is an increase in the amount of protoplasm, which is hard to measure directly, "
    "so other parameters are used. A single maize root apical meristem can give rise to more than 17,500 new cells "
    "per hour, whereas cells in a watermelon may increase in size by up to 3,50,000 times.",
    ["Maize root apical meristem → over 17,500 new cells per hour",
     "3,50,000 is the increase in size of watermelon cells, not a cell count"],
    C11_PGD("growth is measurable"),
    why="3,50,000 refers to the increase in cell size in watermelon. The other options change the number or the "
        "time unit.",
    seconds=30)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Removal of shoot tips (decapitation) is widely applied in tea plantations and in hedge-making.",
       "In most higher plants, the growing apical bud inhibits the growth of the lateral (axillary) buds; removing "
       "the shoot tip usually results in the growth of the lateral buds."),
    AR("A"),
    "Apical dominance",
    "Auxin produced by the growing apical bud suppresses the lateral buds (apical dominance). Decapitation removes "
    "this inhibition, so lateral buds grow and the plant becomes bushy. That is exactly why decapitation is used in "
    "tea plantations (more leafy shoots) and hedge-making (dense growth).",
    ["A: true, NCERT's applications of decapitation", "R: true, definition of apical dominance and effect of "
     "decapitation", "Lateral buds grow after decapitation → bushy plants → R explains A"],
    C11_PGD("auxins: apical dominance"),
    seconds=40)

add(PGD, "Plant growth regulators", "Intermediate", "statement_pair",
    sp("Gibberellins cause fruits like apple to elongate and improve their shape.",
       "Cytokinins are used to speed up the malting process in the brewing industry."),
    SP("C"),
    "Commercial uses of gibberellins",
    "Both uses in the statements are uses of gibberellins: they elongate apple fruits and improve their shape, "
    "and they speed up malting in brewing. Cytokinins are not used for malting.",
    ["Statement I: true (gibberellins)", "Statement II: false, malting is speeded up by gibberellins, not cytokinins"],
    C11_PGD("gibberellins: physiological effects"),
    seconds=35)

add(PGD, "Plant growth regulators", "Intermediate", "match_list",
    ml(("plant growth regulator", "chemical nature"),
       ["Indole-3-acetic acid (IAA)", "Gibberellic acid (GA₃)", "Abscisic acid (ABA)", "Ethylene"],
       ["Gas", "Terpene", "Indole compound", "Derivative of carotenoids"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
       {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
    "Chemical nature of plant growth regulators",
    "NCERT groups PGRs by chemical nature: indole compounds (IAA), adenine derivatives (kinetin), derivatives of "
    "carotenoids (ABA), terpenes (GA₃) and gases (ethylene, C₂H₄).",
    ["IAA → indole compound (A-III)", "GA₃ → terpene (B-II)", "ABA → carotenoid derivative (C-IV)",
     "Ethylene → gas (D-I)"],
    C11_PGD("plant growth regulators: characteristics"),
    why="The wrong codes swap terpene and carotenoid derivative between GA₃ and ABA, or call IAA a terpene.",
    seconds=45)

add(PGD, "Plant growth regulators", "Intermediate", "multi_statement",
    ms("Which of the following statements about auxins are correct?",
       ["Auxins help to initiate rooting in stem cuttings.",
        "Auxins promote flowering, for example in pineapples.",
        "NAA and 2,4-D are natural auxins isolated from plants.",
        "Auxins control xylem differentiation and help in cell division.",
        "Auxins are produced mainly in mature leaves and roots and move to the growing apices."]),
    P("(a), (b) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "B"),
    "Auxins: sources and functions",
    "Auxins are generally produced by the growing apices of stems and roots, from where they migrate to their "
    "regions of action. IAA and IBA are isolated from plants; NAA (naphthalene acetic acid) and 2,4-D are "
    "synthetic auxins. Auxins initiate rooting in stem cuttings, promote flowering in pineapple, control xylem "
    "differentiation and help in cell division.",
    ["(a) True", "(b) True", "(c) False: NAA and 2,4-D are synthetic", "(d) True",
     "(e) False: auxins are produced at the growing apices of stems and roots"],
    C11_PGD("auxins"),
    why="Every other option includes (c) or (e).",
    seconds=50)

add(PGD, "Differentiation and redifferentiation", "Intermediate", "statement_pair",
    sp("Differentiation in plants is closed, because cells derived from the same meristem always mature into the "
       "same kind of structure.",
       "Development in plants is under the control of intrinsic factors, such as genetic factors and plant growth "
       "regulators, as well as extrinsic factors such as light, temperature, water, oxygen and nutrition."),
    SP("D"),
    "Open differentiation and control of development",
    "Differentiation in plants is open: cells or tissues arising from the same meristem have different structures "
    "at maturity. Development is controlled by intrinsic factors (intracellular genetic factors and intercellular "
    "chemicals such as PGRs) and by extrinsic factors (light, temperature, water, oxygen, nutrition).",
    ["Statement I: false, differentiation in plants is open", "Statement II: true"],
    C11_PGD("differentiation, dedifferentiation and redifferentiation; development"),
    seconds=40)

add(PGD, "Growth rate", "Advanced", "numerical",
    "A callus of mass 2 g grows geometrically according to W₁ = W₀e^(rt), with relative growth rate r = 0.231 per "
    "day. Taking ln 2 = 0.693, what will be its mass after 9 days?",
    P("16 g", ["6.2 g", "8 g", "12 g"], "D"),
    "Geometric (exponential) growth",
    "In geometric growth W₁ = W₀e^(rt). Here rt = 0.231 × 9 = 2.079 = 3 × 0.693 = 3 ln 2, so e^(rt) = 2³ = 8. "
    "W₁ = 2 g × 8 = 16 g.",
    ["rt = 0.231 × 9 = 2.079", "2.079 = 3 × 0.693 = 3 ln 2 → e^(rt) = 2³ = 8", "W₁ = W₀ × 8 = 2 × 8 = 16 g"],
    C11_PGD("growth rates: geometric growth"),
    shortcut="rt is three times ln 2, so the callus doubles three times: 2 → 4 → 8 → 16 g.",
    why="6.2 g uses the arithmetic form W₀(1 + rt). 8 g is e^(rt) alone, forgetting to multiply by W₀. 12 g "
        "multiplies W₀ by 2 and by 3 instead of raising 2 to the power 3.",
    seconds=90, verified_by=RECOMPUTED)

add(PGD, "Plant growth regulators", "Advanced", "multi_statement",
    ms("Which of the following statements about gibberellins are correct?",
       ["More than 100 gibberellins have been reported from widely different organisms such as fungi and higher "
        "plants.",
        "All gibberellins are basic in nature.",
        "GA₃ was one of the first gibberellins to be discovered and remains the most intensively studied form.",
        "Gibberellins delay senescence, so fruits can be left on the tree longer to extend the market period.",
        "Gibberellins are derivatives of carotenoids."]),
    P("(a), (c) and (d) only",
      ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"], "A"),
    "Gibberellins",
    "More than 100 gibberellins (GA₁, GA₂, GA₃ ...) are known from fungi and higher plants; GA₃ was one of the "
    "first discovered and is the most intensively studied. All GAs are acidic. They are terpenes; it is ABA that is "
    "a carotenoid derivative. Gibberellins delay senescence, which extends the market period of fruits.",
    ["(a) True", "(b) False: all GAs are acidic", "(c) True", "(d) True",
     "(e) False: GAs are terpenes; ABA is the carotenoid derivative"],
    C11_PGD("gibberellins"),
    why="Options B and D include (b); option C includes (e).",
    seconds=55)

add(PGD, "Plant growth regulators", "Advanced", "assertion_reason",
    ar("Ethylene promotes vertical growth of seedlings and suppresses swelling of the axis.",
       "Ethylene promotes senescence and abscission of plant organs, especially of leaves and flowers."),
    AR("D"),
    "Effects of ethylene",
    "Ethylene influences horizontal growth of seedlings, swelling of the axis and apical hook formation in dicot "
    "seedlings, so the assertion reverses both effects. Ethylene does promote senescence and abscission of plant "
    "organs, especially leaves and flowers, so R is true.",
    ["A: false, ethylene promotes horizontal growth and swelling of the axis", "R: true"],
    C11_PGD("ethylene"),
    why="A is the trap: it inverts the NCERT effects (horizontal growth, swelling of the axis).",
    seconds=40)

add(PGD, "Plant growth regulators", "Advanced", "direct",
    "A grower wants a single compound that, applied as an aqueous spray, is readily absorbed and releases a "
    "growth regulator slowly inside the plant. It should hasten ripening of tomatoes and apples and accelerate "
    "abscission of flowers and fruits for thinning of cotton, cherry and walnut. The compound is:",
    P("Ethephon", ["2,4-D", "Gibberellic acid", "Abscisic acid"], "B"),
    "Ethephon as a source of ethylene",
    "Ethephon is the most widely used compound as a source of ethylene. In aqueous solution it is readily absorbed "
    "and transported within the plant and releases ethylene slowly. Ethylene hastens fruit ripening (tomatoes, "
    "apples) and accelerates abscission of flowers and fruits (thinning of cotton, cherry, walnut).",
    ["Effects described: ripening and abscission → ethylene", "Compound that releases ethylene slowly in the plant "
     "→ ethephon"],
    C11_PGD("ethylene"),
    why="2,4-D is a synthetic auxin used as a herbicide. Gibberellic acid delays senescence of fruits. Abscisic "
        "acid is a growth inhibitor and does not release ethylene.",
    seconds=40)

# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "A typical angiosperm anther is bilobed and each lobe is dithecous. How many microsporangia does such an anther "
    "have?",
    P("Four", ["Two", "One", "Eight"], "C"),
    "Structure of the anther",
    "A typical angiosperm anther is bilobed, each lobe having two theca (dithecous). The anther is a four-sided "
    "(tetragonal) structure with four microsporangia at the corners, two in each lobe.",
    ["2 lobes × 2 theca (microsporangia) per lobe = 4 microsporangia"],
    C12_SR("stamen, microsporangium and pollen grain"),
    why="Two counts only the lobes; one ignores both lobes and theca; eight doubles the real number.",
    seconds=25)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "The prominent apertures in the exine of a pollen grain, where sporopollenin is absent, are called:",
    P("Germ pores", ["Micropyles", "Lenticels", "Hila"], "D"),
    "Pollen wall",
    "The exine of the pollen grain has prominent apertures called germ pores where sporopollenin is absent. The "
    "pollen tube comes out through one of the germ pores when the pollen germinates.",
    ["Exine with apertures lacking sporopollenin → germ pores"],
    C12_SR("stamen, microsporangium and pollen grain"),
    why="The micropyle is the opening of the ovule, the hilum is the junction of ovule and funicle, and lenticels "
        "are openings in the bark of woody stems.",
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "Ovules generally differentiate a single megaspore mother cell (MMC). In which region of the nucellus is it "
    "differentiated?",
    P("Micropylar region", ["Chalazal region", "Region of the hilum", "Region of the funicle"], "B"),
    "Megasporogenesis",
    "Ovules generally differentiate a single megaspore mother cell in the micropylar region of the nucellus. It is "
    "a large cell with dense cytoplasm and a prominent nucleus, and it undergoes meiosis to form four megaspores.",
    ["MMC → large cell, dense cytoplasm, prominent nucleus", "Location → micropylar region of the nucellus"],
    C12_SR("the pistil, megasporangium (ovule) and embryo sac: megasporogenesis"),
    why="The chalaza is the basal part of the ovule opposite the micropyle; the hilum and funicle lie outside the "
        "nucellus.",
    seconds=25)

add(SRFP, "Pollination", "Basic", "direct",
    "Among animals, the dominant biotic pollinating agents are:",
    P("Insects, particularly bees", ["Birds such as sunbirds", "Bats", "Rodents such as squirrels"], "A"),
    "Animal pollination",
    "Bees, butterflies, flies, beetles, wasps, ants, moths, birds (sunbirds, hummingbirds) and bats are common "
    "pollinating agents, and some primates, arboreal rodents and reptiles also pollinate. Among the animals, insects, "
    "particularly bees, are the dominant biotic pollinating agents.",
    ["Many animals pollinate", "Dominant biotic agents → insects, especially bees"],
    C12_SR("pollination: agents of pollination"),
    why="Birds, bats and rodents do pollinate some species, but none is the dominant group.",
    seconds=20)

add(SRFP, "Double fertilisation", "Basic", "direct",
    "In the embryo sac, the fusion of one male gamete with the two polar nuclei is called:",
    P("Triple fusion", ["Syngamy", "Double fertilisation", "Generative fusion"], "D"),
    "Syngamy and triple fusion",
    "One male gamete fuses with the egg cell (syngamy) to form the diploid zygote. The other male gamete fuses with "
    "the two polar nuclei in the central cell to form the triploid primary endosperm nucleus; because three haploid "
    "nuclei are involved this is called triple fusion. The two fusions together make up double fertilisation.",
    ["Male gamete + egg → syngamy", "Male gamete + 2 polar nuclei → triple fusion",
     "Syngamy + triple fusion → double fertilisation"],
    C12_SR("double fertilisation"),
    why="Syngamy is fusion with the egg. Double fertilisation is the name for both fusions together. 'Generative "
        "fusion' is not a term NCERT uses.",
    seconds=20)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Basic", "direct",
    "The occurrence of more than one embryo in a seed is referred to as:",
    P("Polyembryony", ["Parthenocarpy", "Apomixis", "Polyploidy"], "C"),
    "Polyembryony",
    "Occurrence of more than one embryo in a seed is called polyembryony. In many Citrus and mango varieties, "
    "nucellar cells develop into additional embryos.",
    ["More than one embryo per seed → polyembryony"],
    C12_SR("apomixis and polyembryony"),
    why="Parthenocarpy is fruit formation without fertilisation; apomixis is seed formation without fertilisation; "
        "polyploidy is an increase in whole chromosome sets.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "statement_pair",
    sp("In a transverse section, a typical microsporangium is generally surrounded by four wall layers: the "
       "epidermis, endothecium, middle layers and the tapetum.",
       "Carrot grass (Parthenium), which came into India as a contaminant with imported wheat, has become ubiquitous "
       "and causes pollen allergy."),
    SP("A"),
    "Microsporangium wall; pollen and allergy",
    "A microsporangium appears near circular in section and is surrounded by four wall layers: epidermis, "
    "endothecium, middle layers and tapetum. Pollen grains of many species cause severe allergies and bronchial "
    "afflictions; Parthenium, which entered India with imported wheat, is now ubiquitous and causes pollen allergy.",
    ["Statement I: true", "Statement II: true"],
    C12_SR("stamen, microsporangium and pollen grain"),
    seconds=40)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "match_list",
    ml(("part of the ovule", "description"),
       ["Funicle", "Hilum", "Micropyle", "Chalaza"],
       ["Small opening at the tip where the integuments are absent",
        "Stalk that attaches the ovule to the placenta",
        "Basal part of the ovule, opposite the micropylar end",
        "Region where the body of the ovule fuses with the funicle"]),
    M({"A": "II", "B": "IV", "C": "I", "D": "III"},
      [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
       {"A": "II", "B": "I", "C": "IV", "D": "III"}], "B"),
    "Structure of the ovule",
    "The ovule is attached to the placenta by a stalk, the funicle. The body of the ovule fuses with the funicle at "
    "the hilum, the junction between ovule and funicle. The integuments encircle the nucellus except at the tip, "
    "where the micropyle is organised. Opposite the micropylar end is the chalaza, the basal part of the ovule.",
    ["Funicle → stalk (A-II)", "Hilum → ovule-funicle junction (B-IV)", "Micropyle → opening at tip (C-I)",
     "Chalaza → basal part opposite micropyle (D-III)"],
    C12_SR("the pistil, megasporangium (ovule) and embryo sac"),
    why="The wrong codes swap funicle with hilum, or micropyle with chalaza, the two pairs most often confused.",
    seconds=45)

add(SRFP, "Pollination", "Intermediate", "multi_statement",
    ms("Which of the following statements about insect-pollinated flowers are correct?",
       ["The majority of insect-pollinated flowers are large, colourful, fragrant and rich in nectar.",
        "When the flowers are small, a number of them are clustered into an inflorescence to make them conspicuous.",
        "Their pollen grains are generally light, non-sticky and produced in enormous numbers.",
        "Their pollen grains are generally sticky.",
        "In some species, the floral reward is a safe place for the pollinator to lay its eggs."]),
    P("(a), (b), (d) and (e) only",
      ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (c) and (e) only"], "D"),
    "Insect pollination (entomophily)",
    "Insect-pollinated flowers are mostly large, colourful, fragrant and rich in nectar; small flowers are "
    "clustered into inflorescences to be conspicuous. Their pollen grains are generally sticky so they adhere to the "
    "pollinator's body. Rewards are nectar and pollen, and in some species a safe place to lay eggs (as in "
    "Amorphophallus and Yucca). Light, non-sticky pollen is a feature of wind-pollinated flowers.",
    ["(a) True", "(b) True", "(c) False: describes wind-pollinated pollen", "(d) True", "(e) True"],
    C12_SR("pollination: agents of pollination"),
    why="Options A, B and C include (c).",
    seconds=50)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "statement_pair",
    sp("The majority of flowering plants produce unisexual flowers, so pollen rarely comes in contact with the "
       "stigma of the same flower.",
       "Continued self-pollination results in inbreeding depression."),
    SP("D"),
    "Need for outbreeding devices",
    "The majority of flowering plants produce hermaphrodite (bisexual) flowers, so pollen grains are likely to "
    "contact the stigma of the same flower. Continued self-pollination results in inbreeding depression, which is "
    "why flowering plants have evolved devices that discourage self-pollination.",
    ["Statement I: false, most flowering plants have hermaphrodite flowers", "Statement II: true"],
    C12_SR("outbreeding devices"),
    seconds=35)

add(SRFP, "Endosperm and embryo", "Intermediate", "assertion_reason",
    ar("In most flowering plants, endosperm development precedes embryo development.",
       "The zygote divides immediately after fertilisation, before the primary endosperm cell starts dividing."),
    AR("C"),
    "Endosperm before embryo",
    "The primary endosperm cell divides repeatedly to form the endosperm. Most zygotes divide only after a certain "
    "amount of endosperm is formed; this adaptation assures nutrition to the developing embryo. So A is true and "
    "R, which reverses the order, is false.",
    ["A: true", "R: false, most zygotes divide only after some endosperm has formed"],
    C12_SR("post-fertilisation events: endosperm and embryo"),
    seconds=35)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "direct",
    "According to NCERT, apomixis (production of seeds without fertilisation) is seen in:",
    P("Some species of Asteraceae and grasses", ["Pea and groundnut", "All dioecious plants such as papaya",
                                                 "Banana and other parthenocarpic plants"], "B"),
    "Apomixis",
    "Some flowering plants, such as some species of Asteraceae and grasses, have evolved a special mechanism, "
    "apomixis, to produce seeds without fertilisation. It is a form of asexual reproduction that mimics sexual "
    "reproduction.",
    ["Seeds without fertilisation → apomixis", "NCERT examples → some Asteraceae and grasses"],
    C12_SR("apomixis and polyembryony"),
    why="Pea and groundnut form seeds after fertilisation. Dioecy is an outbreeding device. Banana forms fruits "
        "without fertilisation (parthenocarpy), and these fruits are seedless.",
    seconds=30)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "numerical",
    "A microsporangium contains 40 microspore mother cells, and all of them complete microsporogenesis normally. "
    "Each resulting pollen grain eventually forms the usual number of male gametes. How many male gametes are "
    "formed in all?",
    P("320", ["160", "80", "640"], "C"),
    "Microsporogenesis and male gametes",
    "Each microspore mother cell undergoes meiosis to form a tetrad of four microspores, each of which matures into "
    "a pollen grain. In each pollen grain the generative cell divides to form two male gametes.",
    ["Pollen grains = 40 × 4 = 160", "Male gametes = 160 × 2 = 320"],
    C12_SR("microsporogenesis; pollen grain"),
    why="160 counts pollen grains, not gametes. 80 assumes each mother cell gives two pollen grains. 640 assumes "
        "four gametes per pollen grain.",
    seconds=45, verified_by=RECOMPUTED)

add(SRFP, "Endosperm and embryo", "Intermediate", "match_list",
    ml(("structure", "description"),
       ["Scutellum", "Coleoptile", "Hypocotyl", "Plumule"],
       ["Hollow foliar structure enclosing the shoot apex and leaf primordia in a grass embryo",
        "Cylindrical part of the embryonal axis below the cotyledons, ending in the radicle",
        "Stem tip at the end of the epicotyl",
        "Single cotyledon of the grass family, situated towards one side of the embryonal axis"]),
    M({"A": "IV", "B": "I", "C": "II", "D": "III"},
      [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "IV", "B": "I", "C": "III", "D": "II"},
       {"A": "IV", "B": "II", "C": "I", "D": "III"}], "A"),
    "Parts of the embryo",
    "In the grass family the single cotyledon is the scutellum, situated laterally on the embryonal axis. The "
    "epicotyl of a monocot embryo has the shoot apex and a few leaf primordia enclosed in a hollow foliar structure, "
    "the coleoptile. In a dicot embryo, the part of the axis below the cotyledons is the hypocotyl, ending in the "
    "radicle; the part above is the epicotyl, ending in the plumule (stem tip).",
    ["Scutellum → single lateral cotyledon of grasses (A-IV)", "Coleoptile → sheath over shoot apex (B-I)",
     "Hypocotyl → below cotyledons, ends in radicle (C-II)", "Plumule → stem tip of epicotyl (D-III)"],
    C12_SR("post-fertilisation events: embryo"),
    why="The wrong codes swap scutellum with coleoptile, or hypocotyl with plumule.",
    seconds=45)

add(SRFP, "Double fertilisation", "Advanced", "multi_statement",
    ms("Which of the following statements about events in the embryo sac during and after fertilisation are "
       "correct?",
       ["The primary endosperm cell develops into the endosperm.",
        "The synergids and antipodals degenerate after fertilisation.",
        "The zygote develops into the embryo.",
        "The pollen tube releases the two male gametes into the cytoplasm of an antipodal cell.",
        "The two male gametes are formed by division of the vegetative cell."]),
    P("(a), (b) and (c) only",
      ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"], "B"),
    "Double fertilisation and post-fertilisation events",
    "The pollen tube enters one of the synergids (guided by the filiform apparatus) and releases two male gametes "
    "into its cytoplasm. These male gametes were formed by division of the generative cell. After double "
    "fertilisation, the primary endosperm cell develops into the endosperm and the zygote into the embryo, while "
    "the synergids and antipodals degenerate.",
    ["(a) True", "(b) True", "(c) True", "(d) False: the gametes are released into a synergid",
     "(e) False: male gametes come from the generative cell"],
    C12_SR("double fertilisation; post-fertilisation events"),
    why="Options A, C and D include (d) or (e).",
    seconds=55)

add(SRFP, "Pollination", "Advanced", "assertion_reason",
    ar("Xenogamy is the only type of pollination that brings genetically different types of pollen grains to the "
       "stigma.",
       "In xenogamy, pollen grains are transferred from the anther to the stigma of a different plant."),
    AR("A"),
    "Autogamy, geitonogamy and xenogamy",
    "In autogamy pollen comes from the same flower, and in geitonogamy from another flower of the same plant; "
    "geitonogamy is functionally cross-pollination but genetically similar to autogamy because the pollen comes "
    "from the same plant. Only in xenogamy does pollen come from a different plant, so only xenogamy brings "
    "genetically different pollen to the stigma. R states that defining feature, so it explains A.",
    ["A: true", "R: true, pollen from a different plant", "A different plant carries a different genotype → R "
     "explains A"],
    C12_SR("pollination: kinds of pollination"),
    seconds=45)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "statement_pair",
    sp("In plants that shed pollen in the three-celled condition, the pollen tubes carry the two male gametes from "
       "the beginning.",
       "In plants that shed pollen in the two-celled condition, the generative cell divides to form the two male "
       "gametes before the pollen grain lands on the stigma."),
    SP("C"),
    "Pollen tube growth",
    "After a compatible pollen lands, it germinates and its tube grows through the stigma and style. Where pollen "
    "is shed at the three-celled stage, the tube carries the two male gametes from the beginning. Where it is shed "
    "at the two-celled stage, the generative cell divides to form the two male gametes during the growth of the "
    "pollen tube in the stigma, i.e. after the pollen has landed.",
    ["Statement I: true", "Statement II: false, the division happens during pollen tube growth in the stigma"],
    C12_SR("pollen-pistil interaction"),
    why="Statement II shifts the timing of the generative cell division; that detail is the trap.",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "direct",
    "In a flowering plant with 2n = 24, how many chromosomes are present in a cell of the nucellus, the functional "
    "megaspore, an endosperm cell and a synergid, respectively?",
    P("24, 12, 36 and 12", ["12, 12, 36 and 24", "24, 24, 36 and 12", "24, 12, 24 and 12"], "D"),
    "Ploidy of ovule and embryo sac tissues",
    "The nucellus is sporophytic tissue of the parent plant (2n = 24). The megaspore is formed by meiosis (n = 12). "
    "The synergid is part of the female gametophyte formed from the megaspore by mitosis (n = 12). The endosperm "
    "comes from the primary endosperm nucleus formed by triple fusion (3n = 36).",
    ["Nucellus → 2n = 24", "Functional megaspore → n = 12", "Endosperm → 3n = 36", "Synergid → n = 12"],
    C12_SR("megasporogenesis; double fertilisation"),
    why="A treats the nucellus as haploid and the synergid as diploid. B forgets that the megaspore forms by "
        "meiosis. C treats the endosperm as diploid.",
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Advanced", "multi_statement",
    ms("Which of the following statements are correct?",
       ["Parthenocarpy can be induced through the application of growth hormones, and such fruits are seedless.",
        "Apomixis is a form of asexual reproduction that mimics sexual reproduction.",
        "In some species, the diploid egg cell is formed without reduction division and develops into the embryo "
        "without fertilisation.",
        "Parthenocarpic fruits contain seeds formed by apomixis.",
        "Apomixis is the development of a fruit without fertilisation."]),
    P("(a), (b) and (c) only",
      ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"], "C"),
    "Apomixis and parthenocarpy",
    "Parthenocarpy is the development of fruit without fertilisation; it can be induced by growth hormones and the "
    "fruits are seedless. Apomixis is the production of seeds without fertilisation, an asexual process mimicking "
    "sexual reproduction; in some species a diploid egg forms without reduction division and develops into the "
    "embryo without fertilisation.",
    ["(a) True", "(b) True", "(c) True", "(d) False: parthenocarpic fruits are seedless",
     "(e) False: that describes parthenocarpy; apomixis produces seeds"],
    C12_SR("apomixis and polyembryony; parthenocarpy"),
    why="Options A, B and D include (d) or (e).",
    seconds=50)

add(SRFP, "Pollination", "Advanced", "assertion_reason",
    ar("In most water-pollinated species, the pollen grains are protected from wetting by a mucilaginous covering.",
       "Pollination by water is quite rare in flowering plants and is limited to about 30 genera, mostly "
       "monocotyledons."),
    AR("B"),
    "Pollination by water",
    "Both statements are NCERT facts about water pollination. The mucilaginous covering protects the pollen from "
    "getting wet in water. The rarity of water pollination (about 30 genera, mostly monocots) is a separate fact "
    "about its distribution and does not explain why the pollen has a protective covering.",
    ["A: true", "R: true", "R is about how rare water pollination is, not about protecting pollen → B"],
    C12_SR("pollination: agents of pollination"),
    why="Option A is the trap: R is a true fact about the same topic but explains nothing about the mucilage.",
    seconds=45)

# ================================================================ Principles of Inheritance and Variation (7 / 10 / 7)
C12_PI = lambda s: ref(12, PIV, s)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Gregor Mendel conducted his hybridisation experiments on garden peas over a period of:",
    P("Seven years (1856–1863)", ["Three years (1863–1866)", "Two years (1900–1902)",
                                  "Twelve years (1851–1863)"], "B"),
    "Mendel's experiments",
    "Mendel conducted hybridisation experiments on garden peas for seven years (1856–1863) and proposed the laws of "
    "inheritance in living organisms.",
    ["Duration of Mendel's pea experiments → seven years, 1856 to 1863"],
    C12_PI("Mendel's laws of inheritance"),
    why="The other periods do not match NCERT; 1900 is the year his work was rediscovered.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "In 1900, Mendel's results on the inheritance of characters were independently rediscovered by:",
    P("de Vries, Correns and von Tschermak", ["Sutton and Boveri", "Morgan and Sturtevant",
                                               "Watson and Crick"], "A"),
    "Rediscovery of Mendel's work",
    "Mendel's work remained unrecognised for several decades. In 1900, three scientists, de Vries, Correns and von "
    "Tschermak, independently rediscovered his results on the inheritance of characters.",
    ["1900 → independent rediscovery by de Vries, Correns and von Tschermak"],
    C12_PI("chromosomal theory of inheritance"),
    why="Sutton and Boveri linked chromosome movement to Mendel's factors; Morgan and Sturtevant worked on linkage "
        "and gene mapping in Drosophila; Watson and Crick proposed the double helix of DNA.",
    seconds=20)

add(PIV, "Sex determination", "Basic", "direct",
    "Henking (1891) traced a specific nuclear structure all through spermatogenesis in a few insects and named it "
    "the 'X body'. What did he observe about its distribution?",
    P("Only 50 per cent of the sperm received the X body after spermatogenesis",
      ["All the sperm received the X body", "All the eggs lacked the X body",
       "The X body was found only in somatic cells"], "D"),
    "Discovery of the X body",
    "Henking observed that 50 per cent of the sperm received this structure after spermatogenesis while the other "
    "50 per cent did not. He named it the X body but could not explain its significance; later it was named the X "
    "chromosome.",
    ["Structure traced through spermatogenesis → X body", "Distribution → only half the sperm received it"],
    C12_PI("sex determination"),
    why="Henking studied spermatogenesis and found the structure in only half the sperm, not all; he made no "
        "observation about eggs or restriction to somatic cells.",
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "statement_pair",
    sp("α-thalassemia is controlled by a single gene, HBB, on chromosome 11.",
       "Thalassemia is a quantitative problem of synthesising too few globin molecules, whereas sickle-cell anaemia "
       "is a qualitative problem of synthesising an incorrectly functioning globin."),
    SP("D"),
    "Thalassemia",
    "Thalassemia is an autosome-linked recessive blood disease. α-thalassemia is controlled by two closely linked "
    "genes, HBA1 and HBA2, on chromosome 16; β-thalassemia is controlled by a single gene, HBB, on chromosome 11. "
    "Thalassemia is a quantitative problem (too few globin molecules) while sickle-cell anaemia is a qualitative "
    "problem (incorrectly functioning globin).",
    ["Statement I: false, it describes β-thalassemia; α-thalassemia: HBA1 and HBA2 on chromosome 16",
     "Statement II: true"],
    C12_PI("Mendelian disorders: thalassemia"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "Failure of segregation of chromatids during the cell division cycle, resulting in the gain or loss of a "
    "chromosome, is called:",
    P("Aneuploidy", ["Polyploidy", "Point mutation", "Crossing over"], "C"),
    "Chromosomal disorders",
    "Chromosomal disorders are caused by absence, excess or abnormal arrangement of chromosomes. Failure of "
    "segregation of chromatids during cell division results in gain or loss of one or more chromosomes, called "
    "aneuploidy (as in Down's syndrome).",
    ["Gain or loss of individual chromosome(s) → aneuploidy"],
    C12_PI("chromosomal disorders"),
    why="Polyploidy is an increase in a whole set of chromosomes; a point mutation changes a single base; crossing "
        "over exchanges segments between homologous chromosomes.",
    seconds=25)

add(PIV, "Multiple alleles and pleiotropy", "Basic", "statement_pair",
    sp("Multiple alleles can be found only when population studies are made.",
       "A single diploid individual can carry more than two alleles of the same gene."),
    SP("C"),
    "Multiple alleles",
    "When more than two alleles govern the same character, they are called multiple alleles (the ABO blood group "
    "gene I is the NCERT example). Since an individual has only two alleles of a gene, multiple alleles can be "
    "found only when population studies are made.",
    ["Statement I: true", "Statement II: false, an individual has only two alleles of a gene"],
    C12_PI("co-dominance and multiple alleles"),
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "Failure of cytokinesis after the telophase stage of cell division increases the number of whole sets of "
    "chromosomes. This condition, called polyploidy, is often seen in:",
    P("Plants", ["Human males only", "Bacteria", "Human females only"], "B"),
    "Polyploidy",
    "Failure of cytokinesis after telophase results in an increase in a whole set of chromosomes in an organism. "
    "This phenomenon is known as polyploidy, and this condition is often seen in plants.",
    ["Whole chromosome set added → polyploidy", "NCERT: often seen in plants"],
    C12_PI("chromosomal disorders"),
    why="Polyploidy is not restricted to one human sex; bacteria are prokaryotes without such chromosome sets.",
    seconds=25)

add(PIV, "Incomplete and co-dominance", "Intermediate", "direct",
    "In pea, a gene B controls starch synthesis. BB seeds are round with large starch grains, bb seeds are "
    "wrinkled with smaller starch grains, and Bb seeds are round with starch grains of intermediate size. Which "
    "conclusion is correct?",
    P("B is dominant for seed shape, but for starch grain size the alleles show incomplete dominance",
      ["B shows complete dominance for both seed shape and starch grain size",
       "The alleles show co-dominance for seed shape",
       "b is dominant for starch grain size and recessive for seed shape"], "D"),
    "Dominance depends on the phenotype examined",
    "Heterozygous Bb seeds are round, so B appears dominant for seed shape. But Bb seeds have starch grains of "
    "intermediate size, so if starch grain size is taken as the phenotype, the alleles show incomplete dominance. "
    "Dominance is therefore not an autonomous feature of a gene; it depends on the phenotype chosen.",
    ["Shape: Bb round like BB → B dominant", "Starch grain size: Bb intermediate → incomplete dominance"],
    C12_PI("incomplete dominance, co-dominance and multiple alleles"),
    why="Option A ignores the intermediate grain size. Co-dominance would need both parental phenotypes to show in "
        "Bb. b is not dominant for either character.",
    seconds=50)

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "A pea plant of genotype RrYy is obtained by crossing RRYY with rryy. The two genes assort independently. The "
    "gametes produced by this F1 plant are:",
    P("Four kinds, RY, Ry, rY and ry, each with a frequency of 25 per cent",
      ["Two kinds, RY and ry, each with a frequency of 50 per cent",
       "Four kinds, with RY and ry at 40 per cent each and Ry and rY at 10 per cent each",
       "Nine kinds, in the ratio 1 : 2 : 1 : 2 : 4 : 2 : 1 : 2 : 1"], "A"),
    "Independent assortment and gamete formation",
    "Because the R/r and Y/y pairs segregate independently, each R or r gamete is equally likely to receive Y or "
    "y. The F1 therefore forms four kinds of gametes, RY, Ry, rY and ry, each with a frequency of 1/4. Random "
    "fusion of these gametes gives the 9 : 3 : 3 : 1 F2 ratio.",
    ["R or r: 1/2 each; Y or y: 1/2 each", "Independent → each combination 1/2 × 1/2 = 1/4"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="Two kinds of gametes would mean complete linkage; unequal frequencies would mean linkage with "
        "recombination; nine is the number of F2 genotypes, not gamete types.",
    seconds=40, verified_by=RECOMPUTED)

add(PIV, "Mendelian inheritance", "Intermediate", "assertion_reason",
    ar("In Mendel's monohybrid crosses, the recessive parental trait reappears in the F2 generation in a blended, "
       "intermediate form.",
       "Alleles do not show any blending, and both parental characters are recovered as such in the F2 generation, "
       "though one of them is not seen in the F1."),
    AR("D"),
    "Law of segregation",
    "In the F1 the recessive trait is not expressed, but in the F2 it is expressed without any blending. The alleles "
    "do not blend; they segregate during gamete formation, so both parental characters are recovered as such in "
    "the F2. Hence A is false and R is true.",
    ["A: false, the recessive trait reappears unblended", "R: true"],
    C12_PI("inheritance of one gene: law of segregation"),
    seconds=35)

add(PIV, "Linkage and crossing over", "Intermediate", "statement_pair",
    sp("In Morgan's dihybrid crosses in Drosophila, when the two genes were on the same chromosome, the parental gene "
       "combinations were much more frequent than the non-parental ones.",
       "Morgan used the term recombination to describe the generation of non-parental gene combinations."),
    SP("A"),
    "Linkage and recombination",
    "Morgan carried out several dihybrid crosses in Drosophila to study sex-linked genes. When the two genes were on "
    "the same chromosome, the proportion of parental gene combinations was much higher than that of the "
    "non-parental type. He attributed this to the physical association (linkage) of the genes and used the term "
    "recombination for the generation of non-parental gene combinations.",
    ["Statement I: true", "Statement II: true"],
    C12_PI("linkage and recombination"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "match_list",
    ml(("disorder", "type"),
       ["Haemophilia", "Phenylketonuria", "Down's syndrome", "Turner's syndrome"],
       ["Trisomy of chromosome 21", "Autosomal recessive Mendelian disorder",
        "Absence of one X chromosome (45, X0)", "Sex-linked recessive Mendelian disorder"]),
    M({"A": "IV", "B": "II", "C": "I", "D": "III"},
      [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
       {"A": "IV", "B": "I", "C": "II", "D": "III"}], "B"),
    "Mendelian and chromosomal disorders",
    "Haemophilia is a sex-linked recessive disease. Phenylketonuria is an inborn error of metabolism inherited as "
    "an autosomal recessive trait. Down's syndrome is caused by an additional copy of chromosome 21 (trisomy 21). "
    "Turner's syndrome is caused by the absence of one X chromosome (45 with X0).",
    ["Haemophilia → sex-linked recessive (A-IV)", "Phenylketonuria → autosomal recessive (B-II)",
     "Down's syndrome → trisomy 21 (C-I)", "Turner's syndrome → 45, X0 (D-III)"],
    C12_PI("Mendelian disorders; chromosomal disorders"),
    why="The wrong codes swap the two Mendelian disorders, or the two chromosomal ones.",
    seconds=45)

add(PIV, "Sex determination", "Intermediate", "multi_statement",
    ms("Which of the following statements about sex determination are correct?",
       ["In the XO type of sex determination, all the eggs bear an additional X chromosome besides the autosomes.",
        "In Drosophila, the male has one X and one Y chromosome.",
        "In humans, the sex of the child is decided by the mother.",
        "Of the 23 pairs of chromosomes in humans, 22 pairs are autosomes, exactly the same in males and females.",
        "In birds, the male produces two different types of gametes."]),
    P("(a), (b) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "C"),
    "Mechanisms of sex determination",
    "In XO type (as in grasshopper) all eggs carry an X besides the autosomes, while sperm are of two kinds. "
    "Drosophila and humans show XX-XY (male heterogamety). In humans 22 pairs are autosomes; the father produces "
    "X-bearing and Y-bearing sperm, so the sperm (father) decides the child's sex. In birds the female is ZW and "
    "produces two types of gametes, while the ZZ male produces one type.",
    ["(a) True", "(b) True", "(c) False: the sperm decides", "(d) True",
     "(e) False: in birds the female is heterogametic"],
    C12_PI("sex determination"),
    why="Options A, B and D include (c) or (e).",
    seconds=50)

add(PIV, "Polygenic inheritance", "Intermediate", "statement_pair",
    sp("Polygenic traits usually show distinct alternate forms, such as tall and dwarf, with no intermediates.",
       "Polygenic traits are generally controlled by three or more genes."),
    SP("D"),
    "Polygenic inheritance",
    "Mendel studied traits with distinct alternate forms. Polygenic traits, like human height and skin colour, "
    "instead show a gradient of phenotypes. Such traits are generally controlled by three or more genes, each "
    "allele making an additive contribution.",
    ["Statement I: false, polygenic traits are spread across a gradient", "Statement II: true"],
    C12_PI("polygenic inheritance"),
    seconds=35)

add(PIV, "Sex-linked inheritance", "Intermediate", "assertion_reason",
    ar("Red-green colour blindness occurs in about 8 per cent of males but only about 0.4 per cent of females.",
       "The genes that lead to red-green colour blindness are located on the Y chromosome."),
    AR("C"),
    "Colour blindness",
    "Colour blindness occurs in about 8% of males and about 0.4% of females. This is because the genes that lead "
    "to red-green colour blindness are on the X chromosome: males have only one X, while a female is affected only "
    "if both her X chromosomes carry the gene. R puts the gene on the Y chromosome, which is false (a Y-linked "
    "trait would never appear in females).",
    ["A: true", "R: false, the genes are X-linked"],
    C12_PI("sex-linked inheritance: colour blindness"),
    seconds=35)

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "Which feature of Mendel's experiments gave greater credibility to the data that he collected?",
    P("A large sampling size",
      ["Use of Drosophila, which completes its life cycle in about two weeks",
       "Study of traits that showed blending in the F1",
       "Study of only one generation of offspring"], "D"),
    "Why Mendel succeeded",
    "Mendel's experiments had a large sampling size, which gave greater credibility to his data. Confirmation over "
    "successive generations showed that his results pointed to general rules of inheritance. He was also the first "
    "to apply statistical analysis and mathematical logic to problems in biology.",
    ["Large number of plants and crosses → greater credibility of data"],
    C12_PI("Mendel's laws of inheritance"),
    why="Drosophila was Morgan's material; Mendel chose traits with distinct alternate forms, not blending; he "
        "followed several generations.",
    seconds=30)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "numerical",
    "A man with blood group AB (IᴬIᴮ) marries a woman with blood group A who is heterozygous (Iᴬi). What fraction "
    "of their children are expected to have blood group A?",
    P("1/2", ["1/4", "3/4", "1/3"], "B"),
    "ABO blood groups: co-dominance and multiple alleles",
    "Gametes of the man: Iᴬ and Iᴮ; gametes of the woman: Iᴬ and i. The four equally likely children are IᴬIᴬ "
    "(A), Iᴬi (A), IᴬIᴮ (AB) and Iᴮi (B).",
    ["Children: IᴬIᴬ, Iᴬi, IᴬIᴮ, Iᴮi (1/4 each)", "Blood group A: IᴬIᴬ + Iᴬi = 2/4 = 1/2",
     "AB = 1/4, B = 1/4, O = 0"],
    C12_PI("co-dominance and multiple alleles: ABO blood groups"),
    why="1/4 counts only IᴬIᴬ. 3/4 wrongly counts IᴬIᴮ as group A, ignoring co-dominance. 1/3 treats the three "
        "phenotypes as equally likely.",
    seconds=50, verified_by=RECOMPUTED)

add(PIV, "Linkage and crossing over", "Advanced", "numerical",
    "A dihybrid AaBb, which received AB from one parent and ab from the other, is test-crossed with aabb. The "
    "1000 progeny are: 440 AaBb, 430 aabb, 65 Aabb and 65 aaBb. The recombination frequency between the genes is:",
    P("13 per cent", ["87 per cent", "6.5 per cent", "26 per cent"], "A"),
    "Recombination frequency",
    "In a test cross, each progeny class shows the gamete received from the dihybrid parent. Parental gametes (AB, "
    "ab) give AaBb and aabb; non-parental (recombinant) gametes (Ab, aB) give Aabb and aaBb. Recombination frequency "
    "= recombinants / total. Sturtevant used such frequencies as a measure of the distance between genes.",
    ["Parental types: 440 + 430 = 870", "Recombinant types: 65 + 65 = 130",
     "Recombination frequency = 130/1000 = 13%"],
    C12_PI("linkage and recombination"),
    why="87% is the parental fraction. 6.5% counts only one recombinant class. 26% doubles the recombinants.",
    seconds=70, verified_by=RECOMPUTED)

add(PIV, "Incomplete and co-dominance", "Advanced", "numerical",
    "In a plant, flower colour shows incomplete dominance (RR red, Rr pink, rr white), while height shows complete "
    "dominance (T, tall, over t, dwarf). The two genes assort independently. In the progeny of RrTt × RrTt, how many "
    "different phenotypes appear, and what fraction of the progeny is pink-flowered and tall?",
    P("6 phenotypes; 3/8", ["4 phenotypes; 9/16", "9 phenotypes; 3/8", "6 phenotypes; 1/4"], "C"),
    "Combining incomplete and complete dominance",
    "Treat each gene separately and multiply. Flower colour: Rr × Rr gives red : pink : white = 1 : 2 : 1, i.e. "
    "three phenotypes, pink = 1/2. Height: Tt × Tt gives tall : dwarf = 3 : 1, two phenotypes, tall = 3/4.",
    ["Colour: 3 phenotypes, P(pink) = 1/2", "Height: 2 phenotypes, P(tall) = 3/4",
     "Phenotypes = 3 × 2 = 6", "P(pink and tall) = 1/2 × 3/4 = 3/8"],
    C12_PI("incomplete dominance; inheritance of two genes"),
    shortcut="Number of phenotypes = product of phenotypes per gene: 3 × 2 = 6.",
    why="4 and 9/16 assume complete dominance for both genes. 9 is the number of genotypes, not phenotypes. 1/4 "
        "uses 1/4 for pink (confusing it with red) instead of 1/2.",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "assertion_reason",
    ar("Individuals heterozygous for sickle-cell anaemia (HbᴬHbˢ) appear apparently unaffected but are carriers of "
       "the disease.",
       "The disease is controlled by a single pair of alleles, Hbᴬ and Hbˢ, and of the three possible genotypes "
       "only individuals homozygous for Hbˢ show the diseased phenotype."),
    AR("A"),
    "Sickle-cell anaemia as an autosomal recessive trait",
    "Sickle-cell anaemia is an autosome-linked recessive trait. Only HbˢHbˢ individuals show the disease. "
    "Heterozygotes therefore appear apparently unaffected, yet they carry Hbˢ and have a 50% probability of "
    "passing it to each child, i.e. they are carriers. R gives the recessive nature of the allele, which is the "
    "reason for A.",
    ["A: true", "R: true", "Only the homozygote is affected → heterozygote unaffected carrier → R explains A"],
    C12_PI("Mendelian disorders: sickle-cell anaemia"),
    seconds=40)

add(PIV, "Linkage and crossing over", "Advanced", "multi_statement",
    ms("Which of the following statements about the chromosomal theory of inheritance and Morgan's work are "
       "correct?",
       ["One reason Mendel's work remained unrecognised was that the use of mathematics to explain biological "
        "phenomena was new and unacceptable to many biologists of the time.",
        "Chromosomes occur singly in diploid cells, whereas genes occur in pairs.",
        "The two alleles of a gene pair are located on homologous sites on homologous chromosomes.",
        "Drosophila is suitable for genetic studies because it can be grown on a simple synthetic medium, completes "
        "its life cycle in about two weeks and a single mating gives a large number of progeny.",
        "Morgan found that genes located on the X chromosome always assort independently of each other."]),
    P("(a), (c) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Chromosomal theory of inheritance",
    "Mendel's work went unrecognised partly because communication was not easy and the use of mathematics in "
    "biology was new and unacceptable. Chromosomes as well as genes occur in pairs, and the two alleles of a gene "
    "pair lie on homologous sites of homologous chromosomes. Morgan chose Drosophila for its simple culture, "
    "two-week life cycle, large progeny and clear sex differences. He found that genes on the X chromosome did not "
    "assort independently: they were linked.",
    ["(a) True", "(b) False: both chromosomes and genes occur in pairs", "(c) True", "(d) True",
     "(e) False: linked X-chromosome genes did not segregate independently"],
    C12_PI("chromosomal theory of inheritance; linkage and recombination"),
    why="Options A, B and C include (b) or (e).",
    seconds=60)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "statement_pair",
    sp("In pleiotropy, a single phenotype is controlled by several genes acting together.",
       "In co-dominance, the F1 generation resembles both parents."),
    SP("D"),
    "Pleiotropy and co-dominance",
    "Pleiotropy is the reverse of Statement I: a single gene exhibits multiple phenotypic expressions, usually "
    "because the gene affects metabolic pathways that contribute to different phenotypes. A single phenotype "
    "controlled by several genes describes polygenic inheritance. In co-dominance the F1 resembles both parents "
    "(as in blood group AB), unlike incomplete dominance where it is intermediate.",
    ["Statement I: false, it describes polygenic inheritance", "Statement II: true"],
    C12_PI("pleiotropy; co-dominance"),
    why="Statement I swaps the definitions of pleiotropy and polygenic inheritance; that swap is the trap.",
    seconds=40)

add(PIV, "Mendelian inheritance", "Advanced", "match_list",
    ml(("F2 genotype or phenotype of the dihybrid cross RRYY × rryy", "expected fraction of the F2"),
       ["RrYy", "RRYy", "rryy", "Round seeds (any genotype)"],
       ["1/16", "1/4", "3/4", "1/8"]),
    M({"A": "II", "B": "IV", "C": "I", "D": "III"},
      [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
       {"A": "III", "B": "IV", "C": "I", "D": "II"}], "B"),
    "Dihybrid F2 frequencies",
    "With independent assortment, each gene in the F2 gives 1/4 homozygous dominant, 1/2 heterozygous and 1/4 "
    "homozygous recessive, and round (R_) = 3/4. Multiply the probabilities for the two genes.",
    ["RrYy = 1/2 × 1/2 = 1/4 (A-II)", "RRYy = 1/4 × 1/2 = 1/8 (B-IV)", "rryy = 1/4 × 1/4 = 1/16 (C-I)",
     "Round = 3/4 (D-III)"],
    C12_PI("inheritance of two genes"),
    why="The wrong codes swap 1/4 and 1/8 (taking RRYy as doubly heterozygous), or confuse the phenotype fraction "
        "3/4 with a genotype fraction.",
    seconds=75, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "direct",
    "A colour-blind woman marries a man with normal colour vision. Which outcome is expected among their children?",
    P("All sons colour blind; all daughters with normal vision but carriers",
      ["All children with normal vision", "All daughters colour blind; all sons normal",
       "Half the sons and half the daughters colour blind"], "C"),
    "X-linked recessive inheritance",
    "The woman is XᶜXᶜ, so every child receives an Xᶜ from her. Sons receive their only X from the mother and Y "
    "from the father, so all sons are XᶜY (colour blind). Daughters receive the father's normal X as well, so all "
    "are XᶜX (normal vision, carriers).",
    ["Mother XᶜXᶜ → every egg carries Xᶜ", "Father X Y → daughters get X, sons get Y",
     "Sons XᶜY: colour blind; daughters XᶜX: carriers with normal vision"],
    C12_PI("sex-linked inheritance: colour blindness"),
    why="Option A ignores that sons get their only X from the mother. Option B reverses the sexes. Option D would "
        "need a carrier mother and a colour-blind father.",
    seconds=50, verified_by=RECOMPUTED)

# ================================================================ Molecular Basis of Inheritance (7 / 10 / 7)
C12_MB = lambda s: ref(12, MBI, s)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "In a nucleoside, the nitrogenous base is linked to the OH of the 1' carbon of the pentose sugar through a:",
    P("N-glycosidic linkage", ["Phosphoester linkage", "Phosphodiester linkage", "Hydrogen bond"], "D"),
    "Structure of a nucleotide",
    "A nitrogenous base is linked to the 1'C OH of the pentose sugar through an N-glycosidic linkage to form a "
    "nucleoside. A phosphate group linked to the 5'-OH of the nucleoside through a phosphoester linkage gives a "
    "nucleotide, and nucleotides are joined through 3'-5' phosphodiester linkages to form a polynucleotide.",
    ["Base + sugar (1'C) → N-glycosidic linkage → nucleoside", "Phosphate + 5'-OH → phosphoester → nucleotide",
     "Nucleotide + nucleotide → 3'-5' phosphodiester linkage"],
    C12_MB("structure of polynucleotide chain"),
    why="Phosphoester and phosphodiester bonds involve the phosphate; hydrogen bonds join complementary bases of "
        "the two strands.",
    seconds=25)

add(MBI, "DNA packaging", "Basic", "direct",
    "Histones are positively charged proteins because they are rich in the basic amino acid residues:",
    P("Lysine and arginine", ["Glutamic acid and aspartic acid", "Glycine and alanine", "Cysteine and methionine"],
      "B"),
    "Histones",
    "In eukaryotes, the negatively charged DNA is packaged with a set of positively charged basic proteins called "
    "histones. Histones are rich in the basic amino acid residues lysine and arginine, which carry positive charges "
    "in their side chains.",
    ["Histones → positive charge", "Basic residues → lysine and arginine"],
    C12_MB("packaging of DNA helix"),
    why="Glutamic and aspartic acids are acidic; glycine, alanine, cysteine and methionine are not basic residues.",
    seconds=20)

add(MBI, "DNA as genetic material", "Basic", "direct",
    "In Griffith's experiments with Streptococcus pneumoniae, the S strain bacteria formed smooth, shiny colonies "
    "because they have:",
    P("A mucous (polysaccharide) coat", ["Pili all over the cell surface", "Flagella", "A protein capsid"], "A"),
    "Griffith's transforming principle experiment",
    "Griffith grew Streptococcus pneumoniae on culture plates. Some strains produced smooth, shiny colonies (S); "
    "others produced rough colonies (R). This is because the S strain bacteria have a mucous (polysaccharide) coat, "
    "while the R strain does not. Mice infected with the S strain die of pneumonia.",
    ["Smooth colonies → S strain → mucous (polysaccharide) coat", "R strain → no coat, rough colonies"],
    C12_MB("the search for genetic material: transforming principle"),
    why="The difference between S and R strains is the polysaccharide coat; a protein capsid belongs to viruses.",
    seconds=25)

add(MBI, "Transcription", "Basic", "direct",
    "A transcription unit in DNA is defined primarily by three regions. These are:",
    P("A promoter, the structural gene and a terminator", ["An operator, the structural gene and a repressor",
                                                           "An origin, a promoter and an operator",
                                                           "A cap, the structural gene and a poly-A tail"], "C"),
    "Transcription unit",
    "A transcription unit in DNA is defined primarily by three regions: a promoter, the structural gene and a "
    "terminator. The promoter is located towards the 5' end (upstream) of the structural gene and the terminator "
    "towards the 3' end (downstream), with reference to the coding strand.",
    ["Transcription unit = promoter + structural gene + terminator"],
    C12_MB("transcription: transcription unit"),
    why="Operator and repressor belong to the operon model of regulation; origin is for replication; cap and tail "
        "are added to hnRNA after transcription.",
    seconds=25)

add(MBI, "Genetic code and translation", "Basic", "assertion_reason",
    ar("George Gamow suggested that the genetic code should be made up of three nucleotides.",
       "With four bases, a triplet code gives 4³ = 64 combinations, enough to code for all 20 amino acids, whereas a "
       "doublet code would give only 4² = 16."),
    AR("A"),
    "Why the code is a triplet",
    "Gamow, a physicist, argued that since there are only four bases and they must code for 20 amino acids, the code "
    "must use a combination of bases. A doublet gives only 16 combinations, fewer than 20; a triplet gives 64, "
    "more than enough. R is the reasoning behind A.",
    ["A: true", "R: true; 16 < 20 < 64", "R gives the reason for a triplet code → R explains A"],
    C12_MB("genetic code"),
    seconds=35)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "direct",
    "The technique of DNA fingerprinting was initially developed by:",
    P("Alec Jeffreys", ["Francis Crick", "Erwin Chargaff", "Har Gobind Khorana"], "B"),
    "DNA fingerprinting",
    "The technique of DNA fingerprinting was initially developed by Alec Jeffreys. He used a satellite DNA as a "
    "probe that shows a very high degree of polymorphism, called variable number of tandem repeats (VNTR).",
    ["Developer of DNA fingerprinting → Alec Jeffreys"],
    C12_MB("DNA fingerprinting"),
    why="Crick proposed the central dogma; Chargaff gave the base ratio rules; Khorana synthesised RNA molecules of "
        "defined base sequence.",
    seconds=20)

add(MBI, "Lac operon", "Basic", "direct",
    "In the lac operon of E. coli, the inducer that switches on the operon is:",
    P("Lactose", ["Glucose", "The repressor protein", "β-galactosidase"], "D"),
    "Inducible lac operon",
    "Lactose is the substrate for β-galactosidase and it regulates switching on and off of the operon; hence it is "
    "termed the inducer. In its presence the repressor is inactivated by interaction with the inducer, so RNA "
    "polymerase can transcribe the operon.",
    ["Substrate that inactivates the repressor → inducer → lactose"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Glucose is not the lac inducer; the repressor (from the i gene) is what the inducer inactivates; "
        "β-galactosidase is the z gene product that hydrolyses lactose.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Intermediate", "numerical",
    "A double-stranded DNA molecule has 5 × 10⁶ base pairs. Taking the distance between two consecutive base pairs "
    "as 0.34 nm, what is the length of this DNA molecule?",
    P("1.7 mm", ["0.85 mm", "3.4 mm", "17 mm"], "B"),
    "Length of DNA from base pairs",
    "Length = number of base pairs × distance between consecutive base pairs. The two strands run side by side, so "
    "the length depends on the number of base pairs, not on the number of nucleotides.",
    ["Length = 5 × 10⁶ × 0.34 × 10⁻⁹ m", "= 1.7 × 10⁻³ m = 1.7 mm"],
    C12_MB("structure of polynucleotide chain: double helix"),
    why="0.85 mm divides by 2, as if the two strands shared the length; 3.4 mm multiplies by 2, as if the "
        "nucleotides of both strands were laid end to end; 17 mm is a power-of-ten slip in converting nm to mm.",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "DNA and RNA structure", "Intermediate", "statement_pair",
    sp("When the phosphate moiety at the 5'-end of the sugar is free in a polynucleotide chain, that end is referred "
       "to as the 5'-end of the chain.",
       "The backbone of a polynucleotide chain is formed by the nitrogenous bases, while the sugar and phosphate "
       "project outward from it."),
    SP("C"),
    "Polynucleotide chain",
    "A polynucleotide has a free phosphate at the 5'-end of the sugar (5'-end) and a free 3'-OH at the other end "
    "(3'-end). The backbone is formed by sugar and phosphates; the nitrogenous bases linked to the sugar project "
    "from the backbone.",
    ["Statement I: true", "Statement II: false, the sugar-phosphate chain is the backbone and bases project from it"],
    C12_MB("structure of polynucleotide chain"),
    seconds=35)

add(MBI, "DNA packaging", "Intermediate", "assertion_reason",
    ar("In eukaryotes, packaging of chromatin at a higher level requires an additional set of proteins called "
       "non-histone chromosomal (NHC) proteins.",
       "In prokaryotes such as E. coli, the negatively charged DNA is held with some positively charged proteins in "
       "a region termed the nucleoid."),
    AR("B"),
    "Packaging of DNA",
    "In eukaryotes, DNA is wrapped around histone octamers to form nucleosomes, which form chromatin fibres; "
    "higher-level packaging needs non-histone chromosomal proteins. Prokaryotes lack a defined nucleus; their DNA "
    "is held with some positively charged proteins in the nucleoid. R is a true statement about prokaryotes and "
    "says nothing about why eukaryotic chromatin needs NHC proteins.",
    ["A: true", "R: true", "R describes prokaryotic DNA, unrelated to eukaryotic higher-order packaging → B"],
    C12_MB("packaging of DNA helix"),
    seconds=40)

add(MBI, "Genetic code and translation", "Intermediate", "match_list",
    ml(("scientist", "contribution"),
       ["Har Gobind Khorana", "Marshall Nirenberg", "Severo Ochoa", "Francis Crick"],
       ["Chemical method for synthesising RNA molecules with defined combinations of bases",
        "Proposed the central dogma of molecular biology",
        "Enzyme (polynucleotide phosphorylase) that polymerises RNA with defined sequences without a template",
        "Cell-free system for protein synthesis that helped decipher the code"]),
    M({"A": "I", "B": "IV", "C": "III", "D": "II"},
      [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
       {"A": "III", "B": "IV", "C": "I", "D": "II"}], "A"),
    "Deciphering the genetic code",
    "Khorana's chemical method synthesised RNA molecules with defined combinations of bases (homopolymers and "
    "copolymers). Nirenberg's cell-free system for protein synthesis finally helped decipher the code. Ochoa's "
    "enzyme, polynucleotide phosphorylase, polymerised RNA with defined sequences in a template-independent manner. "
    "Crick proposed the central dogma (DNA → RNA → protein).",
    ["Khorana → A-I", "Nirenberg → B-IV", "Ochoa → C-III", "Crick → D-II"],
    C12_MB("genetic code; central dogma"),
    why="The wrong codes swap Khorana with Nirenberg, or Khorana with Ochoa (both made RNA of defined sequence, "
        "one chemically and one enzymatically).",
    seconds=45)

add(MBI, "Replication", "Intermediate", "multi_statement",
    ms("Which of the following statements about DNA replication are correct?",
       ["Deoxyribonucleoside triphosphates serve both as substrates and as a source of energy for polymerisation.",
        "In long DNA molecules, replication occurs within a small opening of the DNA helix called the replication "
        "fork.",
        "Replication can start at any random point in the DNA.",
        "In eukaryotes, DNA replication takes place in the S-phase of the cell cycle.",
        "A failure of cell division after DNA replication results in aneuploidy."]),
    P("(a), (b) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "C"),
    "Replication: enzymes, fork and timing",
    "dNTPs serve as substrates and provide energy. Because the two strands cannot be separated along their entire "
    "length (it needs too much energy), replication occurs within a small opening, the replication fork. "
    "Replication starts only at a definite region, the origin of replication. In eukaryotes it occurs in the "
    "S-phase, and a failure of cell division after DNA replication results in polyploidy.",
    ["(a) True", "(b) True", "(c) False: replication begins at the origin of replication", "(d) True",
     "(e) False: it results in polyploidy"],
    C12_MB("replication: the machinery and the enzymes"),
    why="Options A, B and D include (c) or (e).",
    seconds=50)

add(MBI, "Transcription", "Intermediate", "direct",
    "In eukaryotes, the heterogeneous nuclear RNA (hnRNA), the precursor of mRNA, is transcribed by:",
    P("RNA polymerase II", ["RNA polymerase I", "RNA polymerase III", "DNA polymerase"], "D"),
    "Eukaryotic RNA polymerases",
    "In the eukaryotic nucleus there are three RNA polymerases besides the one in organelles. RNA polymerase I "
    "transcribes rRNAs (28S, 18S and 5.8S); RNA polymerase III transcribes tRNA, 5S rRNA and snRNAs; RNA polymerase "
    "II transcribes the precursor of mRNA, hnRNA.",
    ["Pol I → 28S, 18S, 5.8S rRNA", "Pol II → hnRNA", "Pol III → tRNA, 5S rRNA, snRNA"],
    C12_MB("transcription in eukaryotes"),
    why="Pol I makes the larger rRNAs; Pol III makes tRNA, 5S rRNA and snRNAs; DNA polymerase replicates DNA.",
    seconds=25)

add(MBI, "Transcription", "Intermediate", "assertion_reason",
    ar("In eukaryotes, the structural genes are split: the coding sequences (exons) are interrupted by introns.",
       "Introns are the sequences that appear in the mature, processed RNA."),
    AR("C"),
    "Split genes, exons and introns",
    "Eukaryotic structural genes are split genes. Exons are the coding (expressed) sequences that appear in mature "
    "or processed RNA; introns (intervening sequences) do not appear in mature RNA because they are removed by "
    "splicing. So A is true and R, which says the opposite about introns, is false.",
    ["A: true", "R: false, exons appear in mature RNA; introns are spliced out"],
    C12_MB("transcription unit and the gene; transcription in eukaryotes"),
    seconds=35)

add(MBI, "Genetic code and translation", "Intermediate", "multi_statement",
    ms("Which of the following are features of the genetic code?",
       ["The codon is a triplet; 61 codons code for amino acids and 3 codons do not code for any amino acid.",
        "Some amino acids are coded by more than one codon; hence the code is degenerate.",
        "The codon is read in mRNA in a contiguous fashion; there are no punctuations.",
        "The code is absolutely universal, with no exceptions in any organism or organelle.",
        "The three codons that do not code for amino acids are recognised by specific tRNAs."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "B"),
    "Features of the genetic code",
    "The code is a triplet: 61 codons code for amino acids and 3 are stop codons. It is degenerate (some amino "
    "acids have more than one codon) and is read contiguously without punctuation. It is nearly universal: UUU "
    "codes for phenylalanine from bacteria to humans, but there are exceptions in mitochondrial codons and in some "
    "protozoans. There are no tRNAs for stop codons.",
    ["(a) True", "(b) True", "(c) True", "(d) False: nearly universal, with exceptions",
     "(e) False: there are no tRNAs for stop codons"],
    C12_MB("genetic code; translation"),
    why="Options B, C and D include (d) or (e).",
    seconds=50)

add(MBI, "Genetic code and translation", "Intermediate", "statement_pair",
    sp("Charging (aminoacylation) of tRNA, in which amino acids are activated and linked to their cognate tRNA, "
       "takes place in the presence of ATP.",
       "The ribosome consists of structural RNAs and about 80 different proteins."),
    SP("A"),
    "Translation: charging of tRNA and the ribosome",
    "In the first phase of translation, amino acids are activated in the presence of ATP and linked to their "
    "cognate tRNA (charging or aminoacylation of tRNA). The ribosome, the cellular factory for protein synthesis, "
    "consists of structural RNAs and about 80 different proteins.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("translation"),
    seconds=35)

add(MBI, "Lac operon", "Intermediate", "direct",
    "The lac operon of E. coli consists of one regulatory gene and three structural genes. The enzyme "
    "transacetylase is coded by:",
    P("The a gene", ["The z gene", "The y gene", "The i gene"], "A"),
    "Genes of the lac operon",
    "The lac operon has a regulatory gene i, which codes for the repressor, and three structural genes: z codes for "
    "β-galactosidase (hydrolyses lactose into galactose and glucose), y codes for permease (increases permeability "
    "of the cell to β-galactosides) and a codes for transacetylase.",
    ["i → repressor", "z → β-galactosidase", "y → permease", "a → transacetylase"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="z codes for β-galactosidase, y for permease and the regulatory gene i for the repressor.",
    seconds=25)

add(MBI, "DNA as genetic material", "Advanced", "direct",
    "Avery, MacLeod and McCarty treated the purified extract of heat-killed S-strain bacteria with different "
    "enzymes before mixing it with live R-strain bacteria. Which treatment inhibited transformation?",
    P("Digestion with DNase", ["Digestion with proteases", "Digestion with RNases",
                               "Digestion with both proteases and RNases"], "C"),
    "Biochemical nature of the transforming principle",
    "Avery, MacLeod and McCarty purified biochemicals (proteins, DNA, RNA) from heat-killed S cells. Protein-"
    "digesting enzymes (proteases) and RNA-digesting enzymes (RNases) did not affect transformation, so the "
    "transforming substance was neither protein nor RNA. Digestion with DNase did inhibit transformation, showing "
    "that DNA caused the transformation.",
    ["Proteases → transformation still occurs", "RNases → transformation still occurs",
     "DNase → transformation inhibited → DNA is the transforming principle"],
    C12_MB("the search for genetic material: biochemical characterisation of transforming principle"),
    why="Proteases and RNases, alone or together, left the DNA intact, so transformation still took place.",
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "multi_statement",
    ms("Which of the following statements about the Human Genome Project (HGP) are correct?",
       ["One of its goals was to identify all the approximately 20,000–25,000 genes in human DNA.",
        "One of its goals was to determine the sequences of the 3 billion chemical base pairs that make up human "
        "DNA.",
        "The HGP was closely associated with the rapid development of a new area of biology called bioinformatics.",
        "Chromosome 1 was the first human chromosome to be completely sequenced.",
        "Repeated sequences make up a very small portion of the human genome."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Human Genome Project",
    "The goals of the HGP included identifying all the approximately 20,000–25,000 genes and determining the "
    "sequences of the 3 billion base pairs of human DNA. The project was closely associated with the rapid "
    "development of bioinformatics. The sequence of chromosome 1 was completed only in May 2006, the last of the 24 "
    "human chromosomes. Repeated sequences make up a very large portion of the genome.",
    ["(a) True", "(b) True", "(c) True", "(d) False: chromosome 1 was the last to be completed (May 2006)",
     "(e) False: repeated sequences form a very large portion"],
    C12_MB("human genome project"),
    why="Options A, B and C include (d) or (e). (d) is the trap: chromosome 1 has the most genes, but it was the "
        "last to be sequenced.",
    seconds=55)

add(MBI, "Lac operon", "Advanced", "assertion_reason",
    ar("A very low level of expression of the lac operon has to be present in the cell all the time.",
       "Permease, a product of the lac operon, increases the permeability of the cell to β-galactosides; without "
       "it, lactose cannot enter the cell."),
    AR("A"),
    "Basal expression of the lac operon",
    "Lactose must enter the cell before it can act as an inducer. Its entry depends on permease (y gene product), "
    "which is itself made by the lac operon. So a very low level of expression has to be present all the time; "
    "otherwise lactose could never get in to induce the operon. R gives this reason.",
    ["A: true", "R: true", "No permease → no lactose entry → no induction; so basal expression is needed → R "
     "explains A"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=45)

add(MBI, "DNA as genetic material", "Advanced", "statement_pair",
    sp("RNA was the first genetic material, and there is evidence that essential life processes such as metabolism, "
       "translation and splicing evolved around RNA.",
       "Because RNA is more stable than DNA, RNA is preferred for the storage of genetic information."),
    SP("C"),
    "RNA world and the choice of DNA",
    "RNA was the first genetic material and acted as both genetic material and catalyst. Being a catalyst it was "
    "reactive and unstable, so DNA evolved from RNA with chemical modifications that make it more stable. DNA, "
    "being more stable, is preferred for storage of genetic information; RNA is better for its transmission.",
    ["Statement I: true", "Statement II: false, DNA is more stable and is preferred for storage"],
    C12_MB("RNA world; properties of genetic material"),
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "match_list",
    ml(("term", "description"),
       ["Variable number of tandem repeats (VNTR)", "Single nucleotide polymorphisms (SNPs)",
        "Expressed sequence tags (ESTs)", "BAC and YAC"],
       ["Vectors used to clone DNA fragments for sequencing in the HGP",
        "Satellite DNA used by Jeffreys as a probe, showing a very high degree of polymorphism",
        "Single-base DNA differences, found at about 1.4 million locations in humans",
        "Approach of identifying all the genes that are expressed as RNA"]),
    M({"A": "II", "B": "III", "C": "IV", "D": "I"},
      [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
       {"A": "IV", "B": "III", "C": "II", "D": "I"}], "B"),
    "HGP methods and DNA fingerprinting terms",
    "Jeffreys used a satellite DNA showing high polymorphism, VNTR, as a probe. SNPs are single-base DNA "
    "differences, identified at about 1.4 million locations. ESTs are used to identify all the genes expressed as "
    "RNA. In the HGP, DNA fragments were cloned in bacterial artificial chromosomes (BAC) and yeast artificial "
    "chromosomes (YAC).",
    ["VNTR → A-II", "SNP → B-III", "EST → C-IV", "BAC and YAC → D-I"],
    C12_MB("human genome project; DNA fingerprinting"),
    why="The wrong codes swap the two kinds of DNA variation (VNTR and SNP), or ESTs with the cloning vectors.",
    seconds=50)

add(MBI, "Genetic code and translation", "Advanced", "direct",
    "Within the coding region of a gene, the three base pairs that make up one complete codon are deleted. What is the most likely effect "
    "on the encoded protein?",
    P("One amino acid is deleted, and the reading frame remains unaltered from that point onwards",
      ["The reading frame shifts, so every codon after the deletion is read differently",
       "Translation cannot begin because the initiator codon is lost",
       "The protein becomes three amino acids shorter"], "A"),
    "Mutations and the genetic code",
    "The code is read in triplets without punctuation. Insertion or deletion of one or two bases shifts the "
    "reading frame (frameshift). Insertion or deletion of three bases, or a multiple of three, inserts or deletes "
    "one or more codons, and hence one or more amino acids, and the reading frame remains unaltered from that point "
    "onwards.",
    ["3 bases = 1 codon", "Deleting three bases → one codon, hence one amino acid, fewer",
     "Frame after the deletion is unchanged"],
    C12_MB("mutations and genetic code"),
    why="A frameshift needs deletion of one or two bases (not a multiple of three). The deletion is within the gene, "
        "not at the start codon. Three bases make one codon, so only one amino acid is lost, not three.",
    seconds=45)

add(MBI, "Genetic code and translation", "Advanced", "multi_statement",
    ms("Which of the following statements about translation are correct?",
       ["For initiation, the ribosome binds to the mRNA at the start codon (AUG), which is recognised only by the "
        "initiator tRNA.",
        "During elongation, complexes of an amino acid linked to tRNA sequentially bind to the appropriate codons "
        "in mRNA.",
        "At the end, a release factor binds to the stop codon, terminating translation and releasing the complete "
        "polypeptide.",
        "There are two sites in the large subunit of the ribosome where subsequent amino acids bind, close enough to "
        "form a peptide bond.",
        "There are specific tRNAs for each of the stop codons."]),
    P("(a), (b), (c) and (d) only",
      ["(a), (b) and (e) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"], "C"),
    "Steps of translation",
    "Translation starts when the ribosome binds the mRNA at AUG, recognised only by the initiator tRNA. In "
    "elongation, aminoacyl-tRNA complexes bind in sequence by base pairing of anticodon and codon; the large "
    "subunit has two sites where successive amino acids bind close enough to form a peptide bond. At the end, a "
    "release factor binds to the stop codon. There are no tRNAs for stop codons.",
    ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: there are no tRNAs for stop codons"],
    C12_MB("tRNA the adapter molecule; translation"),
    why="Options A, B and D include (e); option D also leaves out true statements.",
    seconds=55)

# ================================================================ Microbes in Human Welfare (2 / 3 / 2)
C12_MH = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "direct",
    "'Toddy', a traditional drink of some parts of southern India, is made by:",
    P("Fermenting sap from palms", ["Distilling fermented barley malt", "Fermenting milk with lactic acid bacteria",
                                    "Fermenting rice dough with bacteria"], "B"),
    "Microbes in household products",
    "Toddy, a traditional drink of some parts of southern India, is made by fermenting sap from palms with "
    "microbes.",
    ["Toddy → fermentation of palm sap"],
    C12_MH("microbes in household products"),
    why="Distilled malt drinks are whisky-type beverages; milk fermented by LAB gives curd; fermented rice-based "
        "dough is used for idli and dosa.",
    seconds=20)

add(MHW, "Biogas", "Basic", "direct",
    "The technology of biogas production in India was developed mainly due to the efforts of:",
    P("IARI and KVIC", ["ICAR and CSIR", "NBPGR and IARI", "WHO and FAO"], "C"),
    "Biogas in India",
    "The technology of biogas production was developed in India mainly due to the efforts of the Indian "
    "Agricultural Research Institute (IARI) and the Khadi and Village Industries Commission (KVIC). Biogas plants "
    "are more often built in rural areas, where cattle dung is available in large quantities.",
    ["Biogas technology in India → IARI and KVIC"],
    C12_MH("microbes in production of biogas"),
    why="NCERT credits only IARI and KVIC; the other bodies are not named for biogas technology.",
    seconds=20)

add(MHW, "Household and industrial products", "Intermediate", "match_list",
    ml(("microbe or microbial product", "use"),
       ["Lipases", "Pectinases and proteases", "Penicillium notatum", "Saccharomyces cerevisiae"],
       ["Commercial production of ethanol", "Clarifying bottled fruit juices",
        "Removing oily stains from laundry in detergent formulations",
        "Mould that yielded the first antibiotic, discovered by Alexander Fleming"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "D"),
    "Microbes in industrial products",
    "Lipases are used in detergent formulations to remove oily stains. Bottled fruit juices are made clearer using "
    "pectinases and proteases. Penicillin, the first antibiotic, was discovered by Alexander Fleming in the mould "
    "Penicillium notatum while working on Staphylococci. Saccharomyces cerevisiae (brewer's yeast) is used for "
    "bread-making and the commercial production of ethanol.",
    ["Lipases → A-III", "Pectinases and proteases → B-II", "Penicillium notatum → C-IV",
     "Saccharomyces cerevisiae → D-I"],
    C12_MH("microbes in industrial products"),
    why="The wrong codes swap the two enzyme uses, or the mould and the yeast.",
    seconds=45)

add(MHW, "Sewage treatment", "Intermediate", "statement_pair",
    sp("Primary treatment of sewage involves physical removal of particles, large and small, through filtration and "
       "sedimentation.",
       "In secondary treatment, the major part of the activated sludge is pumped back into the aeration tank to "
       "serve as the inoculum."),
    SP("C"),
    "Sewage treatment",
    "Primary treatment is physical: floating debris is removed by sequential filtration and grit by sedimentation. "
    "After secondary (biological) treatment in aeration tanks, the effluent passes to a settling tank where the "
    "bacterial flocs settle as activated sludge. Only a small part of the activated sludge is pumped back as "
    "inoculum; the remaining major part goes to anaerobic sludge digesters.",
    ["Statement I: true", "Statement II: false, only a small part is returned as inoculum; the major part goes to "
     "anaerobic sludge digesters"],
    C12_MH("microbes in sewage treatment"),
    why="Statement II swaps 'small part' and 'major part'; that swap is the trap.",
    seconds=40)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "assertion_reason",
    ar("An organic farmer prefers to keep both pests and their predators at manageable levels rather than "
       "eradicate the pests completely.",
       "Without the pests, the beneficial predatory and parasitic insects that depend on them as food or hosts "
       "would not be able to survive."),
    AR("A"),
    "Biocontrol and the organic farmer's view",
    "The organic farmer works to create a system where insects that are sometimes called pests are not eradicated "
    "but kept at manageable levels by a complex system of checks and balances. Eradicating the pests is undesirable "
    "because the beneficial predators and parasites that depend on them as food or hosts would then not survive. R "
    "is the reason for A.",
    ["A: true", "R: true", "Pest eradication would remove the food or hosts of beneficial insects → R explains A"],
    C12_MH("microbes as biocontrol agents"),
    seconds=40)

add(MHW, "Biogas", "Advanced", "multi_statement",
    ms("Which of the following statements about biogas and methanogens are correct?",
       ["Biogas is a mixture of gases, predominantly methane, produced by microbial activity.",
        "Methanogens are present in the rumen of cattle, where they help in the breakdown of cellulose.",
        "Cattle excreta (gobar) is rich in methanogenic bacteria.",
        "The spent slurry removed from a biogas plant can be used as fertiliser.",
        "Methanogens grow aerobically on cellulosic material."]),
    P("(a), (b), (c) and (d) only",
      ["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only"], "B"),
    "Biogas production",
    "Biogas is a mixture of gases, predominantly methane, produced by microbial activity. Methanogens, such as "
    "Methanobacterium, grow anaerobically on cellulosic material. They are present in the rumen of cattle, where "
    "they help break down cellulose, and cattle dung (gobar) is rich in them. In a biogas plant the slurry of dung "
    "is fermented; the gas is collected under a floating cover and the spent slurry can be used as fertiliser.",
    ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: methanogens grow anaerobically"],
    C12_MH("microbes in production of biogas"),
    why="Options A and C include (e); option D leaves out the true statement (b).",
    seconds=50)

add(MHW, "Household and industrial products", "Advanced", "direct",
    "Which one of the following statements is correct?",
    P("The 'Roquefort cheese' is ripened by growing a specific fungus on it, which gives it a particular flavour",
      ["The dough used for dosa and idli is fermented by fungi",
       "The full potential of penicillin as an effective antibiotic was established by Alexander Fleming alone",
       "Baker's yeast, used to ferment bread dough, is a bacterium"], "A"),
    "Microbes in food and medicine",
    "Roquefort cheese is ripened by growing specific fungi on it, which give it a particular flavour. The dough for "
    "dosa and idli is fermented by bacteria. Fleming discovered penicillin, but its full potential as an antibiotic "
    "was established later by Ernest Chain and Howard Florey. Baker's yeast, Saccharomyces cerevisiae, is a fungus.",
    ["Roquefort cheese → fungal ripening → correct", "Idli/dosa dough → bacteria",
     "Penicillin's potential → Chain and Florey", "Baker's yeast → fungus"],
    C12_MH("microbes in household products; antibiotics"),
    why="Each wrong option changes the organism or the scientist named by NCERT.",
    seconds=45)

# ================================================================ Organisms and Populations (4 / 5 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population attributes", "Basic", "direct",
    "The number of births during a given period in a population that are added to the initial density is called:",
    P("Natality", ["Mortality", "Immigration", "Carrying capacity"], "D"),
    "Population density changes",
    "Population density changes through four basic processes. Natality is the number of births during a given "
    "period that are added to the initial density; mortality is the number of deaths; immigration and emigration "
    "are individuals coming in and leaving.",
    ["Births added to the density → natality"],
    C12_OP("population attributes; population growth"),
    why="Mortality is deaths; immigration is individuals arriving from elsewhere; carrying capacity is the maximum "
        "population a habitat can support.",
    seconds=20)

add(OAP, "Population attributes", "Basic", "statement_pair",
    sp("Natality refers to the number of deaths in a population during a given period.",
       "Emigration is the number of individuals of the same species that have come into the habitat from elsewhere "
       "during the time period under consideration."),
    SP("B"),
    "Natality and emigration",
    "Natality is the number of births during a given period, and mortality the number of deaths. Emigration is the "
    "number of individuals of the population who left the habitat and went elsewhere; individuals coming into the "
    "habitat from elsewhere constitute immigration.",
    ["Statement I: false, it defines mortality", "Statement II: false, it defines immigration"],
    C12_OP("population growth"),
    seconds=30)

add(OAP, "Population growth", "Basic", "direct",
    "In the exponential growth equation dN/dt = rN, the symbol r stands for the:",
    P("Intrinsic rate of natural increase", ["Carrying capacity", "Total birth rate only",
                                             "Population density"], "B"),
    "Exponential growth",
    "When resources are unlimited, a population grows exponentially: dN/dt = (b − d) × N; with (b − d) = r, "
    "dN/dt = rN. Here r is the intrinsic rate of natural increase, an important parameter for assessing the impact "
    "of biotic or abiotic factors on population growth.",
    ["r = b − d = intrinsic rate of natural increase"],
    C12_OP("population growth: exponential growth"),
    why="Carrying capacity is K in the logistic equation; r is birth rate minus death rate, not birth rate alone; "
        "N is the population density.",
    seconds=20)

add(OAP, "Population interactions", "Basic", "direct",
    "Mycorrhizae, the associations between fungi and the roots of higher plants, are an example of:",
    P("Mutualism", ["Commensalism", "Parasitism", "Amensalism"], "C"),
    "Mutualism",
    "In mycorrhizae the fungi help the plant in the absorption of essential nutrients from the soil, while the plant "
    "provides the fungi with energy-yielding carbohydrates. Both partners benefit, so it is mutualism.",
    ["Fungus → helps nutrient absorption", "Plant → gives carbohydrates", "Both benefit → mutualism"],
    C12_OP("population interactions: mutualism"),
    why="In commensalism only one partner benefits; in parasitism one is harmed; in amensalism one is harmed and "
        "the other unaffected.",
    seconds=20)

add(OAP, "Population growth", "Intermediate", "numerical",
    "A pond has 500 frogs at the start of a year. During the year, 80 frogs are born, 30 frogs arrive from nearby "
    "ponds, 50 frogs die and 20 frogs leave for other ponds. Using N(t+1) = N(t) + [(B + I) − (D + E)], the "
    "population at the end of the year is:",
    P("540", ["520", "530", "680"], "A"),
    "Change in population density",
    "Births (B) and immigration (I) add to the density; deaths (D) and emigration (E) reduce it.",
    ["B + I = 80 + 30 = 110", "D + E = 50 + 20 = 70", "N(t+1) = 500 + 110 − 70 = 540"],
    C12_OP("population growth"),
    why="520 swaps immigration and emigration. 530 ignores migration altogether. 680 adds deaths and emigrants "
        "instead of subtracting them.",
    seconds=45, verified_by=RECOMPUTED)

add(OAP, "Population growth", "Intermediate", "assertion_reason",
    ar("The logistic growth model is considered a more realistic model of population growth than the exponential "
       "model.",
       "The resources available for the growth of most animal populations are unlimited."),
    AR("C"),
    "Logistic growth",
    "No population in nature has unlimited resources at its disposal. Since resources for growth for most animal "
    "populations are finite and become limiting sooner or later, the logistic (Verhulst-Pearl) model, which "
    "includes the carrying capacity K, is considered more realistic. R states the opposite and is false.",
    ["A: true", "R: false, resources are finite and become limiting sooner or later"],
    C12_OP("population growth: logistic growth"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "match_list",
    ml(("interaction", "effect on the two species"),
       ["Mutualism", "Competition", "Parasitism", "Amensalism"],
       ["One species is harmed and the other is unaffected", "Both species benefit", "Both species lose",
        "One species benefits and the other is harmed"]),
    M({"A": "II", "B": "III", "C": "IV", "D": "I"},
      [{"A": "II", "B": "I", "C": "IV", "D": "III"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
       {"A": "II", "B": "III", "C": "I", "D": "IV"}], "B"),
    "Types of population interactions",
    "Both species benefit in mutualism and both lose in competition. In parasitism and predation one species "
    "benefits and the interaction is detrimental to the other. In commensalism one benefits and the other is "
    "neither benefited nor harmed, while in amensalism one species is harmed and the other is unaffected.",
    ["Mutualism (+, +) → A-II", "Competition (−, −) → B-III", "Parasitism (+, −) → C-IV",
     "Amensalism (−, 0) → D-I"],
    C12_OP("population interactions"),
    why="The wrong codes swap competition with amensalism (both involve harm), or mutualism with parasitism.",
    seconds=40)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("Calotropis growing in abandoned fields produces highly poisonous cardiac glycosides and is therefore heavily "
       "browsed by cattle and goats.",
       "Thorns, as in Acacia and cactus, are the most common morphological means of defence in plants against "
       "herbivores."),
    SP("D"),
    "Plant defences against herbivores",
    "Plants cannot run away from predators, so they have evolved morphological and chemical defences. Thorns of "
    "Acacia and cactus are the most common morphological defence. Calotropis produces highly poisonous cardiac "
    "glycosides, and that is why cattle or goats are never seen browsing on it.",
    ["Statement I: false, the glycosides keep cattle and goats away", "Statement II: true"],
    C12_OP("population interactions: predation"),
    seconds=35)

add(OAP, "Population attributes", "Intermediate", "multi_statement",
    ms("Which of the following statements about population attributes are correct?",
       ["A population at any given time is composed of individuals of different ages.",
        "Age pyramids of human populations generally show the age distribution of females only.",
        "Sex ratio, such as 60 per cent females and 40 per cent males, is an attribute of a population.",
        "An individual organism has a birth rate and a death rate.",
        "Birth rates and death rates are expressed as per capita births and deaths."]),
    P("(a), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(c), (d) and (e) only", "(a), (b) and (d) only"], "D"),
    "Population attributes",
    "A population has attributes that an individual does not. An individual may be born or die, but a population "
    "has birth rates and death rates, expressed per capita (per member of the population). A population also has "
    "a sex ratio and an age distribution; plotted, the age distribution gives an age pyramid, which for humans "
    "shows males and females in a combined diagram.",
    ["(a) True", "(b) False: human age pyramids show males and females together", "(c) True",
     "(d) False: rates belong to populations, not individuals", "(e) True"],
    C12_OP("population attributes"),
    why="Options A, B and C include (b) or (d).",
    seconds=50)

add(OAP, "Population growth", "Advanced", "numerical",
    "A population follows logistic growth, dN/dt = rN[(K − N)/K], with r = 0.2 per year and carrying capacity "
    "K = 1000. What is its growth rate when N = 250?",
    P("37.5 individuals per year", ["50 individuals per year", "12.5 individuals per year",
                                    "150 individuals per year"], "C"),
    "Logistic (Verhulst-Pearl) growth",
    "Substitute into the logistic equation. The factor (K − N)/K is the fraction of the carrying capacity still "
    "unused, which slows growth compared with the exponential rate rN.",
    ["rN = 0.2 × 250 = 50", "(K − N)/K = 750/1000 = 0.75", "dN/dt = 50 × 0.75 = 37.5 per year"],
    C12_OP("population growth: logistic growth"),
    why="50 is the exponential rate rN without the resistance factor. 12.5 uses N/K instead of (K − N)/K. 150 "
        "multiplies r by (K − N) and forgets N/K.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    ms("Which of the following statements about population interactions are correct?",
       ["Predators in nature are 'prudent': a predator that overexploits its prey could drive the prey extinct and "
        "then become extinct itself for lack of food.",
        "Some species of insects and frogs are cryptically coloured (camouflaged) to avoid being detected easily by "
        "predators.",
        "Nearly 25 per cent of all insects are known to be phytophagous (feeding on plant sap and other parts of "
        "plants).",
        "Competition occurs only between closely related species.",
        "Interspecific competition can occur only when the shared resource is limiting."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "B"),
    "Predation and competition",
    "Prudent predation, camouflage of prey and the 25% figure for phytophagous insects are NCERT statements. "
    "Totally unrelated species can also compete, e.g. flamingoes and resident fishes compete for zooplankton in "
    "some shallow South American lakes. Resources need not be limiting: in interference competition the feeding "
    "efficiency of one species may be reduced by the inhibitory presence of the other even when resources are "
    "abundant.",
    ["(a) True", "(b) True", "(c) True", "(d) False: unrelated species also compete",
     "(e) False: competition can occur even with abundant resources (interference)"],
    C12_OP("population interactions: predation and competition"),
    why="Options A, C and D include (d) or (e).",
    seconds=55)

add(OAP, "Population interactions", "Advanced", "assertion_reason",
    ar("A given fig species can be pollinated by several different wasp species.",
       "The female fig wasp uses the fig fruit as an oviposition site and uses the developing seeds within the fruit "
       "to nourish its larvae."),
    AR("D"),
    "Fig and wasp mutualism",
    "Many fig species have tight one-to-one relationships with their pollinator wasp species: a given fig species "
    "can be pollinated only by its 'partner' wasp species and no other. The female wasp pollinates the fig "
    "inflorescence while searching for egg-laying sites, and in return uses the fruit as an oviposition site and "
    "the developing seeds to nourish her larvae.",
    ["A: false, each fig species is pollinated only by its partner wasp species", "R: true"],
    C12_OP("population interactions: mutualism"),
    seconds=40)

add(OAP, "Population attributes", "Advanced", "direct",
    "An area has 200 Parthenium plants and only one huge banyan tree with a large canopy. Saying that the banyan's "
    "population density is low relative to Parthenium underestimates the banyan's enormous role in the community. "
    "In such a case, a more meaningful measure of population size is:",
    P("Percent cover or biomass", ["The absolute number of individuals",
                                   "The number of fruits counted per tree in a week",
                                   "The birth rate of each species"], "A"),
    "Measuring population density",
    "Total number is generally the most appropriate measure of population density, but in some cases it is "
    "meaningless or hard to determine. Where one banyan tree dominates the community, counting individuals hides its "
    "role; percent cover or biomass is a more meaningful measure of population size.",
    ["Numbers mislead when individuals differ hugely in size", "Use percent cover or biomass instead"],
    C12_OP("population attributes"),
    why="Counting individuals is exactly what underestimates the banyan. Fruit counts and birth rate do not express "
        "the size of the population's presence in the community.",
    seconds=40)

# ================================================================ Ecosystem (3 / 5 / 3)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "The annual net primary productivity of the whole biosphere is approximately:",
    P("170 billion tons (dry weight) of organic matter", ["55 billion tons (dry weight) of organic matter",
                                                           "17 billion tons (dry weight) of organic matter",
                                                           "1,700 billion tons (dry weight) of organic matter"], "B"),
    "Primary productivity of the biosphere",
    "The annual net primary productivity of the whole biosphere is approximately 170 billion tons (dry weight) of "
    "organic matter. Of this, despite occupying about 70 per cent of the surface, the oceans contribute only 55 "
    "billion tons.",
    ["Whole biosphere → about 170 billion tons per year", "Oceans → only 55 billion tons of this"],
    C12_EC("productivity"),
    why="55 billion tons is the oceans' share only; the other two values are off by a factor of ten.",
    seconds=25)

add(ECO, "Structure and components", "Basic", "direct",
    "In a forest, trees occupy the top vertical layer, shrubs the second, and herbs and grasses the bottom layers. "
    "This vertical distribution of different species occupying different levels is called:",
    P("Stratification", ["Succession", "Standing crop", "Ecological pyramid"], "A"),
    "Structure of an ecosystem",
    "Interaction of biotic and abiotic components results in a physical structure characteristic of each type of "
    "ecosystem. Species composition and stratification are its important structural features. The vertical "
    "distribution of different species occupying different levels is called stratification.",
    ["Vertical layering of species: trees, shrubs, herbs and grasses → stratification"],
    C12_EC("ecosystem: structure and function"),
    why="Succession is a change in community over time; standing crop is the living mass at a trophic level; an "
        "ecological pyramid shows relations between trophic levels.",
    seconds=20)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "To compare the productivity of different ecosystems, primary productivity is expressed in units of:",
    P("g m⁻² yr⁻¹ or (kcal m⁻²) yr⁻¹", ["kcal only, without reference to area or time", "g per individual plant",
                                        "Number of plants per m²"], "D"),
    "Units of productivity",
    "Primary production is the amount of biomass or organic matter produced per unit area over a time period by "
    "plants during photosynthesis. It is expressed in weight (g m⁻²) or energy (kcal m⁻²). The rate of biomass "
    "production is productivity, expressed as g m⁻² yr⁻¹ or (kcal m⁻²) yr⁻¹ so that different ecosystems can be "
    "compared.",
    ["Productivity is a rate → needs area and time", "Units: g m⁻² yr⁻¹ or (kcal m⁻²) yr⁻¹"],
    C12_EC("productivity"),
    why="Productivity must be per unit area and per unit time; the other units leave out one or both, or measure "
        "number rather than biomass.",
    seconds=25)

add(ECO, "Productivity and decomposition", "Intermediate", "statement_pair",
    sp("Primary productivity depends on the plant species inhabiting an area, environmental factors, availability "
       "of nutrients and the photosynthetic capacity of plants.",
       "The oceans, which occupy about 70 per cent of the earth's surface, contribute more than half of the "
       "biosphere's annual net primary productivity."),
    SP("C"),
    "Factors and distribution of primary productivity",
    "Primary productivity depends on the plant species of an area, a variety of environmental factors, availability "
    "of nutrients and the photosynthetic capacity of plants, so it varies between ecosystems. Of the biosphere's "
    "annual NPP of about 170 billion tons, the oceans contribute only 55 billion tons, about one-third, despite "
    "occupying about 70 per cent of the surface.",
    ["Statement I: true", "Statement II: false, 55 of 170 billion tons is less than one-third"],
    C12_EC("productivity"),
    seconds=40)

add(ECO, "Productivity and decomposition", "Intermediate", "assertion_reason",
    ar("Decomposition is largely an anaerobic process.",
       "The rate of decomposition is controlled by the chemical composition of the detritus and by climatic "
       "factors."),
    AR("D"),
    "Decomposition",
    "Decomposition is largely an oxygen-requiring process, so A is false (anaerobiosis actually inhibits it). Its "
    "rate is controlled by the chemical composition of the detritus and by climatic factors such as temperature "
    "and soil moisture, so R is true.",
    ["A: false, decomposition is largely oxygen-requiring", "R: true"],
    C12_EC("decomposition"),
    seconds=35)

add(ECO, "Energy flow", "Intermediate", "match_list",
    ml(("organism in the food chain phytoplankton → zooplankton → small fish → fish-eating bird", "role"),
       ["Phytoplankton", "Zooplankton", "Small fish", "Fish-eating bird"],
       ["Secondary consumer", "Producer", "Tertiary consumer", "Primary consumer"]),
    M({"A": "II", "B": "IV", "C": "I", "D": "III"},
      [{"A": "II", "B": "I", "C": "IV", "D": "III"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
       {"A": "II", "B": "IV", "C": "III", "D": "I"}], "C"),
    "Trophic levels",
    "Producers occupy the first trophic level. Animals that feed on producers (herbivores) are primary consumers; "
    "those that eat primary consumers are secondary consumers; those that eat secondary consumers are tertiary "
    "consumers.",
    ["Phytoplankton → producer (A-II)", "Zooplankton → primary consumer (B-IV)",
     "Small fish → secondary consumer (C-I)", "Fish-eating bird → tertiary consumer (D-III)"],
    C12_EC("energy flow"),
    why="The wrong codes shift one organism by a trophic level or treat zooplankton as producers.",
    seconds=40)

add(ECO, "Energy flow", "Intermediate", "multi_statement",
    ms("Which of the following statements are correct?",
       ["In the grazing food chain grass → goat → man, the goat is a secondary consumer.",
        "The amount of energy decreases at successive trophic levels.",
        "Decomposers secrete digestive enzymes that break down dead and waste materials into simple inorganic "
        "materials, which they then absorb.",
        "Animals such as cockroaches and crows are omnivores.",
        "Decomposers are also known as autotrophs."]),
    P("(b), (c) and (d) only",
      ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"], "B"),
    "Food chains and decomposers",
    "In grass → goat → man, grass is the producer and the goat, a herbivore, is the primary consumer. Energy "
    "decreases at successive trophic levels. Decomposers (saprotrophs) are heterotrophs that secrete digestive "
    "enzymes, break down dead matter into simple inorganic materials and absorb them. Cockroaches and crows are "
    "omnivores.",
    ["(a) False: the goat is a primary consumer", "(b) True", "(c) True", "(d) True",
     "(e) False: decomposers are saprotrophs (heterotrophs)"],
    C12_EC("energy flow"),
    why="Options A, C and D include (a) or (e).",
    seconds=50)

add(ECO, "Productivity and decomposition", "Intermediate", "direct",
    "Which of the following is NOT a part of detritus, the raw material for decomposition?",
    P("Roots of living grass plants", ["Dead leaves and bark", "Fallen flowers", "Fecal matter of animals"], "D"),
    "Detritus",
    "Dead plant remains such as leaves, bark and flowers, and dead remains of animals including fecal matter, "
    "constitute detritus, the raw material for decomposition. Living plant parts are not detritus.",
    ["Detritus = dead plant remains + dead animal remains, including fecal matter", "Living roots → not detritus"],
    C12_EC("decomposition"),
    why="Dead leaves, bark, fallen flowers and fecal matter are all listed by NCERT as detritus.",
    seconds=25)

add(ECO, "Productivity and decomposition", "Advanced", "statement_pair",
    sp("The steps of decomposition, such as fragmentation, leaching and catabolism, operate simultaneously on the "
       "detritus.",
       "The release of inorganic nutrients when humus is further degraded by some microbes is called "
       "mineralisation."),
    SP("A"),
    "Steps of decomposition",
    "Decomposition involves fragmentation, leaching, catabolism, humification and mineralisation. Although listed "
    "one after another, all these steps operate simultaneously on the detritus. Humus is highly resistant to "
    "microbial action and is degraded very slowly; when some microbes further degrade it, inorganic nutrients are "
    "released (mineralisation).",
    ["Statement I: true, NCERT stresses that the steps operate simultaneously", "Statement II: true"],
    C12_EC("decomposition"),
    why="Students who think the steps must occur strictly one after another mark Statement I false; NCERT states "
        "they operate simultaneously.",
    seconds=40)

add(ECO, "Structure and components", "Advanced", "multi_statement",
    ms("Which of the following statements about ecosystems are correct?",
       ["An ecosystem is a functional unit of nature in which living organisms interact among themselves and with "
        "the surrounding physical environment.",
        "Ecosystems vary greatly in size, from a small pond to a large forest or a sea.",
        "Forest, grassland and desert are examples of man-made ecosystems.",
        "Many ecologists regard the entire biosphere as a global ecosystem.",
        "The rate of function of a pond community is not affected by solar input, temperature or day-length."]),
    P("(a), (b) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "A"),
    "Ecosystem: concept and structure",
    "An ecosystem is a functional unit of nature, varying in size from a pond to a sea; many ecologists regard "
    "the whole biosphere as a global ecosystem. Forest, grassland and desert are terrestrial (natural) ecosystems; "
    "crop fields and aquaria are man-made. In a pond, solar input, the cycle of temperature, day-length and other "
    "climatic conditions regulate the rate of function of the entire pond.",
    ["(a) True", "(b) True", "(c) False: these are natural terrestrial ecosystems", "(d) True",
     "(e) False: climatic conditions regulate the pond's rate of function"],
    C12_EC("ecosystem: structure and function"),
    why="Options B, C and D include (c) or (e).",
    seconds=50)

add(ECO, "Ecological pyramids", "Advanced", "statement_pair",
    sp("In most ecosystems, the pyramids of number, energy and biomass are all inverted.",
       "To construct a pyramid of biomass, it is enough to take only a few representative individuals of each "
       "trophic level into account."),
    SP("B"),
    "Ecological pyramids",
    "In most ecosystems all three pyramids (number, energy and biomass) are upright: producers are more in number "
    "and biomass than herbivores, and herbivores more than carnivores; energy at a lower level is always more than "
    "at a higher level. In any calculation of energy content, biomass or numbers, all organisms at that trophic "
    "level must be included; generalisations based on a few individuals will not be true.",
    ["Statement I: false, they are upright in most ecosystems (the sea's biomass pyramid is an exception)",
     "Statement II: false, all organisms at the trophic level must be included"],
    C12_EC("ecological pyramids"),
    seconds=40)

# ================================================================ Biodiversity and Conservation (4 / 5 / 4)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "The term 'biodiversity' was popularised by the sociobiologist:",
    P("Edward Wilson", ["Robert May", "Paul Ehrlich", "David Tilman"], "C"),
    "Biodiversity",
    "Biodiversity is the term popularised by the sociobiologist Edward Wilson to describe the combined diversity "
    "at all the levels of biological organisation.",
    ["'Biodiversity' popularised by → Edward Wilson"],
    C12_BD("biodiversity"),
    why="Robert May estimated global species diversity; Paul Ehrlich proposed the rivet popper hypothesis; David "
        "Tilman studied diversity and stability in outdoor plots.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Basic", "statement_pair",
    sp("India has about 1,000 genetically different strains of rice.",
       "India has about 1,000 varieties of mango."),
    SP("D"),
    "Genetic diversity in India",
    "India has more than 50,000 genetically different strains of rice and 1,000 varieties of mango. Statement I "
    "applies the mango figure to rice.",
    ["Statement I: false, more than 50,000 strains of rice", "Statement II: true"],
    C12_BD("biodiversity: genetic diversity"),
    seconds=25)

add(BDC, "Hotspots and Red Data Book", "Basic", "direct",
    "Initially 25 biodiversity hotspots were identified, and more were added later. The total number of "
    "biodiversity hotspots in the world is now:",
    P("34", ["25", "12", "3"], "B"),
    "Biodiversity hotspots",
    "Initially 25 biodiversity hotspots were identified, but subsequently nine more were added, bringing the total "
    "number in the world to 34.",
    ["25 + 9 = 34 hotspots"],
    C12_BD("biodiversity conservation: hotspots"),
    why="25 was the initial number; 12 is the number of megadiversity countries; 3 is the number of hotspots that "
        "cover India's regions of high biodiversity.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "The IUCN Red List (2004) documents the extinction of how many species in the last 500 years?",
    P("784", ["338", "87", "27"], "D"),
    "Recorded extinctions",
    "The IUCN Red List (2004) documents the extinction of 784 species (including 338 vertebrates, 359 "
    "invertebrates and 87 plants) in the last 500 years.",
    ["Total extinctions in the last 500 years → 784", "Of these: 338 vertebrates, 359 invertebrates, 87 plants"],
    C12_BD("loss of biodiversity"),
    why="338 and 87 are the vertebrate and plant shares of the 784; 27 is the number of species lost in the last "
        "twenty years.",
    seconds=25)

add(BDC, "Patterns of biodiversity", "Intermediate", "match_list",
    ml(("concept", "NCERT example"),
       ["Genetic diversity", "Species diversity", "Ecological diversity", "Robert May's estimate"],
       ["India, with deserts, rain forests, mangroves, coral reefs, wetlands, estuaries and alpine meadows, has "
        "more of it than Norway",
        "Global species diversity of about 7 million",
        "Differences in potency and concentration of reserpine in Rauwolfia vomitoria from different Himalayan "
        "ranges",
        "The Western Ghats have a greater amphibian species diversity than the Eastern Ghats"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Levels of biodiversity",
    "Genetic diversity is variation within a species, such as the potency of reserpine in Rauwolfia vomitoria from "
    "different Himalayan ranges. Species diversity is diversity at the species level, as in the amphibians of the "
    "Western versus Eastern Ghats. Ecological diversity is diversity at the ecosystem level, greater in India than "
    "in Norway. Robert May placed global species diversity at about 7 million.",
    ["Genetic → A-III", "Species → B-IV", "Ecological → C-I", "Robert May → D-II"],
    C12_BD("biodiversity; how many species are there on earth"),
    why="The wrong codes swap genetic with species diversity, or species with ecological diversity.",
    seconds=50)

add(BDC, "Patterns of biodiversity", "Intermediate", "statement_pair",
    sp("More than 70 per cent of all the species recorded on earth are plants.",
       "Among animals, mammals are the most species-rich taxonomic group."),
    SP("B"),
    "Global species composition",
    "More than 70 per cent of all recorded species are animals, while plants (including algae, fungi, bryophytes, "
    "gymnosperms and angiosperms) make up no more than 22 per cent. Among animals, insects are the most "
    "species-rich group, making up more than 70 per cent of the total: 7 out of every 10 animals are insects.",
    ["Statement I: false, more than 70% are animals", "Statement II: false, insects are the most species-rich"],
    C12_BD("how many species are there on earth"),
    seconds=35)

add(BDC, "Importance and loss", "Intermediate", "assertion_reason",
    ar("The Amazon rain forest is so huge that it is called the 'lungs of the planet'.",
       "The Amazon rain forest is being cut and cleared for cultivating soya beans or for conversion to grasslands "
       "for raising beef cattle."),
    AR("B"),
    "Habitat loss in tropical rain forests",
    "NCERT says the Amazon rain forest is so huge that it is called the 'lungs of the planet', and that it is being "
    "cut and cleared for soya bean cultivation or for grasslands for beef cattle. Both are true, but the clearing "
    "of the forest is not why it got its name; the name comes from its huge size.",
    ["A: true", "R: true", "R describes the forest's destruction, not the reason for its name → B"],
    C12_BD("loss of biodiversity: habitat loss and fragmentation"),
    why="Option A is wrong because the reason for the name is the forest's huge size, which R does not mention.",
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "multi_statement",
    ms("Which of the following statements about the reasons for conserving biodiversity are correct?",
       ["Under the narrowly utilitarian argument, humans derive countless direct economic benefits from nature, "
        "such as food, firewood, fibre and construction material.",
        "More than 25 per cent of the drugs currently sold in the market worldwide are derived from plants.",
        "Bioprospecting means exploring molecular, genetic and species-level diversity for products of economic "
        "importance.",
        "The ethical argument holds that every species has an intrinsic value, even if it is not of current "
        "economic value to us.",
        "Pollination of plants by bees, birds and bats is the standard example of the narrowly utilitarian "
        "argument."]),
    P("(a), (b), (c) and (d) only",
      ["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"], "B"),
    "Why conserve biodiversity",
    "The narrowly utilitarian argument rests on direct economic benefits: food, firewood, fibre, construction "
    "material, industrial products and medicines (more than 25% of drugs sold worldwide come from plants). "
    "Bioprospecting explores biodiversity for products of economic importance. The broadly utilitarian argument "
    "covers ecosystem services such as oxygen production and pollination by bees, bumblebees, birds and bats. The "
    "ethical argument says every species has intrinsic value.",
    ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: pollination is a broadly utilitarian benefit"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity"),
    why="Options A, C and D include (e).",
    seconds=50)

add(BDC, "Patterns of biodiversity", "Intermediate", "direct",
    "Illustrating the latitudinal gradient in diversity, NCERT notes that Colombia, located near the equator, has "
    "nearly:",
    P("1,400 species of birds", ["105 species of birds", "56 species of birds", "1,200 species of birds"], "C"),
    "Latitudinal gradients",
    "Species diversity generally decreases from the equator towards the poles. Colombia, near the equator, has "
    "nearly 1,400 species of birds, while New York at 41° N has 105 species and Greenland at 71° N only 56 species. "
    "India, with much of its land in the tropics, has more than 1,200 species of birds.",
    ["Colombia (near equator) → about 1,400", "New York (41° N) → 105", "Greenland (71° N) → 56",
     "India → more than 1,200"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    why="105, 56 and 1,200 are NCERT's figures for New York, Greenland and India respectively.",
    seconds=30)

add(BDC, "In situ and ex situ conservation", "Advanced", "multi_statement",
    ms("Which of the following statements about biodiversity conservation are correct?",
       ["Many nations find it economically not feasible to conserve all their biological wealth, because the "
        "number of species waiting to be saved from extinction far exceeds the conservation resources available.",
        "The 'Earth Summit' held in Rio de Janeiro in 1992 called upon all nations to take appropriate measures for "
        "conservation of biodiversity and sustainable utilisation of its benefits.",
        "The World Summit on Sustainable Development was held in 2002 in Rio de Janeiro.",
        "At the World Summit on Sustainable Development, 190 countries pledged to achieve, by 2010, a significant "
        "reduction in the current rate of biodiversity loss.",
        "National parks are a means of ex situ conservation."]),
    P("(a), (b) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Conservation measures and international efforts",
    "Faced with the conflict between development and conservation, many nations find it unrealistic and "
    "economically not feasible to conserve all their biological wealth: the number of species waiting to be saved "
    "from extinction invariably far exceeds the conservation resources available. National parks are protected "
    "areas, a means of in situ conservation. The Earth Summit (Rio de Janeiro, 1992) called on nations to conserve biodiversity and use it "
    "sustainably. Its follow-up, the World Summit on Sustainable Development, was held in 2002 in Johannesburg, "
    "South Africa, where 190 countries pledged a significant reduction in the rate of biodiversity loss by 2010.",
    ["(a) True", "(b) True", "(c) False: the 2002 summit was in Johannesburg", "(d) True",
     "(e) False: national parks are in situ"],
    C12_BD("biodiversity conservation"),
    why="Options A, B and C include (c) or (e). (c) is the trap: it swaps the venue of the 2002 summit with that "
        "of the 1992 summit.",
    seconds=55)

add(BDC, "Importance and loss", "Advanced", "statement_pair",
    sp("Since the origin and diversification of life on earth there have been five episodes of mass extinction, and "
       "the 'sixth extinction' now in progress differs from them mainly in its rate.",
       "Current species extinction rates are estimated to be 100 to 1,000 times faster than in pre-human times, "
       "and human activities are responsible for the faster rates."),
    SP("A"),
    "The sixth extinction",
    "There have been five episodes of mass extinction. The 'sixth extinction' differs in its rate: current "
    "extinction rates are estimated at 100 to 1,000 times those of pre-human times, and our activities are "
    "responsible for the faster rates.",
    ["Statement I: true", "Statement II: true"],
    C12_BD("loss of biodiversity"),
    seconds=40)

add(BDC, "Importance and loss", "Advanced", "assertion_reason",
    ar("In a coevolved plant-pollinator mutualism, the extinction of one partner invariably leads to the extinction "
       "of the other.",
       "When a species becomes extinct, the plant and animal species associated with it in an obligatory way also "
       "become extinct."),
    AR("A"),
    "Co-extinctions",
    "Co-extinction is one of the four major causes of biodiversity loss: when a species becomes extinct, species "
    "associated with it obligatorily also become extinct. A coevolved plant-pollinator pair depends on each other "
    "obligatorily, so the extinction of one invariably leads to the extinction of the other. R is the general "
    "principle of which A is an instance.",
    ["A: true (NCERT example of co-extinction)", "R: true (definition of co-extinction)",
     "Obligatory partners die out together → R explains A"],
    C12_BD("loss of biodiversity: causes"),
    seconds=40)

add(BDC, "Patterns of biodiversity", "Advanced", "direct",
    "If we accept Robert May's global estimates, only 22 per cent of the total species have been recorded so far. "
    "Applying this proportion to India's diversity figures, India probably has yet to discover more than:",
    P("1,00,000 plant species and 3,00,000 animal species",
      ["10,000 plant species and 30,000 animal species", "3,00,000 plant species and 1,00,000 animal species",
       "45,000 plant species and 90,000 animal species"], "A"),
    "Estimating undiscovered species",
    "India has about 45,000 recorded plant species and twice as many animals. Using May's estimate that only 22% of "
    "species have been recorded, NCERT estimates that India probably has more than 1,00,000 plant species and more "
    "than 3,00,000 animal species yet to be discovered and described.",
    ["Recorded: about 45,000 plants, about twice as many animals", "Only 22% recorded (May)",
     "Yet to be discovered: > 1,00,000 plants and > 3,00,000 animals"],
    C12_BD("biodiversity in India"),
    why="Option B is ten times too small. Option C swaps plants and animals. Option D gives the already recorded "
        "numbers, not those yet to be discovered.",
    seconds=45)


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
    assert [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]] == pkg["question_ids"]
    assert len(QUESTIONS) == pkg["count"] == 125
    have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
    assert have == quota, {k: (have[k], quota[k]) for k in set(have) | set(quota) if have[k] != quota[k]}
    order = [q["topic"] for q in QUESTIONS]
    assert sorted(order, key=pkg["topics"].index) == order       # topics in plan order

    fmts = Counter(q["format"] for q in QUESTIONS)
    keys = Counter(q["correct_answer"] for q in QUESTIONS)
    n = len(QUESTIONS)
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "BATCH_002 package BOT_002_p2: 125 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 and "
                    "BATCH_001 were avoided. Numerical answers re-derived by tools/batch_002/BOT_002_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
