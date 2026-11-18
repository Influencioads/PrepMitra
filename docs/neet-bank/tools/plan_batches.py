"""Plans all ten NEET batches at once: exact quotas per subject, topic and difficulty, ID ranges and author packages.

Batch 1 holds 245 questions per subject (the 5 samples in BATCH_000 make it 250), batches 2-10 hold 250, so the bank
ends at exactly 10,000 with every taxonomy cell met. Each subject's ID range for batch k ends at k*250, so ranges never
collide (NEET_PHY_000006..000250 in batch 1, 000251..000500 in batch 2, ...).

Inside a batch, each subject is split into PACKS author packages by contiguous topic groups (taxonomy order), each
with its own contiguous ID sub-range, so authors working at the same time never share a topic or an ID.

    python tools/plan_batches.py          # writes batches/plans/BATCH_001_plan.json .. BATCH_010_plan.json
"""

import json
from collections import Counter
from pathlib import Path

from build_distribution import largest_remainder
from qbank import PREFIX

ROOT = Path(__file__).resolve().parent.parent
BATCHES = 10
PER_SUBJECT = 250
PACKS = 2
DIFFS = ("Basic", "Intermediate", "Advanced")


def written() -> Counter:
    out = Counter()
    for q in json.loads((ROOT / "batches" / "BATCH_000_sample.json").read_text(encoding="utf-8"))["questions"]:
        out[(q["subject"], q["topic"], q["difficulty"])] += 1
    return out


def split_packs(topics: list[dict], packs: int) -> list[list[dict]]:
    total = sum(t["total"] for t in topics)
    out, cur, acc = [], [], 0
    for t in topics:
        if cur and acc + t["total"] / 2 > total * (len(out) + 1) / packs and len(out) < packs - 1:
            out.append(cur)
            cur = []
        cur.append(t)
        acc += t["total"]
    out.append(cur)
    return out


def build():
    taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    done = written()
    plans = {k: {"batch_id": f"BATCH_{k:03d}", "subjects": []} for k in range(1, BATCHES + 1)}
    for s in taxonomy["subjects"]:
        subj, prefix = s["subject"], PREFIX[s["subject"]]
        remaining = {(t["topic"], d): t["by_difficulty"][d] - done[(subj, t["topic"], d)]
                     for t in s["topics"] for d in DIFFS}
        assert min(remaining.values()) >= 0
        first_id = 1 + sum(n for (sj, _, _), n in done.items() if sj == subj)
        for k in range(1, BATCHES + 1):
            size = k * PER_SUBJECT - first_id + 1  # batch 1 absorbs the samples
            left = BATCHES - k + 1
            if left == 1:
                quota = dict(remaining)
            else:
                quota = largest_remainder(size, {c: n for c, n in remaining.items() if n}) | \
                    {c: 0 for c, n in remaining.items() if not n}
                over = {c: quota[c] - remaining[c] for c in quota if quota[c] > remaining[c]}
                assert not over, over
            assert sum(quota.values()) == size
            for c in quota:
                remaining[c] -= quota[c]
            topics = [{"topic": t["topic"], "subtopics": t["subtopics"],
                       "quota": {d: quota[(t["topic"], d)] for d in DIFFS},
                       "total": sum(quota[(t["topic"], d)] for d in DIFFS)} for t in s["topics"]]
            topics = [t for t in topics if t["total"]]
            packs, nxt = [], first_id
            for g, group in enumerate(split_packs(topics, PACKS), 1):
                n = sum(t["total"] for t in group)
                packs.append({"package": f"{prefix}_{k:03d}_p{g}", "topics": [t["topic"] for t in group],
                              "count": n, "question_ids": [f"NEET_{prefix}_{nxt:06d}", f"NEET_{prefix}_{nxt + n - 1:06d}"],
                              "output": f"batches/parts/BATCH_{k:03d}_{prefix}_p{g}.json"})
                nxt += n
            assert nxt == first_id + size
            plans[k]["subjects"].append({
                "subject": subj, "prefix": prefix, "total": size,
                "by_difficulty": {d: sum(t["quota"][d] for t in topics) for d in DIFFS},
                "question_ids": [f"NEET_{prefix}_{first_id:06d}", f"NEET_{prefix}_{first_id + size - 1:06d}"],
                "topics": topics, "packages": packs})
            first_id += size
        assert all(v == 0 for v in remaining.values())
    out = ROOT / "batches" / "plans"
    out.mkdir(parents=True, exist_ok=True)
    for k, p in plans.items():
        p["total"] = sum(s["total"] for s in p["subjects"])
        (out / f"BATCH_{k:03d}_plan.json").write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n",
                                                      encoding="utf-8")
    return plans


if __name__ == "__main__":
    for k, p in build().items():
        print(p["batch_id"], p["total"], {s["prefix"]: [x["count"] for x in s["packages"]] for s in p["subjects"]})
