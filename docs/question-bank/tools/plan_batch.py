"""Plans one 1,000-question batch: exact quotas per subject, topic and difficulty, plus ID ranges.

Each batch takes 10% of every subject (200/200/150/150/200/100) with a 30/40/30 difficulty split. Inside a subject the
quota follows the taxonomy weights. Time-sensitive topics (current affairs, current rates, Budget) are excluded until the
final batches, so they are fresh at release; their share goes to the other topics of the same subject.

ID ranges continue from the highest ID already used in batches/*.json, so batches never collide.

    python tools/plan_batch.py 1            # writes batches/plans/BATCH_001_plan.json
"""

import json
import re
import sys
from pathlib import Path

from build_distribution import DIFFS, largest_remainder
from qbank import PREFIX

ROOT = Path(__file__).resolve().parent.parent
PER_BATCH = {"Quantitative Aptitude": 200, "Reasoning Ability": 200, "English Language": 150,
             "General Awareness and Current Affairs": 150, "Banking and Financial Awareness": 200,
             "Computer Knowledge": 100}
TIME_SENSITIVE = ("current affairs", "current values")


def used_ids():
    """Highest question and stimulus number used so far, per prefix."""
    hi = {}
    for f in (ROOT / "batches").glob("*.json"):
        for m in re.finditer(r'"(BANK|STIM)_([A-Z]+)_(\d{6})"', f.read_text(encoding="utf-8")):
            key = (m[1], m[2])
            hi[key] = max(hi.get(key, 0), int(m[3]))
    return hi


def plan(batch_no: int, include_time_sensitive: bool = False):
    taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    hi = used_ids()
    subjects = []
    for s in taxonomy["subjects"]:
        topics = [t for t in s["topics"]
                  if include_time_sensitive or not any(k in t["note"].lower() for k in TIME_SENSITIVE)]
        n = PER_BATCH[s["subject"]]
        per_diff = largest_remainder(n, DIFFS)
        weights = {t["topic"]: t["target"] for t in topics}
        by_diff = {d: largest_remainder(k, weights) for d, k in per_diff.items()}
        rows = [{"topic": t["topic"], "subtopics": t["subtopics"],
                 "quota": {d: by_diff[d][t["topic"]] for d in DIFFS}} for t in topics]
        for r in rows:
            r["total"] = sum(r["quota"].values())
        p = PREFIX[s["subject"]]
        start = hi.get(("BANK", p), 0) + 1
        subjects.append({
            "subject": s["subject"], "total": n, "by_difficulty": per_diff,
            "question_ids": [f"BANK_{p}_{start:06d}", f"BANK_{p}_{start + n - 1:06d}"],
            "stimulus_id_start": f"STIM_{p}_{hi.get(('STIM', p), 0) + 1:06d}",
            "topics": [r for r in rows if r["total"]],
        })
    out = {"batch_id": f"BATCH_{batch_no:03d}", "total": sum(PER_BATCH.values()),
           "time_sensitive_included": include_time_sensitive, "subjects": subjects}
    assert out["total"] == 1000 and all(sum(r["total"] for r in s["topics"]) == s["total"] for s in subjects)
    path = ROOT / "batches" / "plans" / f"BATCH_{batch_no:03d}_plan.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path, out


def plan_remaining(first: int, last: int):
    """Plans batches first..last so that, with the sample and every earlier plan, each (subject, topic, difficulty)
    reaches its taxonomy target exactly.

    The remaining slots of each subject are interleaved round-robin across topics and difficulties and then dealt
    to the batches in turn, so every batch gets an even spread (each count within one of the others). IDs are
    contiguous per subject in batch order; stimulus IDs start at <batch> * 1000 + 1 so lanes never collide.
    """
    from collections import Counter

    taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    done, last_id = Counter(), {}
    for f in (ROOT / "batches").glob("BATCH_000*.json"):
        for q in json.loads(f.read_text(encoding="utf-8"))["questions"]:
            done[(q["subject"], q["topic"], q["difficulty"])] += 1
    for k in range(1, first):
        p = json.loads((ROOT / "batches" / "plans" / f"BATCH_{k:03d}_plan.json").read_text(encoding="utf-8"))
        for s in p["subjects"]:
            last_id[s["subject"]] = int(s["question_ids"][1][-6:])
            for t in s["topics"]:
                for d, n in t["quota"].items():
                    done[(s["subject"], t["topic"], d)] += n
    r = last - first + 1
    plans = {k: {"batch_id": f"BATCH_{k:03d}", "time_sensitive_included": True, "subjects": []}
             for k in range(first, last + 1)}
    for s in taxonomy["subjects"]:
        subj, p = s["subject"], PREFIX[s["subject"]]
        cells = [(t["topic"], d, t["by_difficulty"][d] - done[(subj, t["topic"], d)])
                 for t in s["topics"] for d in DIFFS]
        assert all(n >= 0 for *_, n in cells), cells
        # one round-robin list per difficulty, concatenated: dealing a single running index then spreads every
        # difficulty (and every topic) evenly, instead of locking each difficulty to the same batches
        slots = []
        for d in DIFFS:
            left = {(t, dd): n for t, dd, n in cells if dd == d}
            while any(left.values()):
                for key in left:
                    if left[key]:
                        slots.append(key)
                        left[key] -= 1
        dealt = {k: Counter() for k in plans}
        for i, key in enumerate(slots):
            dealt[first + i % r][key] += 1
        nxt = last_id.get(subj, 0) + 1
        for k in plans:
            n = sum(dealt[k].values())
            topics = []
            for t in s["topics"]:
                quota = {d: dealt[k][(t["topic"], d)] for d in DIFFS}
                if sum(quota.values()):
                    topics.append({"topic": t["topic"], "subtopics": t["subtopics"], "quota": quota,
                                   "total": sum(quota.values())})
            plans[k]["subjects"].append({
                "subject": subj, "total": n,
                "by_difficulty": {d: sum(c for (_, dd), c in dealt[k].items() if dd == d) for d in DIFFS},
                "question_ids": [f"BANK_{p}_{nxt:06d}", f"BANK_{p}_{nxt + n - 1:06d}"],
                "stimulus_id_start": f"STIM_{p}_{k * 1000 + 1:06d}",
                "topics": topics})
            nxt += n
    for k, pl in plans.items():
        pl["total"] = sum(s["total"] for s in pl["subjects"])
        (ROOT / "batches" / "plans" / f"BATCH_{k:03d}_plan.json").write_text(
            json.dumps(pl, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(pl["batch_id"], pl["total"], {s["subject"][:12]: s["total"] for s in pl["subjects"]})
    grand = sum(done.values()) + sum(pl["total"] for pl in plans.values())
    print("bank total after these batches:", grand)
    assert grand == taxonomy["total"]


if __name__ == "__main__":
    if sys.argv[1] == "--remaining":
        plan_remaining(int(sys.argv[2]), int(sys.argv[3]))
        sys.exit()
    path, out = plan(int(sys.argv[1]), "--time-sensitive" in sys.argv)
    for s in out["subjects"]:
        print(f'{s["subject"]:40} {s["total"]:4} {s["by_difficulty"]} ids {s["question_ids"]} '
              f'stim from {s["stimulus_id_start"]} topics {len(s["topics"])}')
    print("wrote", path)
