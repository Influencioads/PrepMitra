
# ---------------------------------------------------------------- package checks and output
PLAN = {T_CC: (5, 6, 5), T_PU: (2, 3, 2), T_GO: (6, 8, 6), T_HC: (5, 6, 5), T_HX: (4, 5, 4), T_OX: (6, 8, 6),
        T_NI: (4, 5, 4), T_BM: (4, 5, 4), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 128, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    assert sum(have.values()) == sum(sum(v) for v in PLAN.values())
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert all(28 <= keys[k] <= 36 for k in LETTERS), keys
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "Package CHE_010_p2: 128 original Chemistry questions (coordination compounds, purification and "
                    "characterisation, basic principles of organic chemistry, hydrocarbons, halogen, oxygen and "
                    "nitrogen compounds, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_010/CHE_010_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
