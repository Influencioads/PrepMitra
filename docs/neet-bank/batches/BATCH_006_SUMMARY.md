# Batch 6 summary (17 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_001251` to `_001500`, written as 8 topic packages
(`tools/batch_006/*.py`) and merged into `BATCH_006.json`. The bank now holds **6,000 of 10,000**.

- **Difficulty:** 300 Basic / 399 Intermediate / 301 Advanced, exactly as planned per topic.
- **Formats:** 280 direct, 237 numerical, 137 statement pair, 131 assertion-reason, 118 multi-statement, 97 match the list.
- **Answer keys:** A 251, B 247, C 253, D 249.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–6 together (6,000 questions).

## Verification

- **287 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind with no key. 999 matched first time.
- **The one disagreement, `ZOO_001305`, was the solver's mistake.** NCERT says 100 mL of blood delivers 5 mL of O₂ and
  4 mL of CO₂.
- **18 questions were changed** and then re-checked blind:
  - **Six p-block questions (CHE p1)** depended on single-element facts: tin and steam, Al₂O₃ film, hexahalides,
    nitrogen disproportionation, Sn/Pb softness, and helium diffusing through rubber. They now test group trends,
    configurations or the anomalous first element.
  - **NCERT lines that are wrong in reality were removed:**
    - Miller's 800 °C.
    - "Almost 20 billion years" for the age of the universe.
    - The ozone layer forming before life.
    - "Microwaves resonate with water".
    - Gadolinium named as a room-temperature ferromagnet.
  - **One question needed knowledge outside NCERT** (lac operon and glucose). It was replaced.
  - **One non-standard ATP/NADPH assumption** was replaced with NCERT's 3 ATP + 2 NADPH per CO₂.
  - **Four assertion-reason or multi-statement items** had arguable keys and were reworded.
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

- **`CHE_001365`** (the reducing character of the group 16 dioxides falls down the group) is at the edge of the p-block
  rule.
- **Zoology and Botany are close to exhausted.** Most new items are application or scenario questions on NCERT
  mechanisms. Writers list the ones closest to earlier facts in their reports.
