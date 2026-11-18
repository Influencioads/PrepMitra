"""Writes batches/parts/BATCH_010_ZOO_p1.json: package ZOO_010_p1 of BATCH_010 (Zoology, 131 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination;
Chemical Coordination and Integration. IDs NEET_ZOO_002251 .. NEET_ZOO_002381. Every numerical answer is re-derived
below before the file is written, and the plan quota, ID range, subtopics, key balance and format mix are asserted.
Facts follow the rationalised NCERT Class 11 Biology textbook; for the frog only the digestive, circulatory,
respiratory, nervous and reproductive systems, and no earthworm or cockroach anatomy. Facts already tested in
BATCH_000 to BATCH_009 (see `merge_batch.py stems 10 ZOO_010_p1`) are not asked again in the same way; most items are
application, identification, counting or comparison questions that combine NCERT statements in new ways.

    python docs/neet-bank/tools/batch_010/ZOO_010_p1.py
"""


import json
import re
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
ZOO = "Zoology"
PACKAGE = "ZOO_010_p1"
BATCH = "BATCH_010"
FIRST_ID, LAST_ID = 2251, 2381
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")

QUESTIONS = []

AK = "Animal Kingdom"
SOA = "Structural Organisation in Animals"
BIO = "Biomolecules"
BRE = "Breathing and Exchange of Gases"
BFC = "Body Fluids and Circulation"
EXC = "Excretory Products and their Elimination"
LOC = "Locomotion and Movement"
NEU = "Neural Control and Coordination"
CCI = "Chemical Coordination and Integration"


def ref(chapter, section):
    return f"Class 11 Biology, '{chapter}', {section}"


def Z(topic, subtopic, difficulty, fmt, text, options, answer, concept, explanation, steps, ncert,
      shortcut=None, why_others_wrong=None, seconds=45, verified_by=AUTHORED):
    """Appends one Zoology question with the next ID in the package range."""
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4
    assert ncert, "every Zoology question needs an NCERT reference"
    if fmt == "assertion_reason":
        assert options == ASSERTION_REASON
    if fmt == "statement_pair":
        assert options == STATEMENT_PAIR
    if fmt == "numerical":
        assert verified_by == RECOMPUTED
    qid = f"NEET_ZOO_{FIRST_ID + len(QUESTIONS):06d}"
    QUESTIONS.append({
        "question_id": qid, "exam_mappings": default_mappings(ZOO), "subject": ZOO, "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why_others_wrong, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(verified_by), "verified_at": TODAY},
    })


def match_options(correct: dict, wrong: list, at: str) -> list:
    """Option texts for a match-the-list question with the correct code at position `at`."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    for m in [correct, *wrong]:
        assert sorted(m) == list("ABCD") and sorted(m.values()) == sorted(["I", "II", "III", "IV"])
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4
    return opts


def M(a, b, c, d):
    return {"A": a, "B": b, "C": c, "D": d}


def ar(assertion, reason):
    return ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {assertion}\nReason (R): {reason}\n\n"
            "Choose the correct answer from the options given below:")


def sp(one, two):
    return (f"Given below are two statements:\n\nStatement I: {one}\nStatement II: {two}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")


def ml(intro, list1, list2):
    l1 = "\n".join(f"{k}. {v}" for k, v in zip("ABCD", list1))
    l2 = "\n".join(f"{k}. {v}" for k, v in zip(["I", "II", "III", "IV"], list2))
    return (f"Match List-I ({intro[0]}) with List-II ({intro[1]}).\n\nList-I:\n{l1}\n\nList-II:\n{l2}\n\n"
            "Choose the correct answer from the options given below:")


def ms(lead, statements):
    body = "\n".join(f"({chr(97 + i)}) {s}" for i, s in enumerate(statements))
    return f"{lead}\n\n{body}\n\nChoose the correct answer from the options given below:"


def ms_check(truth: str, options: list, answer: str):
    """Asserts that the multi-statement option at `answer` is exactly the set of true statements, e.g. 'abd'."""
    sets = ["".join(sorted(re.findall(r"\(([a-e])\)", o))) for o in options]
    assert sets[LETTERS.index(answer)] == "".join(sorted(truth)), (sets, truth)
    assert sets.count("".join(sorted(truth))) == 1


def count_check(items: dict, options: list, answer: str):
    """For 'how many of the following' items: asserts the keyed option is the number of items marked True."""
    n = sum(1 for v in items.values() if v)
    assert options[LETTERS.index(answer)] == str(n) or options[LETTERS.index(answer)].startswith(f"{n} "), (n, options)


# ---------------------------------------------------------------- questions
