# Batch 9 summary (18 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_002001` to `_002250`, written as 8 topic packages
(`tools/batch_009/*.py`) and merged into `BATCH_009.json`. The bank now holds **9,000 of 10,000**.

- **Difficulty:** 300 Basic / 400 Intermediate / 300 Advanced, exactly as planned per topic.
- **Formats:** 237 numerical, 232 direct, 151 assertion-reason, 140 statement pair, 120 multi-statement, 120 match the list.
- **Answer keys:** A 255, B 244, C 256, D 245.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–9 together (9,000 questions).

## Verification

- **287 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind with no key, and every key matched first time.
- **20 questions were changed** and all 20 matched on a blind re-check:
  - **NCERT lines that are wrong in reality (6):** bacterial flagella as extensions of the cell wall, xanthophylls
    listed apart from carotenoids, 1100–1200 mL/min as the filtration rate, the resting potential caused by the
    Na⁺/K⁺ pump, modern humans dated 75,000–10,000 years ago (and a distractor built on it).
  - **Outside the strict NMC wording (5):** three p-block items on single compounds (I₂ bond enthalpy, Sn/Pb halide
    covalency, group 15 hydride boiling points), the Curie–Weiss law, and minimum NAND-gate counts.
  - **Ambiguous wording or arguable keys (6):** a lung-volume stem, a polygene count, a pendulum statement, a Saheli
    count, and two assertion-reason items.
  - **Not stated by NCERT (3):** a Griffith + DNase hypothetical, short capillary-tube meniscus behaviour, and two
    items the writer could not confirm in the rationalised book (earthworm as farmer's friend, goats as alien invasion).
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

- **`CHE_002128`** keys the anomalous first element by NCERT's "no d orbitals" explanation, an older bonding model.
- **`PHY_002148`, `PHY_002157`** use μr = 1 + χ; confirm the magnetisation section is still in the rationalised NCERT.
- **Zener diode and logic-gate items** cite the NMC syllabus; the rationalised NCERT dropped them.
- **Batch 6's `CHE_001358`** (group 16 vs group 15 ionisation enthalpies) is on the final-audit list: NCERT's own
  data contradict its wording for Sb/Te and Bi/Po.
