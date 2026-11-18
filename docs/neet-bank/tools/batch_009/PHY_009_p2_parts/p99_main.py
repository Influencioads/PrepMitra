

# ================================================================ checks and output
def main():
    for i, x in enumerate(QS):
        x["question_id"] = f"NEET_PHY_{FIRST_ID + i:06d}"
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    assert ROOT / pkg["output"] == OUT
    lo, hi = pkg["question_ids"]
    assert QS[0]["question_id"] == lo and QS[-1]["question_id"] == hi, (QS[0]["question_id"], QS[-1]["question_id"])
    quota = {(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"] for d, n in t["quota"].items()}
    subs = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    have = Counter((x["topic"], x["difficulty"]) for x in QS)
    assert have == Counter(quota), {k: (have.get(k), v) for k, v in quota.items() if have.get(k) != v}
    assert len(QS) == pkg["count"] == COUNT
    for x in QS:
        assert x["subtopic"] in subs[x["topic"]], (x["question_id"], x["subtopic"])
    order = [x["topic"] for x in QS]
    assert order == sorted(order, key=pkg["topics"].index)
    fmts = Counter(x["format"] for x in QS)
    assert 0.53 <= fmts["numerical"] / len(QS) <= 0.58, fmts
    for f_ in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f_] >= 0.08 * len(QS), (f_, fmts)
    keys = Counter(x["correct_answer"] for x in QS)
    assert all(31 <= keys[k] <= 36 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "Package PHY_009_p2: 133 original Physics questions (Electrostatics to Experimental Skills), "
                    "NEET_PHY_002118..002250. Numerical answers recomputed by tools/batch_009/PHY_009_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
