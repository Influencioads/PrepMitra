"""Writes batches/BATCH_000_sample.json: the 20 fully solved NEET sample questions for approval.

Five per paper section (Physics, Chemistry, Botany, Zoology), covering every NEET stem style: direct, numerical,
assertion-reason, two statements, match the list and multi-statement. Every computable answer is re-derived here
before the file is written; if an assertion fails, nothing is written. Answer keys are balanced (5 x A, B, C, D).

    python docs/neet-bank/tools/sample_batch_000.py
"""

import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings

ROOT = Path(__file__).resolve().parent.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
RECOMPUTED = ("script:recompute", "ai:author-solve")
AUTHORED = ("ai:author-solve",)
# Questions a separate model instance answered blind (no key) and matched; filled after that check.
# 2026-11-16: all 20 answered blind by a separate model instance; every answer matched, no issues raised.
BLIND_CHECKED = {f"NEET_{s}_{n:06d}" for s in ("PHY", "CHE", "BOT", "ZOO") for n in range(1, 6)}


def q(qid, subject, topic, subtopic, difficulty, fmt, text, options, answer, concept, explanation, steps,
      shortcut=None, why_others_wrong=None, ncert=None, seconds=60, verified_by=AUTHORED):
    assert answer in LETTERS and len(options) == 4
    tags = list(verified_by) + (["ai:independent-check"] if qid in BLIND_CHECKED else [])
    return {
        "question_id": qid, "exam_mappings": default_mappings(subject), "subject": subject, "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why_others_wrong, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": tags, "verified_at": TODAY},
    }


def match_options(correct: dict, wrong: list, at: str) -> list:
    """Option texts for a match-the-list question with the correct code at position `at`."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4
    return opts


PHY, CHE, BOT, ZOO = "Physics", "Chemistry", "Botany", "Zoology"

# ---------------------------------------------------------------- verification of computable answers
# P1 projectile: H = u^2 sin^2(theta) / 2g
u, g = 30, 10
H = F(u * u) * F(1, 4) / (2 * g)
assert H == F(45, 4)  # 11.25 m

# P2 dimensions as (M, L, T) exponents
DIM = {"Planck's constant": (1, 2, -1), "Pressure": (1, -1, -2), "Impulse": (1, 1, -1), "Surface tension": (1, 0, -2)}
assert DIM["Planck's constant"] == (1, 2, -2 + 1) and DIM["Surface tension"] == (1, 0, -2)

# P3 two cells in parallel across 4 ohm: node voltage V from Kirchhoff's current law
E1, r1, E2, r2, R = 6, 1, 4, 2, 4
V = F(E1, r1) + F(E2, r2)
V = V / (F(1, r1) + F(1, r2) + F(1, R))
I = V / R
assert I == F(8, 7)
assert F(E1 + E2, R + r1 + r2) == F(10, 7)  # distractor: cells wrongly taken in series

# P5 g at depth R/2 equals g at height h: (1 - 1/2) = 1 / (1 + h/R)^2  ->  h = (sqrt(2) - 1) R
h = math.sqrt(2) - 1
assert math.isclose(1 / (1 + h) ** 2, 0.5)
assert math.isclose(1 - 2 * 0.25, 0.5)  # distractor R/4 from the small-height approximation

# C2 first order: t(75%) = 2 t(50%)
k = math.log(4) / 60
assert math.isclose(math.log(2) / k, 30)

# C3 Nernst for Zn | Zn2+ (0.01 M) || Cu2+ (1 M) | Cu at 298 K
E = 1.10 - 0.059 / 2 * math.log10(0.01 / 1)
assert round(E, 3) == 1.159

# B3 AaBbCc x AaBbCc: fraction with the dominant phenotype for exactly one trait
dom = F(3, 4)
exactly = {n: sum(math.prod(dom if t else 1 - dom for t in combo)
                  for combo in itertools.product([True, False], repeat=3) if sum(combo) == n) for n in range(4)}
assert exactly[1] == F(9, 64) and exactly[2] == F(27, 64) and exactly[3] == F(27, 64)

# Z3 Hardy-Weinberg: aa = 16 %  ->  carriers among phenotypically normal = 2pq / (p^2 + 2pq)
q_ = F(2, 5)
p_ = 1 - q_
assert q_ * q_ == F(16, 100)
assert 2 * p_ * q_ / (p_ * p_ + 2 * p_ * q_) == F(4, 7)

# ---------------------------------------------------------------- questions
QUESTIONS = [
    # ------------------------------------------------------------ Physics
    q("NEET_PHY_000001", PHY, "Kinematics", "Projectile motion", "Basic", "numerical",
      "A ball is thrown with a speed of 30 m/s at an angle of 30° above the horizontal. Taking g = 10 m/s², the "
      "maximum height reached by the ball is:",
      ["5.625 m", "11.25 m", "22.5 m", "45 m"], "B",
      "Maximum height of a projectile",
      "Only the vertical component of velocity, u sin θ, decides how high the ball rises. It rises until this "
      "component becomes zero.",
      ["Vertical component: u sin θ = 30 × sin 30° = 15 m/s",
       "At the top, vertical velocity = 0, so 0 = (15)² − 2gH",
       "H = 225 / (2 × 10) = 11.25 m"],
      shortcut="H = u² sin²θ / 2g = 900 × ¼ / 20 = 11.25 m.",
      why_others_wrong="45 m uses the full speed (u²/2g). 22.5 m forgets the 2 in 2g. 5.625 m divides by an extra 2.",
      seconds=50, verified_by=RECOMPUTED),

    q("NEET_PHY_000002", PHY, "Physics and Measurement", "Dimensional analysis", "Basic", "match_list",
      "Match List-I (physical quantity) with List-II (dimensional formula).\n\n"
      "List-I:\nA. Planck's constant\nB. Pressure\nC. Impulse\nD. Surface tension\n\n"
      "List-II:\nI. [M T⁻²]\nII. [M L² T⁻¹]\nIII. [M L⁻¹ T⁻²]\nIV. [M L T⁻¹]\n\n"
      "Choose the correct answer from the options given below:",
      match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                    [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                     {"A": "I", "B": "III", "C": "IV", "D": "II"}], at="D"),
      "D",
      "Dimensions from defining equations",
      "Write each quantity from an equation that defines it, then replace every term by its dimensions.",
      ["Planck's constant h = E/ν: [M L² T⁻²] / [T⁻¹] = [M L² T⁻¹] → II",
       "Pressure = force/area: [M L T⁻²] / [L²] = [M L⁻¹ T⁻²] → III",
       "Impulse = force × time: [M L T⁻²] × [T] = [M L T⁻¹] → IV",
       "Surface tension = force/length: [M L T⁻²] / [L] = [M T⁻²] → I"],
      shortcut="Impulse has the same dimensions as momentum, [M L T⁻¹], and h has the dimensions of angular "
               "momentum, [M L² T⁻¹].",
      seconds=45),

    q("NEET_PHY_000003", PHY, "Current Electricity", "Cells, emf and internal resistance", "Advanced", "numerical",
      "Two cells of emf 6 V and 4 V, with internal resistances 1 Ω and 2 Ω respectively, are connected in parallel "
      "(positive terminal to positive terminal). A 4 Ω resistor is connected across the combination. The current "
      "through the 4 Ω resistor is:",
      ["10/7 A", "1 A", "8/7 A", "5/4 A"], "C",
      "Kirchhoff's current law at a junction (cells in parallel)",
      "Let V be the common terminal voltage. The currents from the two cells add up to the current in the resistor.",
      ["Current from the 6 V cell: (6 − V)/1; from the 4 V cell: (4 − V)/2; through the resistor: V/4",
       "(6 − V) + (4 − V)/2 = V/4",
       "Multiply by 4: 24 − 4V + 8 − 2V = V, so 7V = 32 and V = 32/7 V",
       "Current through 4 Ω = V/4 = 8/7 A ≈ 1.14 A"],
      shortcut="Equivalent cell: E = (E₁/r₁ + E₂/r₂)/(1/r₁ + 1/r₂) = 8/1.5 = 16/3 V, r = 2/3 Ω; "
               "I = (16/3)/(4 + 2/3) = 8/7 A.",
      why_others_wrong="10/7 A treats the cells as if in series (10 V across 7 Ω). 5/4 A averages the emfs and "
                       "ignores internal resistance. 1 A uses the 4 V cell alone.",
      seconds=120, verified_by=RECOMPUTED),

    q("NEET_PHY_000004", PHY, "Magnetic Effects of Current and Magnetism", "Force on charges and conductors",
      "Intermediate", "assertion_reason",
      "Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
      "Assertion (A): A charged particle moving parallel to a uniform magnetic field continues to move in a "
      "straight line.\n"
      "Reason (R): The magnetic force on a moving charged particle does no work on it.\n\n"
      "Choose the correct answer from the options given below:",
      ASSERTION_REASON, "B",
      "Magnetic (Lorentz) force F = q(v × B)",
      "When v is parallel to B, v × B = 0, so there is no force and the particle is not deflected: A is true. "
      "The magnetic force is always perpendicular to v, so it does no work: R is also true. But R is not why the "
      "particle goes straight; a force that does no work can still bend the path (circular motion when v ⊥ B). "
      "The reason is that the force is zero.",
      ["F = qvB sin θ with θ = 0° gives F = 0 → A is true",
       "F ⊥ v always, so power F·v = 0 → R is true",
       "R does not explain A: zero work does not mean zero deflection"],
      why_others_wrong="Option A is the trap: R is true, but zero work also holds when the particle moves in a "
                       "circle, so it cannot explain the straight path.",
      seconds=50),

    q("NEET_PHY_000005", PHY, "Gravitation", "Variation of g", "Advanced", "numerical",
      "The acceleration due to gravity at a depth R/2 below the Earth's surface is equal to the acceleration due to "
      "gravity at a height h above the surface. If R is the radius of the Earth, h is:",
      ["(√2 − 1)R", "R/2", "R/4", "√2 R"], "A",
      "Variation of g with depth and with height",
      "Below the surface g falls linearly with depth; above it g falls as the inverse square of distance from the "
      "centre. Set the two equal.",
      ["At depth d: g_d = g(1 − d/R) = g(1 − 1/2) = g/2",
       "At height h: g_h = g / (1 + h/R)²",
       "g/(1 + h/R)² = g/2 → (1 + h/R)² = 2 → 1 + h/R = √2",
       "h = (√2 − 1)R ≈ 0.414 R"],
      why_others_wrong="R/4 comes from g_h ≈ g(1 − 2h/R), which is valid only when h ≪ R; here h is comparable "
                       "to R. R/2 assumes depth and height act equally. √2 R forgets to subtract 1.",
      seconds=90, verified_by=RECOMPUTED),

    # ------------------------------------------------------------ Chemistry
    q("NEET_CHE_000001", CHE, "Chemical Bonding and Molecular Structure", "VSEPR shapes", "Basic", "direct",
      "Which of the following molecules has a see-saw shape?",
      ["XeF₄", "BF₃", "CH₄", "SF₄"], "D",
      "VSEPR theory: bond pairs and lone pairs around the central atom",
      "A see-saw shape comes from 4 bond pairs and 1 lone pair (5 electron pairs, trigonal bipyramidal "
      "arrangement with the lone pair in an equatorial position).",
      ["SF₄: S has 6 valence electrons, 4 used in bonds → 4 bond pairs + 1 lone pair → see-saw",
       "XeF₄: 4 bond pairs + 2 lone pairs → square planar",
       "BF₃: 3 bond pairs, no lone pair → trigonal planar",
       "CH₄: 4 bond pairs, no lone pair → tetrahedral"],
      seconds=30),

    q("NEET_CHE_000002", CHE, "Chemical Kinetics", "Half-life", "Intermediate", "numerical",
      "A first-order reaction is 75% complete in 60 minutes. The time taken for it to be 50% complete is:",
      ["30 min", "40 min", "45 min", "20 min"], "A",
      "Half-life of a first-order reaction is independent of initial concentration",
      "75% completion means 25% (one quarter) remains, which takes exactly two half-lives.",
      ["100% → 50% (one half-life) → 25% (two half-lives)",
       "2 × t½ = 60 min",
       "t½ = 30 min"],
      shortcut="For first order, t₇₅% = 2 t₅₀%.",
      why_others_wrong="45 min assumes the reaction proceeds at a constant rate (zero order).",
      seconds=40, verified_by=RECOMPUTED),

    q("NEET_CHE_000003", CHE, "Redox Reactions and Electrochemistry", "Nernst equation and Gibbs energy",
      "Advanced", "numerical",
      "For the cell Zn | Zn²⁺ (0.01 M) || Cu²⁺ (1 M) | Cu, E°cell = 1.10 V. The emf of the cell at 298 K is "
      "(take 2.303RT/F = 0.059 V):",
      ["1.041 V", "1.10 V", "1.159 V", "1.218 V"], "C",
      "Nernst equation",
      "Cell reaction: Zn + Cu²⁺ → Zn²⁺ + Cu, with n = 2. A lower product concentration (Zn²⁺) than reactant "
      "concentration (Cu²⁺) makes the emf larger than E°.",
      ["E = E° − (0.059/n) log ([Zn²⁺]/[Cu²⁺])",
       "E = 1.10 − (0.059/2) log (0.01/1) = 1.10 − 0.0295 × (−2)",
       "E = 1.10 + 0.059 = 1.159 V"],
      why_others_wrong="1.041 V gets the sign of the log term wrong. 1.218 V uses n = 1. 1.10 V ignores "
                       "concentration.",
      seconds=75, verified_by=RECOMPUTED),

    q("NEET_CHE_000004", CHE, "Coordination Compounds", "Valence bond theory", "Intermediate", "statement_pair",
      "Given below are two statements:\n\n"
      "Statement I: [Ni(CN)₄]²⁻ is square planar and diamagnetic.\n"
      "Statement II: [NiCl₄]²⁻ is tetrahedral and paramagnetic.\n\n"
      "In the light of the above statements, choose the correct answer from the options given below:",
      STATEMENT_PAIR, "A",
      "Valence bond theory: strong- and weak-field ligands with a d⁸ ion",
      "Ni²⁺ is 3d⁸. CN⁻ is a strong-field ligand: it pairs the 3d electrons, leaving one 3d orbital free for dsp² "
      "hybridisation (square planar, no unpaired electrons). Cl⁻ is a weak-field ligand: no pairing, so sp³ "
      "hybridisation (tetrahedral) with two unpaired electrons.",
      ["Ni²⁺: [Ar] 3d⁸",
       "[Ni(CN)₄]²⁻: pairing → dsp² → square planar, 0 unpaired electrons → diamagnetic (Statement I true)",
       "[NiCl₄]²⁻: no pairing → sp³ → tetrahedral, 2 unpaired electrons → paramagnetic (Statement II true)"],
      ncert="Class 12 Chemistry, 'Coordination Compounds', valence bond theory", seconds=45),

    q("NEET_CHE_000005", CHE, "Organic Compounds Containing Oxygen", "Aldehydes and ketones", "Advanced",
      "multi_statement",
      "Which of the following compounds give a positive iodoform test?\n\n"
      "(a) Ethanol\n(b) Propan-2-ol\n(c) Propan-1-ol\n(d) Acetophenone\n(e) Pentan-3-one\n\n"
      "Choose the correct answer from the options given below:",
      ["(a), (c) and (e) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (b) and (c) only"], "B",
      "Haloform reaction",
      "The iodoform test is positive for compounds with a CH₃CO– group (methyl ketones and acetaldehyde), and for "
      "alcohols with a CH₃CH(OH)– group, which I₂/NaOH first oxidises to CH₃CO–.",
      ["(a) Ethanol, CH₃CH₂OH → oxidised to CH₃CHO → positive",
       "(b) Propan-2-ol, CH₃CH(OH)CH₃ → oxidised to acetone → positive",
       "(c) Propan-1-ol, CH₃CH₂CH₂OH → gives propanal, no CH₃CO– → negative",
       "(d) Acetophenone, C₆H₅COCH₃ → methyl ketone → positive",
       "(e) Pentan-3-one, CH₃CH₂COCH₂CH₃ → ethyl groups on both sides, no CH₃CO– → negative"],
      why_others_wrong="Pentan-3-one is the usual trap: it is a ketone but not a methyl ketone.",
      seconds=75),

    # ------------------------------------------------------------ Botany
    q("NEET_BOT_000001", BOT, "Cell: The Unit of Life", "Prokaryotic cell", "Basic", "direct",
      "Which of the following is absent in a typical bacterial cell?",
      ["Ribosomes", "Plasma membrane", "Mitochondria", "Cell wall"], "C",
      "Prokaryotic cells lack membrane-bound organelles",
      "Bacteria have no membrane-bound organelles such as mitochondria, plastids or a nucleus. They do have a "
      "plasma membrane, 70S ribosomes and (in most) a cell wall.",
      ["Mitochondria are membrane-bound → absent in prokaryotes",
       "Ribosomes (70S) are not membrane-bound → present",
       "Plasma membrane and cell wall are parts of the bacterial cell envelope → present"],
      ncert="Class 11 Biology, 'Cell: The Unit of Life', prokaryotic cells", seconds=25),

    q("NEET_BOT_000002", BOT, "Plant Growth and Development", "Plant growth regulators", "Intermediate",
      "match_list",
      "Match List-I (plant growth regulator) with List-II (effect).\n\n"
      "List-I:\nA. Auxin\nB. Gibberellin\nC. Cytokinin\nD. Ethylene\n\n"
      "List-II:\nI. Promotes fruit ripening\nII. Causes apical dominance\nIII. Delays leaf senescence\n"
      "IV. Causes bolting in rosette plants\n\n"
      "Choose the correct answer from the options given below:",
      match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                    [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                     {"A": "I", "B": "IV", "C": "III", "D": "II"}], at="B"),
      "B",
      "Physiological effects of plant growth regulators",
      "Each regulator has a signature effect that NEET tests directly.",
      ["Auxin: the growing apical bud inhibits lateral buds (apical dominance) → II",
       "Gibberellin: internode elongation just before flowering in rosette plants such as cabbage (bolting) → IV",
       "Cytokinin: promotes nutrient mobilisation and delays leaf senescence → III",
       "Ethylene: enhances respiration rate during ripening (respiratory climacteric) → I"],
      ncert="Class 11 Biology, 'Plant Growth and Development', plant growth regulators", seconds=40),

    q("NEET_BOT_000003", BOT, "Principles of Inheritance and Variation", "Mendelian inheritance", "Advanced",
      "numerical",
      "In a cross AaBbCc × AaBbCc, the three genes assort independently and each shows complete dominance. "
      "What fraction of the offspring will show the dominant phenotype for exactly one of the three traits?",
      ["27/64", "3/64", "1/64", "9/64"], "D",
      "Product rule for independently assorting genes",
      "For each gene, Aa × Aa gives the dominant phenotype with probability 3/4 and the recessive with 1/4. "
      "'Exactly one dominant' can happen in 3 ways (which trait is dominant).",
      ["P(dominant) = 3/4, P(recessive) = 1/4 for each trait",
       "One particular arrangement, e.g. dominant–recessive–recessive: 3/4 × 1/4 × 1/4 = 3/64",
       "Three such arrangements: 3 × 3/64 = 9/64"],
      why_others_wrong="27/64 is the fraction for exactly two dominant traits (and also for all three). 3/64 "
                       "counts only one arrangement. 1/64 is the triple-recessive fraction.",
      ncert="Class 12 Biology, 'Principles of Inheritance and Variation', dihybrid cross", seconds=90,
      verified_by=RECOMPUTED),

    q("NEET_BOT_000004", BOT, "Photosynthesis", "Photorespiration", "Intermediate", "assertion_reason",
      "Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
      "Assertion (A): C₄ plants show little or no photorespiration.\n"
      "Reason (R): In C₄ plants the Calvin cycle runs in bundle sheath cells, where a high CO₂ concentration "
      "makes RuBisCO act mainly as a carboxylase.\n\n"
      "Choose the correct answer from the options given below:",
      ASSERTION_REASON, "A",
      "Why C₄ plants avoid photorespiration",
      "RuBisCO binds both CO₂ and O₂; photorespiration happens when it binds O₂. C₄ plants first fix CO₂ in "
      "mesophyll cells and release it in bundle sheath cells, raising the CO₂ concentration around RuBisCO. So "
      "RuBisCO's oxygenase activity is minimised. R is true and is exactly why A is true.",
      ["Photorespiration = oxygenation of RuBP by RuBisCO", "C₄ pathway concentrates CO₂ in bundle sheath cells",
       "High CO₂ : O₂ ratio → carboxylation dominates → little photorespiration"],
      ncert="Class 11 Biology, 'Photosynthesis in Higher Plants', photorespiration and the C₄ pathway", seconds=45),

    q("NEET_BOT_000005", BOT, "Ecosystem", "Productivity and decomposition", "Basic", "statement_pair",
      "Given below are two statements:\n\n"
      "Statement I: Gross primary productivity minus the respiration losses of producers is the net primary "
      "productivity.\n"
      "Statement II: Secondary productivity is the rate at which producers form new organic matter.\n\n"
      "In the light of the above statements, choose the correct answer from the options given below:",
      STATEMENT_PAIR, "C",
      "Primary and secondary productivity",
      "GPP − R = NPP, so Statement I is true. Secondary productivity is the rate of formation of new organic "
      "matter by consumers, not producers, so Statement II is false.",
      ["NPP = GPP − R → Statement I true", "Secondary productivity refers to consumers → Statement II false"],
      ncert="Class 12 Biology, 'Ecosystem', productivity", seconds=30),

    # ------------------------------------------------------------ Zoology
    q("NEET_ZOO_000001", ZOO, "Body Fluids and Circulation", "Blood and blood groups", "Basic", "direct",
      "A person with blood group AB has:",
      ["No antigens on RBCs and both anti-A and anti-B antibodies in plasma",
       "Antigens A and B on RBCs and no anti-A or anti-B antibodies in plasma",
       "Antigens A and B on RBCs and both anti-A and anti-B antibodies in plasma",
       "No antigens on RBCs and no antibodies in plasma"], "B",
      "ABO blood grouping",
      "The blood group is named after the antigens on the RBCs. The plasma carries antibodies only against the "
      "antigens the person lacks, so group AB has neither antibody. This is why AB people are called universal "
      "recipients.",
      ["Group AB → antigens A and B on RBCs", "Both antigens present → no anti-A, no anti-B in plasma"],
      why_others_wrong="The first option describes group O. Having both antigen and its antibody (third option) "
                       "would make the person's own blood clump.",
      ncert="Class 11 Biology, 'Body Fluids and Circulation', ABO grouping", seconds=25),

    q("NEET_ZOO_000002", ZOO, "Excretory Products and their Elimination", "Regulation of kidney function",
      "Intermediate", "multi_statement",
      "Which of the following statements about antidiuretic hormone (ADH) are correct?\n\n"
      "(a) It is released into the blood from the neurohypophysis.\n"
      "(b) It increases water reabsorption from the latter parts of the renal tubule.\n"
      "(c) Its deficiency causes diabetes insipidus.\n"
      "(d) It is secreted by the adrenal cortex.\n\n"
      "Choose the correct answer from the options given below:",
      ["(a), (b) and (d) only", "(b) and (c) only", "(a), (c) and (d) only", "(a), (b) and (c) only"], "D",
      "Hormonal regulation of water reabsorption",
      "ADH (vasopressin) is made by hypothalamic neurons and released from the posterior pituitary "
      "(neurohypophysis). It makes the distal tubule and collecting duct reabsorb more water. Too little ADH "
      "causes diabetes insipidus: large volumes of dilute urine.",
      ["(a) True: stored in and released from the neurohypophysis", "(b) True: acts on the distal parts of the tubule",
       "(c) True: deficiency → diabetes insipidus", "(d) False: the adrenal cortex secretes aldosterone, not ADH"],
      ncert="Class 11 Biology, 'Excretory Products and their Elimination', regulation of kidney function",
      seconds=45),

    q("NEET_ZOO_000003", ZOO, "Evolution", "Gene flow, drift and Hardy-Weinberg", "Advanced", "numerical",
      "In a population in Hardy-Weinberg equilibrium, 16% of individuals show a recessive trait (genotype aa). "
      "Among the individuals who do NOT show the trait, what fraction are carriers (Aa)?",
      ["4/7", "12/25", "3/7", "3/5"], "A",
      "Hardy-Weinberg principle: p² + 2pq + q² = 1",
      "q² is the recessive fraction; find q and p, then compare carriers (2pq) with all individuals showing the "
      "dominant trait (p² + 2pq).",
      ["q² = 0.16 → q = 0.4, p = 0.6",
       "AA = p² = 0.36, Aa = 2pq = 0.48 → normal individuals = 0.84",
       "Carriers among normal = 0.48 / 0.84 = 4/7 ≈ 0.57"],
      why_others_wrong="12/25 (0.48) is the carrier fraction of the whole population, not of the normal "
                       "individuals asked about. 3/7 is the AA share among normal individuals. 3/5 is p.",
      ncert="Class 12 Biology, 'Evolution', Hardy-Weinberg principle", seconds=90, verified_by=RECOMPUTED),

    q("NEET_ZOO_000004", ZOO, "Human Health and Disease", "Pathogens and diseases", "Intermediate", "match_list",
      "Match List-I (disease) with List-II (causative organism).\n\n"
      "List-I:\nA. Typhoid\nB. Malaria\nC. Ascariasis\nD. Ringworm\n\n"
      "List-II:\nI. Plasmodium vivax\nII. Trichophyton\nIII. Salmonella typhi\nIV. Ascaris lumbricoides\n\n"
      "Choose the correct answer from the options given below:",
      match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                    [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
                     {"A": "III", "B": "I", "C": "II", "D": "IV"}], at="C"),
      "C",
      "Common human diseases and their pathogens",
      "Typhoid is bacterial, malaria is protozoan, ascariasis is caused by a roundworm (helminth) and ringworm by "
      "fungi.",
      ["Typhoid → Salmonella typhi (bacterium) → III", "Malaria → Plasmodium (protozoan) → I",
       "Ascariasis → Ascaris (intestinal roundworm) → IV",
       "Ringworm → fungi of genera Microsporum, Trichophyton, Epidermophyton → II"],
      ncert="Class 12 Biology, 'Human Health and Disease', common diseases in humans", seconds=35),

    q("NEET_ZOO_000005", ZOO, "Biotechnology: Principles and Processes", "Restriction enzymes", "Intermediate",
      "assertion_reason",
      "Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
      "Assertion (A): The restriction endonuclease EcoRI cuts DNA at random sites.\n"
      "Reason (R): EcoRI recognises the palindromic nucleotide sequence 5'-GAATTC-3'.\n\n"
      "Choose the correct answer from the options given below:",
      ASSERTION_REASON, "D",
      "Specificity of restriction endonucleases",
      "Restriction endonucleases cut only at specific recognition sequences. EcoRI recognises the palindrome "
      "GAATTC and cuts between G and A on each strand, leaving sticky ends. So A is false and R is true.",
      ["Restriction endonucleases are sequence-specific → A is false",
       "EcoRI site: 5'-GAATTC-3' / 3'-CTTAAG-5', a palindrome → R is true"],
      ncert="Class 12 Biology, 'Biotechnology: Principles and Processes', restriction enzymes", seconds=35),
]

if __name__ == "__main__":
    from collections import Counter
    assert len(QUESTIONS) == 20
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert set(keys.values()) == {5}, keys
    doc = {"schema_version": "1.0", "batch_id": "BATCH_000", "created_at": TODAY,
           "notes": "20 fully solved NEET (UG) samples for approval: 5 per section, every stem style. All original.",
           "stimuli": [], "questions": QUESTIONS}
    out = ROOT / "batches" / "BATCH_000_sample.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}")
