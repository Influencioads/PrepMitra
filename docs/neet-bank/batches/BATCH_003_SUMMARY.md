# Batch 3 summary (16 Nov 2026)

**1,000 original questions**, `NEET_PHY/CHE/BOT/ZOO_000501` to `_000750`, written as 8 topic packages
(`tools/batch_003/*.py`) and merged into `BATCH_003.json`. The bank now holds **3,000 of 10,000**.

- **Difficulty:** 301 Basic / 400 Intermediate / 299 Advanced, exactly as planned per topic.
- **Formats:** 259 direct, 240 numerical, 141 statement pair, 133 multi-statement, 132 assertion-reason, 95 match the list.
- **Answer keys:** A 251, B 253, C 249, D 247.
- **Validator:** 0 errors and 0 warnings for the sample and Batches 1–3 together.

## Verification

- **257 answers** are recomputed by an `assert` in the builders. The Physics builders also solve every described circuit
  and capacitor network to confirm the layout gives the keyed answer.
- **All 1,000** were answered blind with no key. Every one matched; there were no wrong keys in this batch.
- **Syllabus scope.** The blind checkers now also judge scope against the NMC wording. **8 Chemistry questions went
  beyond it and were replaced**, then re-checked blind:
  - the mercury cell (2);
  - individual p-block compounds: phosphorus allotropes, chlorine oxoacids, noble-gas uses, S₂ and xenon fluorides (4);
  - lanthanoid reactions and uses (2).
  The rule is now in the writer brief.
- **`NEET_ZOO_000694` rewritten.** It used NCERT dates that are wrong in reality (jawless fish 350 mya, seaweeds
  320 mya) and NCERT's "T. rex was the biggest dinosaur". It now tests the order of evolution, which is not disputed.
- **`NEET_CHE_000587` reworded.** It said Pb forms "at the anode" during charging, which is ambiguous. It now says
  "negative plate / positive plate".
- **Scope audit of Batches 1–3.** A read-only agent reviewed 419 candidates: every p-Block, d/f-block and
  electrochemistry question, plus keyword hits for every excluded area in all four subjects. It found 6 more
  out-of-scope questions in Batches 1–2:
  - `CHE_000087`: the Ni–Cd cell.
  - `CHE_000094`: the mercury cell.
  - `CHE_000128`: xenon compounds.
  - `CHE_000142`: actinoid contraction.
  - `CHE_000378`: argon's occurrence in air.
  - `CHE_000390`: lanthanoid ion colours.

  Their original writers replaced them with in-scope questions (same IDs, topics and key positions). The replacements
  were re-checked blind, and Batches 1 and 2 were re-merged.
- All 1,000 are `Pending Human Review`.

## For a teacher to check first

- **The MTP (Amendment) Act 2017 statements in Zoology.** NCERT's wording may lag the current law.
- **Logic gates and lab-experiment questions in Physics** have no NCERT reference. Gates are in the NMC syllabus but
  were dropped from the book.
- **Frog anatomy details.** In scope, because the NMC lists the frog's systems. Check them against the current book.
- **Assertion-reason keyed B**, the type students dispute most. Each package keeps these to cases where R is a separate
  property. The writers' reports list them by ID.
