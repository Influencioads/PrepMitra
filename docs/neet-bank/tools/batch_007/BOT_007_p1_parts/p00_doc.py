"""Writes batches/parts/BATCH_007_BOT_p1.json: package BOT_007_p1 of batch 7 (Botany, 125 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_001501 .. NEET_BOT_001625.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books (secondary growth, taxonomical aids, plant life cycles and alternation of generations, early
experiments on photosynthesis) is not used. Facts already tested in batches 1-6 were listed with
`merge_batch.py stems 007 BOT_007_p1` and avoided; where a topic is saturated, questions test new combinations,
comparisons or applications. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_007/BOT_007_p1.py
"""

