# Batch 7 summary (17 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_001501` to `_001750`, written as 8 topic packages
(`tools/batch_007/*.py`) and merged into `BATCH_007.json`. The bank now holds **7,000 of 10,000**.

- **Difficulty:** 301 Basic / 400 Intermediate / 299 Advanced, exactly as planned per topic.
- **Formats:** 246 direct, 239 numerical, 136 statement pair, 135 assertion-reason, 131 multi-statement, 113 match the list.
- **Answer keys:** A 251, B 249, C 251, D 249.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–7 together (7,000 questions).

## Verification

- **293 answers** are recomputed by an `assert` in the builders.
- **All 1,000** were answered blind with no key, and every key matched first time.
- **9 questions were changed** and re-checked blind:
  - **Out-of-date or wrong-in-reality figures removed:**
    - India's 14 biosphere reserves and 90 national parks.
    - Thyroxine rising "several-fold" in pregnancy.
    - Relaxin as pregnancy-only (it is also made in normal cycles), replaced by hPL.
  - **Removed or out-of-scope content replaced:**
    - The earthworm section.
    - The old Chemistry hormones section (mineralocorticoids, Addison's disease). The NMC lists only a general
      introduction to hormones.
  - **Stem fixes:**
    - The ribosome-size stem no longer claims NCERT gives that size.
    - The species–area statement now gives the 2^Z values students need.
    - A match list with two equivalent List-II items was rewritten.
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

- **Older batches may contain more out-of-date counts.** Batch 2 used the same biosphere-reserve and national-park
  figures. A final audit for time-sensitive counts is planned before the bank is called complete.
- **Physics Experimental Skills and logic-gate items** still have no NCERT reference (they are NMC-listed but not in
  the rationalised book).
