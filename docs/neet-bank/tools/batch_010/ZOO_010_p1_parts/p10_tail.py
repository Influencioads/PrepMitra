PLAN = ROOT / "batches" / "plans" / f"{BATCH}_plan.json"
OUT = ROOT / "batches" / "parts" / f"{BATCH}_ZOO_p1.json"


def check_plan():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if s["subject"] == ZOO)
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, (have - planned, planned - have)
    assert len(QUESTIONS) == pkg["count"] == LAST_ID - FIRST_ID + 1
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_ZOO_{n:06d}" for n in range(FIRST_ID, LAST_ID + 1)]
    assert pkg["question_ids"] == [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]]
    assert pkg["output"] == f"batches/parts/{BATCH}_ZOO_p1.json"
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    for x in QUESTIONS:
        assert x["subtopic"] in subtopics[x["topic"]], (x["question_id"], x["subtopic"])


if __name__ == "__main__":
    check_plan()
    n = len(QUESTIONS)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert all(0.22 * n <= keys[k] <= 0.28 * n for k in LETTERS), keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    for f in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f] >= 0.08 * n, (f, fmts)
    assert 0.04 * n <= fmts["numerical"] <= 0.08 * n, fmts
    for x in QUESTIONS:
        if x["format"] == "numerical":
            assert "script:recompute" in x["verification"]["verified_by"], x["question_id"]
        else:
            assert "script:recompute" not in x["verification"]["verified_by"], x["question_id"]
    stems = [x["question_text"] for x in QUESTIONS]
    assert len(set(stems)) == n
    doc = {"schema_version": "1.0", "batch_id": BATCH, "created_at": TODAY,
           "notes": "BATCH_010 package ZOO_010_p1: 131 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, Neural Control "
                    "and Coordination, and Chemical Coordination and Integration. Facts from the rationalised NCERT "
                    "Class 11 Biology textbook, avoiding questions already asked in BATCH_000-BATCH_009 (many items "
                    "are counting, comparison or scenario questions that combine NCERT statements); every numerical "
                    "answer re-derived by tools/batch_010/ZOO_010_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
