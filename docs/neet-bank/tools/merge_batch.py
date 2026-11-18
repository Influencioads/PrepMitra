"""Joins a batch's package files into batches/BATCH_<NNN>.json, and runs the blind check bookkeeping.

    python tools/merge_batch.py 1                     # parts/BATCH_001_*_p*.json -> BATCH_001.json (checks the plan)
    python tools/merge_batch.py dump 1 PHY_001_p1     # key-free text of one package for a blind solver
    python tools/merge_batch.py stems 2 PHY_002_p1    # stems + answers of EARLIER questions on that package's topics
    python tools/merge_batch.py apply 1 PHY_001_p1 answers.txt
        # answers.txt has lines "NEET_PHY_000006 | B | ...". Tags ai:independent-check on every match and prints the
        # mismatches; a mismatched question must be fixed by its author and re-checked before it is tagged.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / "batches" / "parts"


def plan(k):
    return json.loads((ROOT / "batches" / "plans" / f"BATCH_{k:03d}_plan.json").read_text(encoding="utf-8"))


def package_path(k, package):
    for s in plan(k)["subjects"]:
        for p in s["packages"]:
            if p["package"] == package:
                return ROOT / p["output"]
    raise SystemExit(f"no package {package} in batch {k}")


def merge(k):
    p = plan(k)
    questions, stimuli = [], []
    for s in p["subjects"]:
        for pkg in s["packages"]:
            doc = json.loads((ROOT / pkg["output"]).read_text(encoding="utf-8"))
            assert len(doc["questions"]) == pkg["count"], (pkg["package"], len(doc["questions"]), pkg["count"])
            questions += doc["questions"]
            stimuli += doc.get("stimuli", [])
    assert len(questions) == p["total"]
    out = ROOT / "batches" / f"BATCH_{k:03d}.json"
    out.write_text(json.dumps({"schema_version": "1.0", "batch_id": f"BATCH_{k:03d}",
                               "created_at": questions[0]["verification"]["verified_at"],
                               "notes": f"Merged from {sum(len(s['packages']) for s in p['subjects'])} package files.",
                               "stimuli": stimuli, "questions": questions}, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {out}: {len(questions)} questions")


def dump(k, package):
    doc = json.loads(package_path(k, package).read_text(encoding="utf-8"))
    stim = {s["stimulus_id"]: s for s in doc.get("stimuli", [])}
    blocks = []
    for q in doc["questions"]:
        head = f"{stim[q['stimulus_id']]['content']}\n\n" if q.get("stimulus_id") in stim else ""
        blocks.append(f"{q['question_id']}\n{head}{q['question_text']}\n" +
                      "\n".join(f"{o['key']}) {o['text']}" for o in q["options"]))
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n\n-----\n\n".join(blocks))


def apply(k, package, answers_file):
    path = package_path(k, package)
    doc = json.loads(path.read_text(encoding="utf-8"))
    given = {}
    for line in Path(answers_file).read_text(encoding="utf-8").splitlines():
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 2 and parts[0].startswith("NEET_") and parts[1] in ("A", "B", "C", "D"):
            given[parts[0]] = parts[1]
    matched, mismatched, missing = 0, [], []
    for q in doc["questions"]:
        tags = q["verification"]["verified_by"]
        if q["question_id"] not in given:
            missing.append(q["question_id"])
        elif given[q["question_id"]] == q["correct_answer"]:
            matched += 1
            if "ai:independent-check" not in tags:
                tags.append("ai:independent-check")
        else:
            mismatched.append(f"{q['question_id']}: key {q['correct_answer']}, blind {given[q['question_id']]}")
            if "ai:independent-check" in tags:
                tags.remove("ai:independent-check")
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{package}: {matched} matched, {len(mismatched)} mismatched, {len(missing)} not answered")
    for m in mismatched:
        print("MISMATCH", m)


def stems(k, package):
    """Earlier questions (sample + merged batches + part files of earlier batches) on this package's topics."""
    pkg = next(p for s in plan(k)["subjects"] for p in s["packages"] if p["package"] == package)
    files = [ROOT / "batches" / "BATCH_000_sample.json"]
    for j in range(1, k):
        merged = ROOT / "batches" / f"BATCH_{j:03d}.json"
        files += [merged] if merged.exists() else sorted(PARTS.glob(f"BATCH_{j:03d}_*.json"))
    sys.stdout.reconfigure(encoding="utf-8")
    n = 0
    for f in files:
        for q in json.loads(f.read_text(encoding="utf-8"))["questions"]:
            if q["topic"] in pkg["topics"] and q["question_id"].split("_")[1] == package.split("_")[0]:
                ans = next(o["text"] for o in q["options"] if o["key"] == q["correct_answer"])
                print(f"[{q['question_id']} | {q['topic']} | {q['format']}] {q['question_text']}\n  -> {ans}\n")
                n += 1
    print(f"{n} earlier questions on these topics")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "dump":
        dump(int(a[1]), a[2])
    elif a[0] == "stems":
        stems(int(a[1]), a[2])
    elif a[0] == "apply":
        apply(int(a[1]), a[2], a[3])
    else:
        merge(int(a[0]))
