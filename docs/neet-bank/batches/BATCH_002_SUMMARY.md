# Batch 2 summary (16 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_000251` to `_000500`, written as 8 topic packages
(`tools/batch_002/*.py`) and merged into `BATCH_002.json`. The bank now holds **2,000 of 10,000**.

- **Difficulty:** 299 Basic / 401 Intermediate / 300 Advanced, exactly as planned per topic.
- **Formats:** 267 direct, 243 numerical, 141 statement pair, 131 multi-statement, 120 assertion-reason, 98 match the list.
- **Answer keys:** A 247, B 250, C 254, D 249. Writers set each answer's position by hand this time; no code reshuffles
  options.
- **Validator:** 0 errors and 0 warnings for the sample, Batch 1 and Batch 2 together. Each writer first read every
  earlier question on its topics and avoided those facts and number templates. The near-duplicate check caught two
  close templates during writing, and both were rewritten.

## Verification

- **248 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind by a separate solver with no answer key. 998 matched first time.
- **One wrong key was caught and fixed.** In `NEET_PHY_000384` (Wheatstone bridge), the circuit as described balances at
  P/Q = S/R, so the keyed 30 Ω was wrong. The stem now describes the standard two-branch layout, and the builder asserts
  the null condition.
- **The other disagreement, `NEET_BOT_000460`, was the solver's mistake.** NCERT says only a *small* part of the
  activated sludge is returned as inoculum. The key (C) stands, and a second blind solve agreed.
- **Three wordings were tightened** and re-checked blind:
  - `NEET_ZOO_000354`: "voluntary control".
  - `NEET_PHY_000290`: "under gravity and tension only".
  - `NEET_BOT_000455`: "one complete codon".
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

Writers listed the facts they were least sure of:

- **Possibly removed in rationalised NCERT:**
  - Wien's law (`PHY_000320`), Newton's law of cooling (`PHY_000330`), Carnot refrigerator (`PHY_000340`).
  - Logic gates. They were dropped from the book, but the NMC syllabus lists them.
  - "Do plants breathe?" (`BOT_000369`).
  - Evolution "brief account" dates (`ZOO_000436`–`443`).
  - Applications of coordination compounds (`CHE_000395`).
- **p-block facts cited to the pre-2023 NCERT** (`CHE_000367`, `375`, `377`, `378`), as in Batch 1.
- **Numbers to confirm against the current book:**
  - Biosphere reserves, national parks and sanctuaries (Botany, biodiversity).
  - 38 ATP in the respiration balance sheet (`BOT_000373`).
  - Testicular lobules (`ZOO_000390`).
- **Assertion-reason keyed B**, the type students dispute most. Spot-check these:
  - Physics: `PHY_000312`.
  - Chemistry: `CHE_000339`, `CHE_000427`.
  - Botany: `BOT_000259`, `276`, `293`, and the Amazon "lungs of the planet" question in BOT p2, which is the most arguable.
  - Zoology: `ZOO_000388`, `ZOO_000463`, and the five in ZOO p1 listed in that writer's report.
