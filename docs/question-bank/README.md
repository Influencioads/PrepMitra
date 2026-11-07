# PrepMitra Banking Question Bank

**Status (7 Nov 2026): complete.** 10,000 original questions in `batches/BATCH_001.json` to `BATCH_010.json` plus the
20-question `BATCH_000_sample.json` counted in the total. Exact targets met: Quant 2,000, Reasoning 2,000, English 1,500,
General Awareness 1,500, Banking 2,000, Computer 1,000; 3,000 Basic / 4,000 Intermediate / 3,000 Advanced. Validator:
0 errors (one accepted near-duplicate warning, `BANK_REAS_000004 ~ BANK_REAS_000099`). Every question is still
"Pending Human Review"; each `BATCH_0NN_SUMMARY.md` lists what a reviewer should look at.

**Browse:** `python -m http.server 8765 --directory docs/question-bank`, then open `/viewer/index.html`.

**Import into the app** (`backend/app/services/bank_import.py`): creates the six Mains exams, activates blueprints that
follow `exam_patterns.json`, adds the bank's topics, and stores each question once per exam stage that tests its
subject (10,000 questions become 88,000 exam rows). Re-running it updates rows and never undoes an admin's
approve/reject.

```bash
cd backend
python -m app.services.bank_import --dry-run              # report only
python -m app.services.bank_import                        # draft: served only after expert approval
python -m app.services.bank_import --status verified --publish   # serve in mocks now (used for local dev)
```

Questions whose checks were weaker (no blind re-solve, or facts confirmed only via search results) are put in the
admin review sample when imported as verified.

## Phase 1 (research and sample)

This folder holds the research and specification for the 10,000-question banking bank (IBPS PO, IBPS Clerk, IBPS
RRB Officer Scale-I, IBPS RRB Office Assistant, SBI PO, SBI Clerk). Question generation starts only after this phase
is approved.

| # | Deliverable | File |
|---|---|---|
| 1 | Complete syllabus (subject → topic → subtopic) | [02_SYLLABUS_AND_DISTRIBUTION.md](02_SYLLABUS_AND_DISTRIBUTION.md), [taxonomy.json](taxonomy.json) |
| 2 | Official patterns for all six exams | [01_EXAM_PATTERNS.md](01_EXAM_PATTERNS.md), [exam_patterns.json](exam_patterns.json) |
| 3 | Topic-wise distribution of the 10,000 questions | [02_SYLLABUS_AND_DISTRIBUTION.md](02_SYLLABUS_AND_DISTRIBUTION.md) |
| 4 | Source research report with URLs | [03_SOURCES.md](03_SOURCES.md) |
| 5 | Database-ready JSON schema | [question.schema.json](question.schema.json) |
| 6 | 20 fully solved sample questions | [batches/BATCH_000_sample.json](batches/BATCH_000_sample.json) |
| - | Validator and manifest builder | [tools/qbank.py](tools/qbank.py) |

```bash
python tools/build_distribution.py                       # rebuild taxonomy.json and the distribution tables
python tools/sample_batch_000.py                         # rebuild the samples (re-derives every computable answer)
python tools/qbank.py validate batches/*.json            # validate all batches together (exit code 1 on errors)
python tools/qbank.py manifest batches/*.json            # write manifest.json (cumulative counts)
```

Run these from this folder.

## Schema: differences from the brief, and why

The brief's example record was kept, with these changes:

1. **`exam_ids` + `exam_stage` → `exam_mappings: [{exam_id, stage, section_key}]`.** A single question is often
   valid in one exam's prelims and another exam's mains (e.g. IBPS PO Prelims and IBPS Clerk Mains), which a single
   `exam_stage` field cannot express. Each entry maps to one row of `question_exam_mappings`.
2. **Marks and negative marks moved off the question** into `exam_patterns.json`, per section. The brief asks for
   marks to be configurable by exam and stage, and the official sections have fractional per-question marks (for
   example, 30 marks for 35 questions). The API attaches the marks when it serves a question in a given section.
   `suggested_time_seconds` stays on the question.
3. **Shared stimuli.** Reading passages, DI tables and puzzle conditions are stored once in `stimuli` and referenced by
   `stimulus_id` and `set_position`. Real papers ask 3 to 5 questions per passage, table or puzzle.
4. **`current_affairs: {event_date, review_by}`** is required for time-sensitive topics. After `review_by`, the
   validator warns and the app should stop serving the question until it is re-verified.
5. **`verification.fact_checks`** (claim, source URL, date checked) is mandatory for GA and Banking questions.
6. **Review status:** `Draft → Pending Human Review → Approved / Rejected`. `Approved` requires a `human:` entry
   in `verified_by`; the validator enforces this. All 20 samples are **Pending Human Review**: the answers were
   checked by script and by me, but no human has reviewed them yet.
7. **Exactly four options (A to D)**, as the brief asks. The real papers have five, so see "Four-option rules" below.

## Four-option rules

Some question types in the real exams have a fixed set of five answers. With four options, one of the five must be
dropped, and it is never the correct answer:

| Question type | Real exam's five answers | Four options PrepMitra uses |
|---|---|---|
| Syllogism, inequality, statement–conclusion | Only I / Only II / Either / Neither / Both | Only I, Only II, Neither, Both. If the answer is "Either I or II", it replaces whichever wrong option is least likely to be chosen. |
| Quadratic equations, quantity comparison | > / ≥ / < / ≤ / = or cannot be established | The correct relation, "x = y or the relationship cannot be established" (always kept), and two wrong relations. A strict answer (x > y) never sits beside its weaker form (x ≥ y), because that would also be true; the validator rejects it. Avoid exactly-equal quantities, because any fourth relation (≥ or ≤) would then also be true. |
| Data sufficiency | I alone / II alone / Either alone / Both together / Neither | The correct answer plus the three most tempting of the other four |
| Error detection | Four parts + No error | Three parts + No error |

Because PrepMitra scores by section (max marks ÷ questions, minus ¼ of that for a wrong answer), four options do not
change the marking. They do make guessing slightly easier than in the real exam (25% instead of 20%).

## Validation rules (tools/qbank.py)

These are enforced on every batch and across all batches given:

- Structure, enums and ID format (`BANK_<SUBJ>_NNNNNN`, where the prefix must match the subject).
- Exactly 4 options with keys A to D in order, distinct option texts, the answer key is one of the options, and
  `final_answer` names the same option.
- Every exam mapping exists in `exam_patterns.json` and that section actually tests the subject.
- The topic exists in `taxonomy.json` for the subject (an unknown subtopic is a warning).
- Stimulus references resolve, and `set_position` runs from 1 to n within each set.
- Current-affairs dates are present and not past the review date. GA and Banking questions have fact checks.
- Source honesty: an `Original` question cannot carry an exam year or URL; `Official PYQ` and `Licensed`
  questions need a URL and a licence note.
- **Duplicates.** An exact duplicate (normalised stem, sorted options and stimulus, hashed) is an error. A
  near-duplicate (similarity ≥ 0.92 within the same subject, with shingle blocking so 10,000 questions stay fast) is a
  warning for the human reviewer, since a same-template Quant question with new numbers can be legitimate.

It was tested against a deliberately broken file. It caught an exact duplicate across files, a wrong exam section,
an `Original` question claiming an exam year, `Approved` with no human reviewer, a missing current-affairs date and an
invalid answer key. It also caught a bug in its own first normalisation, which treated "x > y" and "x ≥ y" as the same
option.

## How the existing backend maps to this

The current `questions` model (`backend/app/models/catalog.py`) stores one `exam_id`, one `topic_id`, `difficulty`
as easy/medium/hard and options as JSON. Importing this bank needs:

- a many-to-many `question_exam_mappings` table (exam, stage, section) in place of the single `exam_id`;
- subject → topic → subtopic as shared rows, not per-exam topics;
- `question_sets` (stimuli) and `question_sources`;
- the difficulty map Basic/Intermediate/Advanced → easy/medium/hard.

This is Phase 7 of the brief (SQL, import and API). It has not been built yet.

## Decisions needed before batch generation

1. ~~Four or five options?~~ **Decided 2026-11-05: four options (A to D)**, as in the brief. The real papers use five,
   so formats with a fixed answer set follow the rules in "Four-option rules" below.
2. **Fix the app's IBPS PO and RRB prelims blueprints** in `backend/app/seed.py` to match the 2026 notifications. See
   findings 1 and 2 in [01_EXAM_PATTERNS.md](01_EXAM_PATTERNS.md).
3. **Approve the topic weights** in [02_SYLLABUS_AND_DISTRIBUTION.md](02_SYLLABUS_AND_DISTRIBUTION.md). Four topics
   were added beyond the brief because they appear regularly in these exams: Quadratic Equations, Wrong Number Series,
   Problems on Ages and RBI Circulars. Static Awareness was also added for RRB GA.
4. **Current-affairs window.** 1,047 questions (917 GA and 130 Banking: repo rate, Budget and Economic Survey) are
   time-sensitive. I suggest writing them in the last batches,
   just before release, with `review_by` set about 6 months out, so they are not stale on day one.
