"""Splits a subject's remaining batches into topic packages that separate agents can write in parallel, and joins the
fragments back into the normal part files.

A package is a contiguous group of the subject's topics, covering every remaining batch. Because packages never share
a topic, two agents working at once cannot duplicate each other, and each agent only has to read earlier questions of
its own topics. Inside each batch, the subject's planned ID range is cut into contiguous sub-ranges, one per package,
in package order; stimuli of package g in batch k start at k*1000 + 100*g + 1.

    python tools/packages.py plan REAS 7 10 4      # writes batches/plans/packages/REAS_pkg1.json ... pkg4.json
    python tools/packages.py join 7 REAS           # fragments of batch 7 -> batches/parts/BATCH_007_REAS.json
"""

import json
import sys
from pathlib import Path

from qbank import PREFIX

ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = ROOT / "batches" / "plans" / "packages"
FRAG_DIR = ROOT / "batches" / "parts" / "frag"
SUBJECT = {v: k for k, v in PREFIX.items()}


def load_plan(k):
    return json.loads((ROOT / "batches" / "plans" / f"BATCH_{k:03d}_plan.json").read_text(encoding="utf-8"))


def plan(prefix, first, last, groups):
    subject = SUBJECT[prefix]
    per_batch = {k: next(s for s in load_plan(k)["subjects"] if s["subject"] == subject) for k in range(first, last + 1)}
    # topic order from the taxonomy keeps related topics (all puzzles, all DI ...) in the same package
    taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    order = [t["topic"] for s in taxonomy["subjects"] if s["subject"] == subject for t in s["topics"]]
    totals = {t: sum(r["total"] for s in per_batch.values() for r in s["topics"] if r["topic"] == t) for t in order}
    order = [t for t in order if totals[t]]
    target = sum(totals.values()) / groups
    packs, cur, acc = [], [], 0
    for t in order:
        if cur and acc + totals[t] / 2 > target * (len(packs) + 1) and len(packs) < groups - 1:
            packs.append(cur)
            cur = []
        cur.append(t)
        acc += totals[t]
    packs.append(cur)

    PKG_DIR.mkdir(parents=True, exist_ok=True)
    FRAG_DIR.mkdir(parents=True, exist_ok=True)
    next_id = {k: int(s["question_ids"][0][-6:]) for k, s in per_batch.items()}
    for g, topics in enumerate(packs, 1):
        batches = {}
        for k, s in per_batch.items():
            rows = [r for r in s["topics"] if r["topic"] in topics]
            n = sum(r["total"] for r in rows)
            lo = next_id[k]
            next_id[k] += n
            batches[f"{k:03d}"] = {
                "batch_id": f"BATCH_{k:03d}", "count": n,
                "by_difficulty": {d: sum(r["quota"][d] for r in rows) for d in ("Basic", "Intermediate", "Advanced")},
                "question_ids": [f"BANK_{prefix}_{lo:06d}", f"BANK_{prefix}_{lo + n - 1:06d}"],
                "stimulus_id_start": f"STIM_{prefix}_{k * 1000 + 100 * g + 1:06d}",
                "topics": rows,
                "output": f"batches/parts/frag/BATCH_{k:03d}_{prefix}_pkg{g}.json",
            }
        pkg = {"subject": subject, "prefix": prefix, "package": g, "topics": topics,
               "total": sum(b["count"] for b in batches.values()), "batches": batches}
        (PKG_DIR / f"{prefix}_pkg{g}.json").write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n",
                                                       encoding="utf-8")
        print(f"{prefix}_pkg{g}: {pkg['total']} questions, topics: {', '.join(topics)}")
    for k, s in per_batch.items():  # every ID of the subject's batch range is assigned exactly once
        assert next_id[k] == int(s["question_ids"][1][-6:]) + 1, (k, next_id[k], s["question_ids"])


def join(k, prefix):
    frags = sorted(FRAG_DIR.glob(f"BATCH_{k:03d}_{prefix}_pkg*.json"), key=lambda p: int(p.stem.split("pkg")[1]))
    expected = sorted(PKG_DIR.glob(f"{prefix}_pkg*.json"))
    missing = [p.stem for p in expected if not (FRAG_DIR / f"BATCH_{k:03d}_{p.stem}.json").exists()]
    if missing:
        sys.exit(f"missing fragments for batch {k}: {missing}")
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in frags]
    qs = [q for d in docs for q in d["questions"]]
    ids = [int(q["question_id"][-6:]) for q in qs]
    assert ids == list(range(ids[0], ids[0] + len(ids))), "fragment IDs are not contiguous"
    out = {"schema_version": "1.0", "batch_id": f"BATCH_{k:03d}", "created_at": docs[0]["created_at"],
           "notes": f"Joined from {len(docs)} topic packages: " + " | ".join(d.get("notes", "") for d in docs),
           "stimuli": [s for d in docs for s in d["stimuli"]], "questions": qs}
    path = ROOT / "batches" / "parts" / f"BATCH_{k:03d}_{prefix}.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {path.name}: {len(qs)} questions from {len(docs)} fragments")


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    else:
        join(int(sys.argv[2]), sys.argv[3])
