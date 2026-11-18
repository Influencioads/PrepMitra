
# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 131
    ids = [x["question_id"] for x in QUESTIONS]
    assert ids[0] == pkg["question_ids"][0] and ids[-1] == pkg["question_ids"][1] and len(set(ids)) == len(ids)
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    assert all(x["subtopic"] in subtopics[x["topic"]] for x in QUESTIONS), \
        [(x["question_id"], x["subtopic"]) for x in QUESTIONS if x["subtopic"] not in subtopics[x["topic"]]]
    assert all(x["solution"]["ncert_reference"] and x["solution"]["why_others_wrong"] for x in QUESTIONS)
    stems = [x["question_text"] for x in QUESTIONS]
    assert len(set(stems)) == len(stems), "duplicate stem"
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert max(keys.values()) - min(keys.values()) <= 3, keys
    for f in (D, ASR, STP, MAT, MUL):
        assert fmts[f] >= 0.08 * len(QUESTIONS), (f, fmts)
    assert 0.03 * len(QUESTIONS) <= fmts[NUM] <= 0.08 * len(QUESTIONS), fmts
    assert all("script:recompute" in x["verification"]["verified_by"] for x in QUESTIONS if x["format"] == NUM)
    assert all(x["suggested_time_seconds"] <= 180 for x in QUESTIONS)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "ZOO_009_p2: 131 original Zoology questions (Neural Control and Coordination, Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers and computed match/count keys re-derived in tools/batch_009/ZOO_009_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
