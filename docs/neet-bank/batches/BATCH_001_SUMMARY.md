# Batch 1 summary (16 Nov 2026)

**980 original questions**, `NEET_PHY/CHE/BOT/ZOO_000006` to `_000250`. Together with the 20 samples that is 1,000 of
10,000. Written by 8 topic packages (`tools/batch_001/*.py`), merged into `BATCH_001.json`.

| | Physics | Chemistry | Botany | Zoology | Total |
|---|---:|---:|---:|---:|---:|
| Questions | 245 | 245 | 245 | 245 | 980 |

- **Difficulty:** 293 Basic / 394 Intermediate / 293 Advanced, exactly as planned per topic.
- **Formats:** 261 direct, 244 numerical, 131 statement pair, 127 multi-statement, 119 assertion-reason, 98 match the list.
- **Answer keys:** A 250, B 241, C 246, D 243.
- **Validator:** 0 errors, 0 warnings (sample + Batch 1 together, including the near-duplicate check).

## Verification

- **259 questions** have their answer recomputed by an `assert` in the builder (all numericals, plus isomer counts, bond
  orders, truth tables and similar).
- **All 980** were answered blind by a separate model instance that saw no answer key. **979 matched first time.**
- **One wrong key was caught and fixed.** `NEET_PHY_000018` statement (d) was "constant speed means zero
  acceleration". That is true for straight-line motion, which the stem specifies, so the keyed answer was wrong. (d) was
  replaced with a clearly false statement and re-checked.
- **Four questions were reworded** after checkers called them arguable, and re-checked blind:
  - Three assertion-reason questions where A versus B could be argued: `NEET_PHY_000230`, `NEET_BOT_000017`,
    `NEET_ZOO_000023`.
  - One wording slip in `NEET_ZOO_000154`: "ampullary-isthmic junction" changed to NCERT's "ampullary region".
- All 980 are `Pending Human Review`. None is approved; approval needs a teacher.

## What a teacher should check first

Authors listed the facts they were least sure of. Most concern the **rationalised NCERT (2023)**: whether these
sections are still in the current books. The NMC syllabus still lists their topics.

**Physics**
- Metre bridge (`000142`, `000149`).
- Transformer losses (`000182`).
- Curie's law (`000169`).
- Diamond critical angle (`000189`).
- Rolling friction (`000037`).
- Weightlessness (`000070`).
- Whether NCERT states, in so many words, that surface tension falls with temperature (`000085`).

**Chemistry**
- **p-Block (`000119`–`000131`):** the rationalised books dropped the chapter but NMC keeps the topic. These questions
  cite the pre-2023 edition and stay with general trends.
- **Lab-manual questions (`000242`–`000250`):** check the indicated temperatures and group reagents.
- **Etard and Stephen reactions (`000213`).**
- **The p-nitroaniline pKb of about 13 (`000231`):** not from the NCERT table.

**Botany**
- **Possibly removed NCERT examples:**
  - anisogamy in Eudorina;
  - honey bee sex determination (`000179`);
  - Lupinus and Phoenix seed viability (`000159`);
  - Ophrys (`000218`);
  - Abingdon tortoise (`000225`).
- **The RQ of malic acid (4/3):** computed, not stated by NCERT.
- **"Nucellar embryos are not genetically identical to the zygotic embryo" (`000158`):** inferred, not NCERT's words.
- **`000210` is a deliberate trap:** "primary sludge" is the false part. Keep the wording.

**Zoology**
- Frog anatomy details (`000037`, `000041`).
- Carbonic anhydrase rates (`000052`).
- pBR322 restriction sites, taken from the NCERT figure (`000232`).
- MTP and amniocentesis (`000174`, `000175`).
- NCERT's own definition of convergent evolution (`000189`).

**Assertion-reason keyed B** (R true but not the explanation), the type students argue about most. Spot-check these:
- Physics: `000092`, `000116`, `000149`.
- Chemistry: `000078`, `000093`.
- Botany: `000249`.
- Zoology: `000092`.

## Process notes for batches 2–10

- The validator's distinct-options check is now case-sensitive. Genotype options such as TT, Tt and tt were being
  treated as duplicates.
- Builders that place answer positions automatically to balance keys can move other questions' options when one
  question changes. After a fix, carry blind answers over by option text, not by letter (as was done here for
  `BOT_001_p1`).
