# Batch 4 summary (16 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_000751` to `_001000`, written as 8 topic packages
(`tools/batch_004/*.py`) and merged into `BATCH_004.json`. The bank now holds **4,000 of 10,000**.

- **Difficulty:** 301 Basic / 399 Intermediate / 300 Advanced, exactly as planned per topic.
- **Formats:** 270 direct, 237 numerical, 146 statement pair, 131 assertion-reason, 121 multi-statement, 95 match the list.
- **Answer keys:** A 248, B 249, C 252, D 251.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–4 together (4,000 questions).

## Verification

- **253 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind with no key. 999 matched first time.
- **The one disagreement, `BOT_000998`, was the solver's mistake.** NCERT's "Evil Quartet" has co-extinctions, not
  pollution. The key (A) stands, and a second blind solve agreed.
- **Four questions were tightened** and re-checked blind:
  - `PHY_000947`: the prism is now stated to be equilateral. "Parallel to the base at minimum deviation" holds only for
    an isosceles prism.
  - `CHE_000976`: the claim that pyridine is "a base stronger than the amine" was dropped. NCERT says it, but
    chemically it is wrong.
  - `BOT_000761` and `BOT_000993`: assertion-reason Reasons were reworded so that R clearly explains A.
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

- **`BOT_000761`:** the new R says acellular particles lack "mode of nutrition". The re-check accepted the key but
  noted that a student could argue the point.
- **p-block group 13/14 facts** cited to the pre-2023 NCERT (CHE p1).
- **Biology section names in `ncert_reference`**, written from memory of the rationalised books (ZOO p2).
- **Physics Experimental Skills items**, which have no NCERT reference.
