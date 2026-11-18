# Batch 5 summary (17 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_001001` to `_001250`, written as 8 topic packages
(`tools/batch_005/*.py`) and merged into `BATCH_005.json`. The bank now holds **5,000 of 10,000**.

- **Difficulty:** 299 Basic / 405 Intermediate / 296 Advanced, exactly as planned per topic.
- **Formats:** 273 direct, 234 numerical, 149 statement pair, 128 assertion-reason, 120 multi-statement, 96 match the list.
- **Answer keys:** A 255, B 246, C 255, D 244.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–5 together (5,000 questions).

## Verification

- **242 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind with no key, and every key matched. There were no wrong keys in this batch.
- **Pedigree analysis removed from the bank.** It was dropped from the rationalised NCERT and is not in the NMC list.
  - Three Batch 5 questions and two Batch 3 questions (`BOT_000662`, `BOT_000670`) were replaced.
  - Three more Mendelian questions (`BOT_000677`, `BOT_001168`, `BOT_001181`) only had their solution labels changed.
  - The rule is now in the writer brief.
- **Disputed NCERT fact removed.** Two questions relied on NCERT's "reptiles have no external ear openings", which is
  wrong for many lizards (`ZOO_001012`, `ZOO_001015`).
- **Two wordings tightened:**
  - `ZOO_001162`: "all" vasa efferentia.
  - `BOT_001049`: the thorns Reason now states the cause plainly.
- The 9 changed questions were re-checked blind and all matched.
- All 1,000 are `Pending Human Review`.

## Process note

A network outage and a usage-limit pause stopped the writers mid-batch. Each was resumed from its saved files, and
nothing was lost.

## For a teacher to check first

- **Zoology topics are now heavily covered.** Writers report that many new items are application or scenario
  questions built on NCERT lines that earlier batches already used. Batches 6–10 will lean more on this.
- **Chemistry p-block group 13/14 trends** are still cited to the pre-2023 NCERT.
- **`CHE_001076`** asks about adding an inert gas at constant pressure. NCERT covers only constant volume, but the
  answer follows from Le Chatelier's principle.
