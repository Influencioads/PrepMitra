"""Writes batches/parts/BATCH_008_BOT_p1.json: package BOT_008_p1 of batch 8 (Botany, 130 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants, Plant Growth and Development. IDs NEET_BOT_001751 .. NEET_BOT_001880.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books or outside the NMC 2026 list (secondary growth, taxonomical aids, plant life cycles and
alternation of generations, early experiments on photosynthesis, seed dormancy, photoperiodism, vernalisation) is not
used. Facts already tested in batches 1-7 were listed with `merge_batch.py stems 008 BOT_008_p1` and avoided; where a
topic is saturated, questions test new combinations, comparisons or applications. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_008/BOT_008_p1.py
"""
