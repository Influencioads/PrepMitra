# PrepMitra NEET (UG) Question Bank

**Status (18 Nov 2026): all 10,000 written.** The 20 samples (`batches/BATCH_000_sample.json`) and Batches 1–10
(`batches/BATCH_001.json` … `BATCH_010.json`, 2,500 per subject) are validated together and every question was answered
blind by a separate solver whose answer matched the key (`ai:independent-check`). Each batch has a summary
(`batches/BATCH_0NN_SUMMARY.md`) listing what was changed and what a teacher should check first. A final audit across
all batches removed NCERT lines that are wrong in reality or out of date, time-changing counts and out-of-syllabus
content (see [batches/FINAL_AUDIT.md](batches/FINAL_AUDIT.md)). All questions are still "Pending Human Review": AI
checks are not a substitute for subject-teacher approval.

How a batch is made: `tools/plan_batches.py` sets the quotas; 8 authors write topic packages following
[tools/AUTHOR_BRIEF.md](tools/AUTHOR_BRIEF.md); a separate solver answers each package with no key
(`tools/merge_batch.py dump` / `apply`); disagreements are fixed and re-checked; `tools/merge_batch.py <n>` joins the
packages.

Every question is **original**. Nothing is scraped or copied from coaching sites or apps (see
[03_SOURCES.md](03_SOURCES.md), section D).

| # | Deliverable | File |
|---|---|---|
| 1 | Official 2026 exam pattern | [01_EXAM_PATTERN.md](01_EXAM_PATTERN.md), [exam_patterns.json](exam_patterns.json) |
| 2 | Syllabus (NMC 2026) → topics → subtopics, with the 10,000-question split | [02_SYLLABUS_AND_DISTRIBUTION.md](02_SYLLABUS_AND_DISTRIBUTION.md), [taxonomy.json](taxonomy.json) |
| 3 | Sources, with URLs | [03_SOURCES.md](03_SOURCES.md) |
| 4 | Import-ready JSON schema | [question.schema.json](question.schema.json) |
| 5 | 20 fully solved samples | [batches/BATCH_000_sample.json](batches/BATCH_000_sample.json) |
| - | Validator, manifest, plan and sample builders | [tools/](tools/) |

```bash
python tools/build_distribution.py                 # rebuild taxonomy.json and the distribution tables
cd tools && python sample_batch_000.py && cd ..    # rebuild the samples (re-derives every numerical answer)
python tools/qbank.py validate batches/*.json      # validate (exit code 1 on errors)
python tools/qbank.py manifest batches/*.json      # write manifest.json
```

Run these from this folder.

## The plan

- **10,000 questions**: 2,500 each for Physics, Chemistry, Botany and Zoology, the four 45-question blocks of the
  paper. Difficulty is 3,000 Basic / 4,000 Intermediate / 3,000 Advanced, as in the banking bank.
- **Only what the NMC 2026 syllabus lists.** Each topic records its NMC unit. NCERT chapters the syllabus leaves out
  (for example Transport in Plants, Digestion and Absorption, s-Block, Polymers) are listed as "no questions" in
  `taxonomy.json` and the distribution file.
- Topic weights are **estimates**, not counts from past papers. Change a weight in `tools/build_distribution.py` and
  re-run it.

## Question styles

All questions are four-option, single-answer MCQs, as the NTA bulletin specifies. The `format` field records the
stem style, because NEET mixes several:

| `format` | What it is | Rule the validator enforces |
|---|---|---|
| `direct` | Plain question | none |
| `numerical` | Calculation with numeric options | the answer must be recomputed by script before release |
| `assertion_reason` | Assertion (A) and Reason (R) | the four options are the fixed NEET set, in a fixed order |
| `statement_pair` | Statement I and Statement II | fixed option set, fixed order |
| `match_list` | Match List-I with List-II | each option is a code like `A-II, B-III, C-I, D-IV`, each numeral used once |
| `multi_statement` | "Which of (a)–(e) are correct?" | none |

Diagram-based questions are left out for now: the app shows text only. They can be added once the question model
supports images.

## Schema: differences from the banking bank

1. Subjects are `Physics`, `Chemistry`, `Botany`, `Zoology`. IDs are `NEET_PHY_000001` and so on.
2. One exam mapping per question: `NEET_UG` / `UG` / the subject's section. Marks (+4/−1) come from
   `exam_patterns.json`.
3. New required field `format` (table above), and an optional `solution.ncert_reference`. The validator warns when a
   Biology question has none, so a reviewer can check the fact against NCERT.
4. No current-affairs fields: NEET content does not expire.
5. Review status works as in banking: `Pending Human Review` until a subject teacher approves the question.
   `Approved` needs a `human:` entry in `verified_by`.

## Verification of the samples

- The 7 numerical answers are re-derived in `tools/sample_batch_000.py` before the file is written (`script:recompute`).
- All 20 were answered blind (no answer key) by a separate model instance. All 20 answers matched and it raised no
  issues (`ai:independent-check`). It noted that a few students might argue for A instead of B on `NEET_PHY_000004`; the
  solution explains why R does not explain A.
- **Still needed:** a Physics, a Chemistry and a Biology teacher to review the 20 samples before batch writing starts.

## Import into the app

`backend/app/services/neet_import.py` creates the **NEET (UG)** exam in the new **Medical entrance** category
(`medical`), activates a blueprint that follows `exam_patterns.json` (4 × 45 questions, +4/−1, one 180-minute
timer), adds the bank's topics, and stores each question keyed by its bank ID. Re-running it updates questions and
never undoes an admin's approve/reject.

```bash
cd backend
python -m app.services.neet_import --dry-run                       # report only
python -m app.services.neet_import                                 # draft: served only after expert approval
python -m app.services.neet_import --status verified --publish     # serve in mocks now (local dev only)
```

The seed adds NEET (UG) as a **draft** in the launch catalog, like every non-banking exam. Publish it from the admin
panel (or with `--publish`) once enough questions are approved. After publishing, the website lets students start
it only when `VITE_OPEN_EXAM_CATEGORIES` includes `medical`; otherwise it shows as "Coming soon". The mobile app has no
such switch, so it can be started there as soon as it is published.
