# Brief for NEET package authors

You write **one package** of PrepMitra's 10,000-question NEET (UG) bank: a fixed set of topics of one subject, for one
batch. Other authors write other topics at the same time, so you cannot collide with them. Today is 2026-11-16. `created_at` and `verified_at` stay "2026-11-16". All
paths are relative to `C:\Users\LENOVO\Downloads\examapp\PrepMitra\docs\neet-bank`; run commands from there.

## Read first
- `README.md` (question styles, schema differences), `question.schema.json` (exact record format).
- `01_EXAM_PATTERN.md` and the relevant part of `02_SYLLABUS_AND_DISTRIBUTION.md`: **only content the NMC 2026
  syllabus lists**. Each subject's "Not in the 2026 syllabus" list is off limits.
- `tools/sample_batch_000.py` and `batches/BATCH_000_sample.json`: the quality bar and a `q()` helper to copy.
- `batches/plans/BATCH_<NNN>_plan.json`: find your package (e.g. `PHY_001_p1`). It gives your topics, the exact quota
  per (topic, difficulty), your ID range and your output path.
- `tools/qbank.py`: validator, `ASSERTION_REASON`, `STATEMENT_PAIR`, `default_mappings(subject)`.

## Deliverables
1. A builder `tools/batch_<NNN>/<package>.py` (add `sys.path.insert(0, <tools dir>)` to import qbank) that writes your
   output file: `schema_version` "1.0", `batch_id` "BATCH_<NNN>", `created_at` "2026-11-16", `notes`, `stimuli` (usually
   `[]`), `questions` in ID order. The builder asserts every computable answer and your quota before it writes. Write it
   in several parts (several short tool calls); a single huge write tends to fail.
2. 0 errors and 0 warnings from (sample first, earlier merged batches next, your file last):
   `python tools/qbank.py validate batches/BATCH_000_sample.json batches/BATCH_001.json ... <your file> --plan batches/plans/BATCH_<NNN>_plan.json --package <package>`
   (run it in the background with no timeout: on all batches it takes over 10 minutes; read its output file when
   it ends, and re-run it if the output is empty).

## Writing rules
- **Exactly** the planned count per (topic, difficulty), IDs exactly your range in order, subtopic from the topic's list.
- Four options A–D, exactly one defensible answer, answer keys balanced (about 25% each across your package).
- **Formats** (field `format`), aim across the package: Physics about 55% `numerical`; Chemistry about 30% `numerical`;
  Botany and Zoology about 5% `numerical` (genetics, ecology ratios). The rest spread over `direct`,
  `assertion_reason`, `statement_pair`, `match_list` and `multi_statement`, each at least 8% of your package. Use the
  fixed option sets for assertion-reason and statement-pair, and `match_options()` from the sample builder for
  match-the-list.
- **Difficulty:** Basic = direct NCERT recall or a one-step calculation. Intermediate = two steps, or linking two
  ideas, or a careful reading of an NCERT line. Advanced = multi-step numericals, multi-concept statements, traps that
  real NEET papers set. All at NEET level, not board-exam level and not JEE Advanced.
- **Stay inside the NMC wording, not just the chapter.** Where the syllabus narrows a unit, keep to it. Chemistry:
  p-Block (groups 13–18) is ONLY "electronic configuration, general trends in physical and chemical properties, and
  unique behaviour of the first element" - no individual compounds, allotropes, oxoacids, xenon compounds or uses.
  Electrochemistry cells are ONLY the dry cell, lead accumulator and fuel cells (no mercury cell). Check every unit's
  NMC text in `02_SYLLABUS_AND_DISTRIBUTION.md` and the NMC syllabus before using a sub-topic.
  Biology: no pedigree analysis or pedigree symbols (removed from the rationalised NCERT, not in the NMC list).
  p-Block, strictly: every tested fact must be a configuration, a trend down a group or across a period, or the
  anomalous first element. A single element's own reaction, property or use (tin + steam, Al oxide film, helium in
  rubber, which hexahalides exist, astatine being radioactive, gallium's melting point) does not count.
  d/f-block: lanthanoids ONLY configuration, oxidation states, lanthanoid contraction (no hardness, tarnishing,
  colour, reactions); actinoids ONLY configuration and oxidation states (no actinoid contraction).
  Physics Thermodynamics: no heat engines, Carnot engine, efficiency or refrigerator COP (beyond the NMC wording).
  Genetics: plain Hardy-Weinberg only, no conditional (Bayesian) probabilities.
- **NCERT lines that are wrong in reality are off limits**, even with "according to NCERT": e.g. Miller's 800 °C,
  "20 billion years", ozone layer before life, "microwaves resonate with water", "reptiles have no external ear
  openings", NCERT's T. rex / jawless-fish dates, pyridine "a stronger base than the amine", ctenophores "radially symmetrical", hexokinase acting on fructose to give
glucose-6-phosphate, "every parietal ovary becomes two-chambered", the white-light fringe next to the centre being red,
recombination changing a single gene's allele frequency, bacterial flagella as "extensions from the cell wall",
xanthophylls listed apart from carotenoids, 1100-1200 mL/min as the filtration rate, the resting potential caused by
the Na+/K+ pump, modern Homo sapiens arising 75,000-10,000 years ago, Lupinus arcticus 10,000-year dormancy,
Monascus as a "yeast", the Amazon producing 20% of atmospheric oxygen, Amazon species counts, the Basmati patent,
GEAC as "Approval" committee, the "recently cleared" Patents Bill amendment. Physics: no Curie-Weiss law, no minimum
NAND-gate counts. Chemistry p-block: no single-compound values (hydride boiling points, X-X bond enthalpies, Sn/Pb
halide covalency). Count questions: every listed item must be unambiguously in or out (e.g. Saheli is not clearly
hormonal or non-hormonal). Do not combine two NCERT experiments into a hypothetical NCERT does not describe. Do not key inferences NCERT does not state (no somatostatin ->
gigantism, more enzyme -> higher Vmax) or classifications NCERT does not give (Penicillium's class). Also avoid borderline
  facts (gadolinium as a room-temperature ferromagnet) and anything needing knowledge NCERT does not give.
- **No counts that change over time** (numbers of biosphere reserves, national parks, sanctuaries, hotspots, species
  totals), no removed sections (earthworm, cockroach, pedigree analysis, the old Chemistry hormones section beyond a
  general introduction), and give in the stem any value students cannot work out by hand (e.g. 2^0.2).
- **Facts come from NCERT** (rationalised Class 11–12 textbooks). Every Botany/Zoology question sets
  `solution.ncert_reference` (class, chapter name, section). Chemistry and Physics set it when the question tests an NCERT
  statement. Do not test facts that NCERT does not state, numbers that differ between books, or disputed examples.
  If you are not sure of a fact, write a different question.
- **Numericals:** give every constant the question needs (g, h, R, Kf, 2.303RT/F, log values) in the stem, choose
  numbers that work out cleanly, and recompute the answer in the builder with an `assert`. Make wrong options come
  from real mistakes (wrong formula, sign, unit, factor of 2), and say which mistake in `why_others_wrong`.
- **Multi-statement and match-the-list:** every statement must be clearly true or clearly false by NCERT. The
  correct combination must be the only one among the options.
- **Full solution:** concept, explanation, steps, shortcut where a real one exists, why_others_wrong, final_answer
  "Option X: ...", realistic suggested_time_seconds (20–180).
- **No repeats.** Do not test the same fact twice in your package. Run
  `python tools/merge_batch.py stems <NNN> <package> > <your scratch folder>/earlier.txt` and read it: it lists every
  earlier question on your topics with its answer. Do not test those facts again, or the same numeric template with new
  numbers; find a different fact, angle or set-up (NCERT has far more than has been asked). Validate together with the
  earlier merged batches (`batches/BATCH_001.json` ... ) so the near-duplicate check covers them.
- **Assertion-reason keyed B** (R true but not the explanation) is what students dispute most. Use it only when R is
  plainly unrelated to why A is true (a different property of the same thing), never when R is a consequence of A or a
  partial reason. If you are unsure whether R explains A, write a different question.
- **Multi-statement and "which is correct" questions must hold for the exact situation in the stem.** Check each
  statement under the stem's own conditions (straight-line motion, ideal gas, aqueous solution, ...). A Batch 1 key was
  wrong because a statement that is false in general was true under the stem's condition.
- **Answer positions:** choose each question's correct position yourself and keep it fixed. Do not write code that
  re-balances positions across questions, because one later edit then moves the options of many other questions.
- **Original only.** Never copy or paraphrase questions from coaching sites, apps, PYQ collections or books. Do not
  browse question sites. `source`: Original, PrepMitra, url null, year null.
- **verification:** review_status "Pending Human Review", verified_at "2026-11-16". `verified_by` must be honest:
  `script:recompute` only if your builder really asserts the answer; `ai:author-solve` always; `ai:self-recheck` for
  your own second solve. Do **not** add `ai:independent-check`; the coordinator adds it after a separate blind solve.

## Scope and report
Create or change only your builder and your output file. Temporary files go in the session scratchpad, in your own
subfolder named after your package. Do not edit shared tools; report bugs in them instead. On this Windows machine
bash heredocs sometimes fail on quoting: write each builder part with the Write tool and join the parts.
Report briefly: quota matched, validator result, answer-key and format counts, and anything a teacher should check
(facts you were least sure of).
