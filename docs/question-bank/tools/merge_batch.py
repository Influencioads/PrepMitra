"""Merges a batch's subject part files into one import file and writes its summary.

    python tools/merge_batch.py 1

Reads batches/parts/BATCH_001_*.json, writes batches/BATCH_001.json, validates it together with every earlier batch
(duplicates are checked across all of them) and against the batch plan, then writes batches/BATCH_001_SUMMARY.md and
refreshes manifest.json. Nothing is written if validation finds errors.
"""

import json
import random
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from qbank import check_quota, summary, validate

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["QUANT", "REAS", "ENG", "GA", "BFA", "COMP"]
# Options that must keep their place: fixed answer sets (conclusions, data sufficiency, relations, error parts).
FIXED_OPTION = re.compile(r"no (error|improvement|replacement|swap|correction)|only (conclusion|statement|i\b|ii\b)|"
                          r"\bneither\b|\bboth\b|\beither\b|cannot be (established|determined)|not sufficient|"
                          r"\balone\b|none of|all of the above|[xy] [<>=≤≥]|quantity i|\bi and ii\b", re.I)
LETTER_REF = re.compile(r"\b[Oo]ptions? \(?[A-D]\b|\([A-D]\)")


def reshuffle_options(questions: list[dict]) -> int:
    """Several builders placed keys on the least-used letter in rotation, which left runs like A, B, C, D in a row
    (predictable inside a puzzle or passage set). Reorders the options of every question whose options can move
    freely, with a seed per question ID so a re-merge gives the same result. Returns how many questions moved."""
    moved = 0
    for q in questions:
        opts, sol = q["options"], q["solution"]
        texts = " ".join(o["text"] for o in opts)
        prose = " ".join(str(sol.get(k) or "") for k in ("explanation", "why_others_wrong", "shortcut", "concept")) \
            + " ".join(sol["steps"]) + q["question_text"]
        if FIXED_OPTION.search(texts) or LETTER_REF.search(prose):
            continue
        answer = next(o["text"] for o in opts if o["key"] == q["correct_answer"])
        order = [o["text"] for o in opts]
        random.Random(q["question_id"]).shuffle(order)
        letters = [o["key"] for o in opts]
        q["options"] = [{"key": k, "text": t} for k, t in zip(letters, order)]
        q["correct_answer"] = letters[order.index(answer)]
        sol["final_answer"] = f"Option {q['correct_answer']}: {answer}"
        moved += 1
    return moved


def main(batch_no: int):
    bid = f"BATCH_{batch_no:03d}"
    parts = [ROOT / "batches" / "parts" / f"{bid}_{p}.json" for p in ORDER]
    missing = [p.name for p in parts if not p.exists()]
    if missing:
        sys.exit(f"missing part files: {missing}")
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in parts]
    merged = {"schema_version": "1.0", "batch_id": bid, "created_at": docs[0]["created_at"],
              "notes": f"{bid}: merged from {len(parts)} subject parts.",
              "stimuli": [s for d in docs for s in d["stimuli"]],
              "questions": [q for d in docs for q in d["questions"]]}
    print(f"options reshuffled on {reshuffle_options(merged['questions'])} questions")
    out = ROOT / "batches" / f"{bid}.json"
    tmp = out.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    earlier = sorted(p for p in (ROOT / "batches").glob("BATCH_*.json") if p.name < out.name and ".tmp" not in p.name)
    err, warn, questions = validate([*map(str, earlier), str(tmp)])
    plan = ROOT / "batches" / "plans" / f"{bid}_plan.json"
    err += [f"quota: {p}" for p in check_quota(plan, merged["questions"])]
    for line in warn + err:
        print(line)
    if err:
        tmp.unlink()
        sys.exit(f"{len(err)} error(s); {out.name} not written")
    tmp.replace(out)

    qs = merged["questions"]
    s = summary(qs)
    cum = summary(questions)
    keys = Counter(q["correct_answer"] for q in qs)
    topics = Counter((q["subject"], q["topic"]) for q in qs)
    md = [f"# {bid} summary", "",
          f"- Questions: **{len(qs)}** (stimuli/sets: {len(merged['stimuli'])})",
          f"- Validation: 0 errors, {len(warn)} warning(s), checked together with {', '.join(p.name for p in earlier)}",
          f"- Answer keys: {dict(sorted(keys.items()))}",
          f"- Source types: {s['by_source_type']}",
          f"- Review status: {s['by_review_status']} (served to students only after human approval)", "",
          "## By subject and difficulty", "", "| Subject | Basic | Intermediate | Advanced | Total |",
          "|---|---:|---:|---:|---:|"]
    for subj in s["by_subject"]:
        c = Counter(q["difficulty"] for q in qs if q["subject"] == subj)
        md.append(f"| {subj} | {c['Basic']} | {c['Intermediate']} | {c['Advanced']} | {sum(c.values())} |")
    d = s["by_difficulty"]
    md += [f"| **Total** | **{d.get('Basic', 0)}** | **{d.get('Intermediate', 0)}** | **{d.get('Advanced', 0)}** "
           f"| **{len(qs)}** |", "", "## By exam (questions mapped; one question can map to several exams)", "",
           "| Exam | Questions |", "|---|---:|"]
    md += [f"| {e} | {n} |" for e, n in s["by_exam"].items()]
    md += ["", "## By topic", "", "| Subject | Topic | Questions |", "|---|---|---:|"]
    md += [f"| {a} | {b} | {n} |" for (a, b), n in sorted(topics.items())]
    md += ["", "## Cumulative (all batches including the BATCH_000 sample)", "",
           f"- Total: **{cum['total_questions']}** of 10,000", f"- By subject: {cum['by_subject']}",
           f"- By difficulty: {cum['by_difficulty']}", f"- Review status: {cum['by_review_status']}"]
    if warn:
        md += ["", "## Warnings", ""] + [f"- {w}" for w in warn]
    (ROOT / "batches" / f"{bid}_SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    all_batches = sorted(str(p) for p in (ROOT / "batches").glob("BATCH_*.json"))
    subprocess.run([sys.executable, str(Path(__file__).with_name("qbank.py")), "manifest", *all_batches],
                   check=True, stdout=subprocess.DEVNULL)
    print(f"wrote {out.name}, {bid}_SUMMARY.md and manifest.json")


if __name__ == "__main__":
    main(int(sys.argv[1]))
