# Brief for subject-batch authors (Batches 2–10)

You write **one subject's part of one batch** of PrepMitra's 10,000-question banking bank (IBPS PO, IBPS Clerk, IBPS
RRB Officer Scale-I, IBPS RRB Office Assistant, SBI PO, SBI Clerk). Today is 2026-11-05. All paths below are
relative to `C:\Users\LENOVO\Downloads\examapp\PrepMitra\docs\question-bank`; run commands from there.

## Read first
- `README.md`: schema decisions, the **Four-option rules**, validation rules.
- `question.schema.json`: exact record format. `01_EXAM_PATTERNS.md`: official patterns. `03_SOURCES.md`: preferred sources.
- `batches/plans/BATCH_<NNN>_plan.json`: your subject's exact quota per (topic, difficulty), your question ID range
  and your first stimulus ID (continue sequentially from it).
- The previous batch's builder for your subject, `tools/batch_<NNN-1>/<subject>.py`, and its output: reuse its
  structure and helpers. Batch 1 builders are the reference quality bar.
- `tools/qbank.py`: validator. Use `default_mappings(subject, difficulty)` for exam mappings.

## Deliverables
1. `tools/batch_<NNN>/<subject>.py` (add `sys.path.insert(0, <tools dir>)` to import qbank), which writes
   `batches/parts/BATCH_<NNN>_<PREFIX>.json` (schema_version "1.0", batch_id "BATCH_<NNN>", created_at "2026-11-05",
   notes, stimuli, questions). The script asserts every computable answer and the quota before writing.
2. 0 errors and 0 warnings from (list every earlier file of your subject so duplicates are checked across batches;
   the newest file must be last):
   `python tools/qbank.py validate batches/BATCH_000_sample.json batches/parts/BATCH_001_<PREFIX>.json ... batches/parts/BATCH_<NNN>_<PREFIX>.json --plan batches/plans/BATCH_<NNN>_plan.json --subject "<Subject>"`

Quant authors also run `python tools/series_audit.py <all earlier QUANT files> batches/parts/BATCH_<NNN>_QUANT.json`
and fix every SUSPECT line (a wrong option that some other common rule also produces).

## No repeats across batches
Before writing, dump the question stems (and stimuli titles) of all earlier files of your subject and read them. Do not
test the same fact, the same passage theme, the same puzzle structure or the same numeric template with new numbers
only. New contexts, new structures, new facts. The validator only catches textual near-duplicates; repeated facts are
your responsibility.

## Rules (all subjects)
- Exactly the planned count per (topic, difficulty); subtopic from that topic's subtopic list in the plan.
- Exactly 4 options (A–D); one defensible answer; balanced correct keys (~25% each).
- Relation questions: a strict answer (x > y) never sits beside its weaker form (x ≥ y); avoid exactly-equal
  quantities (the fourth relation would also be true). The validator rejects the first case.
- Difficulty: Basic = Clerk/OA prelims; Intermediate = PO prelims / Clerk mains; Advanced = PO mains. Not school-level.
- Full solution: concept, explanation, steps, shortcut where a real one exists, why_others_wrong, final_answer
  "Option X: ...", realistic suggested_time_seconds. Shared passages/data/puzzles go in `stimuli` (3–6 questions
  per set, set_position 1..n).
- source: Original, PrepMitra, url null, year null. Never copy from coaching sites, newspapers or books.
- verification: review_status "Pending Human Review", verified_at "2026-11-05". verified_by must be honest:
  `script:recompute` / `script:brute-force-unique` only if the script really checks it; `ai:independent-check` only
  when a separate, fresh subagent (not you, the author) answered the question from a key-free dump and matched the
  key, and the question was not changed afterwards without a re-check; use `ai:self-recheck` for your own re-solve; `web:fact-check` only for facts confirmed on a page you
  opened; `web:search-confirmed` when only search results confirmed it (e.g. pib.gov.in returns 403 to fetches).

## Facts (GA, Banking, and Computer where non-obvious)
- Every GA/Banking question needs `fact_checks` with URLs you actually opened or saw in search results that state the
  fact. Never invent a URL. If you cannot verify a fact, drop it and write a different question.
- Time-sensitive questions (current affairs, appointments, awards, sports, summits, books, economic data, rates,
  Budget/Economic Survey, anything that can change) need `current_affairs: {event_date, review_by}`. Event dates
  must come from the source, not memory. Use review_by "2027-05-05". Current-affairs window: events from
  2025-11-01 to 2026-11-04, verified on official sites (pib.gov.in, ministries, rbi.org.in, organisers' sites) or
  major news outlets. Do not invent or extrapolate events.
- Some sites block automated access (pib.gov.in and indiabudget.gov.in return 403; rbidocs PDFs show a bot check).
  **Do not try to get around a block** (no user-agent spoofing, no CAPTCHA or bot-check workarounds). Use another
  page you can open that states the fact (ministry or regulator HTML pages, rbi.org.in, organisers' sites, major news
  outlets), or rely on search results and mark the question `web:search-confirmed`.
- RBI rates read from https://www.rbi.org.in/ on 2026-11-05: Repo 5.50%, SDF 5.25%, MSF 5.75%, Bank Rate 5.75%,
  CRR 3.00%, SLR 18.00%; the MPC met 5–7 October 2026, next meeting 2–4 December 2026.

## Scope and report
Only create/modify your builder and your part file. Other agents run at the same time and share the session
scratchpad: put any temporary files in your own subfolder named `<NNN>_<PREFIX>` there and never overwrite files you
did not create. Report shared-tool bugs instead of fixing them. Report back
briefly: quota matched, validator summary (with all earlier files), answer-key distribution, verification methods,
facts dropped, anything a human reviewer should check.
