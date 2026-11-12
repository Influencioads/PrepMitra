"""Validator and manifest builder for PrepMitra banking question batches (stdlib only).

    python docs/question-bank/tools/qbank.py validate docs/question-bank/batches/*.json
    python docs/question-bank/tools/qbank.py manifest docs/question-bank/batches/*.json

`validate` checks every file against the rules in question.schema.json plus the cross-file rules a JSON Schema cannot
express: exam/section mapping against exam_patterns.json, topic against taxonomy.json, stimulus references,
current-affairs expiry, fact-check presence, source honesty and duplicates across all files given. It exits 1 on any
error. Near-duplicates are warnings for a human reviewer, because same-template quant questions with new numbers can
be legitimate.
"""

import argparse
import datetime as dt
import difflib
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = {"Quantitative Aptitude": "QUANT", "Reasoning Ability": "REAS", "English Language": "ENG",
          "General Awareness and Current Affairs": "GA", "Banking and Financial Awareness": "BFA",
          "Computer Knowledge": "COMP"}
DIFFICULTIES = {"Basic", "Intermediate", "Advanced"}
REVIEW = {"Draft", "Pending Human Review", "Approved", "Rejected"}
SOURCE_TYPES = {"Original", "Official PYQ", "Licensed"}
STIMULUS_TYPES = {"passage", "data_table", "chart", "caselet", "puzzle", "input_output"}
FACT_SUBJECTS = {"General Awareness and Current Affairs", "Banking and Financial Awareness"}
NEAR_DUP = 0.92
REQUIRED = ["question_id", "exam_mappings", "subject", "topic", "subtopic", "difficulty", "question_type", "language",
            "question_text", "options", "correct_answer", "solution", "suggested_time_seconds", "source",
            "verification"]


# Default exam mapping by subject and difficulty: Basic -> clerk/OA level, Intermediate -> PO prelims and clerk mains,
# Advanced -> PO mains. Authors may narrow a question's mappings; the validator checks whatever they choose.
_GA = "ga"
MAPPING_RULES = {
    ("Quantitative Aptitude", "Basic"): [("IBPS_CSA", "Prelims", "numerical"), ("SBI_JA", "Prelims", "numerical"),
                                         ("IBPS_RRB_OA", "Prelims", "numerical")],
    ("Quantitative Aptitude", "Intermediate"): [("IBPS_PO", "Prelims", "quant"), ("SBI_PO", "Prelims", "quant"),
                                                ("IBPS_RRB_OS1", "Prelims", "quant"), ("IBPS_CSA", "Mains", "quant"),
                                                ("SBI_JA", "Mains", "quant"), ("IBPS_RRB_OA", "Mains", "numerical")],
    ("Quantitative Aptitude", "Advanced"): [("IBPS_PO", "Mains", "dai"), ("SBI_PO", "Mains", "dai"),
                                            ("IBPS_RRB_OS1", "Mains", "quant")],
    ("Reasoning Ability", "Basic"): [("IBPS_CSA", "Prelims", "reasoning"), ("SBI_JA", "Prelims", "reasoning"),
                                     ("IBPS_RRB_OA", "Prelims", "reasoning")],
    ("Reasoning Ability", "Intermediate"): [("IBPS_PO", "Prelims", "reasoning"), ("SBI_PO", "Prelims", "reasoning"),
                                            ("IBPS_RRB_OS1", "Prelims", "reasoning"),
                                            ("IBPS_CSA", "Mains", "reasoning"),
                                            ("SBI_JA", "Mains", "reasoning_computer"),
                                            ("IBPS_RRB_OA", "Mains", "reasoning")],
    ("Reasoning Ability", "Advanced"): [("IBPS_PO", "Mains", "reasoning"), ("SBI_PO", "Mains", "reasoning_computer"),
                                        ("IBPS_RRB_OS1", "Mains", "reasoning")],
    ("English Language", "Basic"): [("IBPS_CSA", "Prelims", "english"), ("SBI_JA", "Prelims", "english")],
    ("English Language", "Intermediate"): [("IBPS_PO", "Prelims", "english"), ("SBI_PO", "Prelims", "english"),
                                           ("IBPS_CSA", "Mains", "english"), ("SBI_JA", "Mains", "english"),
                                           ("IBPS_RRB_OS1", "Mains", "language"),
                                           ("IBPS_RRB_OA", "Mains", "language")],
    ("English Language", "Advanced"): [("IBPS_PO", "Mains", "english"), ("SBI_PO", "Mains", "english")],
    ("Computer Knowledge", "Basic"): [("IBPS_RRB_OA", "Mains", "computer"), ("IBPS_RRB_OS1", "Mains", "computer"),
                                      ("SBI_JA", "Mains", "reasoning_computer")],
    ("Computer Knowledge", "Intermediate"): [("IBPS_RRB_OA", "Mains", "computer"),
                                             ("IBPS_RRB_OS1", "Mains", "computer"),
                                             ("SBI_JA", "Mains", "reasoning_computer"),
                                             ("SBI_PO", "Mains", "reasoning_computer")],
    ("Computer Knowledge", "Advanced"): [("SBI_PO", "Mains", "reasoning_computer"),
                                         ("IBPS_RRB_OS1", "Mains", "computer")],
}
for _subject in FACT_SUBJECTS:
    MAPPING_RULES[(_subject, "Basic")] = [(x, "Mains", _GA) for x in ("IBPS_CSA", "SBI_JA", "IBPS_RRB_OA", "IBPS_RRB_OS1")]
    MAPPING_RULES[(_subject, "Intermediate")] = [(x, "Mains", _GA) for x in
                                                 ("IBPS_PO", "SBI_PO", "IBPS_CSA", "SBI_JA", "IBPS_RRB_OS1", "IBPS_RRB_OA")]
    MAPPING_RULES[(_subject, "Advanced")] = [(x, "Mains", _GA) for x in ("IBPS_PO", "SBI_PO", "IBPS_RRB_OS1")]


def default_mappings(subject: str, difficulty: str) -> list:
    return [{"exam_id": e, "stage": s, "section_key": k} for e, s, k in MAPPING_RULES[(subject, difficulty)]]


def load_reference():
    patterns = json.loads((ROOT / "exam_patterns.json").read_text(encoding="utf-8"))
    sections = {}  # (exam_id, stage, section_key) -> subjects
    for exam in patterns["exams"]:
        for stage in exam["stages"]:
            for sec in stage["sections"]:
                sections[(exam["exam_id"], stage["stage"], sec["section_key"])] = set(sec["subjects"])
    taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    topics, ca_topics = {}, set()
    for s in taxonomy["subjects"]:
        for t in s["topics"]:
            topics.setdefault(s["subject"], {})[t["topic"]] = set(t["subtopics"])
            if "current affairs" in t["note"].lower() or "current values" in t["note"].lower():
                ca_topics.add((s["subject"], t["topic"]))
    return sections, topics, ca_topics


def normalize(text: str) -> str:
    """Lower-case, drop punctuation and quotes, keep maths symbols (x > y and x ≥ y must stay different)."""
    text = text.lower().replace("₹", " rs ")
    text = re.sub(r"[,;!?\"'“”‘’()\[\]{}]+|(?<!\d)\.|\.(?!\d)", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fingerprint(q: dict) -> str:
    """Text the duplicate check compares: stem + sorted options + stimulus, so a new data set is a new question."""
    opts = sorted(normalize(o["text"]) for o in q.get("options", []))
    return " | ".join([normalize(q.get("question_text", "")), *opts, q.get("stimulus_id") or ""])


def is_date(v) -> bool:
    try:
        dt.date.fromisoformat(v)
        return True
    except (TypeError, ValueError):
        return False


def check_question(q, ctx, err, warn):
    qid = q.get("question_id", "<no id>")
    e = lambda msg: err.append(f"{ctx}:{qid}: {msg}")
    w = lambda msg: warn.append(f"{ctx}:{qid}: {msg}")
    missing = [k for k in REQUIRED if k not in q]
    if missing:
        return e(f"missing fields {missing}")

    subject = q["subject"]
    if subject not in PREFIX:
        return e(f"unknown subject {subject!r}")
    if not re.fullmatch(rf"BANK_{PREFIX[subject]}_\d{{6}}", qid):
        e(f"id must be BANK_{PREFIX[subject]}_NNNNNN for {subject}")
    if q["topic"] not in ctx_topics[subject]:
        e(f"topic {q['topic']!r} is not in taxonomy.json for {subject}")
    elif q["subtopic"] not in ctx_topics[subject][q["topic"]]:
        w(f"subtopic {q['subtopic']!r} is not listed under {q['topic']!r} in taxonomy.json")
    if q["difficulty"] not in DIFFICULTIES:
        e(f"difficulty {q['difficulty']!r}")
    if q["question_type"] != "MCQ" or q["language"] != "en":
        e("question_type must be MCQ and language en")
    if len(q["question_text"].strip()) < 10:
        e("question_text too short")

    # options: exactly 4 (PrepMitra decision), keys A-D in order, distinct texts, answer among keys
    opts = q["options"]
    keys = [o.get("key") for o in opts]
    if keys != list("ABCD"):
        e(f"options must be exactly 4 with keys A, B, C, D in order (got {keys})")
    texts = [normalize(o.get("text", "")) for o in opts]
    if any(not t for t in texts) or len(set(texts)) != len(texts):
        e("options must be non-empty and distinct")
    if q["correct_answer"] not in keys:
        e(f"correct_answer {q['correct_answer']!r} is not an option key")
    else:
        # a strict relation answer (x > y) must not sit next to its weaker form (x ≥ y), which is also true
        ans = next(o.get("text", "") for o in opts if o.get("key") == q["correct_answer"])
        weak = ans.replace(">", "≥").replace("<", "≤")
        if weak != ans and any(o.get("text") == weak for o in opts):
            e(f"options contain both {ans!r} and the also-true {weak!r}")

    sol = q["solution"]
    for k in ("concept", "explanation", "steps", "final_answer"):
        if not sol.get(k):
            e(f"solution.{k} is empty")
    if sol.get("final_answer") and not sol["final_answer"].startswith(f"Option {q['correct_answer']}"):
        e(f"solution.final_answer must start with 'Option {q['correct_answer']}'")
    if not 10 <= q["suggested_time_seconds"] <= 300:
        e("suggested_time_seconds must be 10-300")

    # exam mappings must point at a real section of that exam stage that tests this subject
    seen = set()
    for m in q["exam_mappings"]:
        key = (m.get("exam_id"), m.get("stage"), m.get("section_key"))
        if key in seen:
            e(f"duplicate exam mapping {key}")
        seen.add(key)
        if key not in ctx_sections:
            e(f"exam mapping {key} does not exist in exam_patterns.json")
        elif subject not in ctx_sections[key]:
            e(f"section {key} does not test {subject}")

    # shared stimulus
    if "stimulus_id" in q:
        if q["stimulus_id"] not in ctx_stimuli:
            e(f"stimulus {q['stimulus_id']} is not defined in this file")
        if not isinstance(q.get("set_position"), int):
            e("set_position is required with stimulus_id")

    # time-sensitive questions carry an event date and a review-by date
    ca = q.get("current_affairs")
    if (subject, q["topic"]) in ctx_ca and not ca:
        e("current_affairs {event_date, review_by} is required for this topic")
    if ca:
        if not (is_date(ca.get("event_date")) and is_date(ca.get("review_by"))):
            e("current_affairs dates must be YYYY-MM-DD")
        elif dt.date.fromisoformat(ca["review_by"]) < TODAY:
            w(f"current-affairs review_by {ca['review_by']} has passed: re-verify before serving")

    # source honesty: original questions never claim an exam year or a URL
    src = q["source"]
    if src.get("source_type") not in SOURCE_TYPES:
        e(f"source_type {src.get('source_type')!r}")
    elif src["source_type"] == "Original":
        if src.get("source_url") or src.get("original_exam_year"):
            e("Original questions must have source_url and original_exam_year null")
    else:
        if not src.get("source_url") or not src.get("license_note"):
            e(f"{src['source_type']} needs source_url and license_note")
        if src["source_type"] == "Official PYQ" and not src.get("original_exam_year"):
            e("Official PYQ needs original_exam_year")

    v = q["verification"]
    if v.get("review_status") not in REVIEW:
        e(f"review_status {v.get('review_status')!r}")
    if not is_date(v.get("verified_at")):
        e("verification.verified_at must be YYYY-MM-DD")
    if v.get("review_status") == "Approved":
        if not any(str(x).startswith("human:") for x in v.get("verified_by", [])):
            e("Approved requires a human: reviewer in verified_by")
        if not (v.get("answer_verified") and v.get("solution_verified")):
            e("Approved requires answer_verified and solution_verified")
    if subject in FACT_SUBJECTS:
        checks = v.get("fact_checks") or []
        if not checks:
            e("GA/Banking questions need at least one fact_check with a source URL")
        for c in checks:
            if not str(c.get("source_url", "")).startswith("http") or not is_date(c.get("checked_on")):
                e("fact_check needs source_url (http...) and checked_on date")


def validate(paths):
    global ctx_sections, ctx_topics, ctx_ca, ctx_stimuli, TODAY
    ctx_sections, ctx_topics, ctx_ca = load_reference()
    TODAY = dt.date.today()
    err, warn, all_q = [], [], []
    ids, hashes = {}, {}
    for path in paths:
        ctx = Path(path).name
        try:
            doc = json.loads(Path(path).read_text(encoding="utf-8"))
        except json.JSONDecodeError as ex:
            err.append(f"{ctx}: invalid JSON: {ex}")
            continue
        if doc.get("schema_version") != "1.0" or not re.fullmatch(r"BATCH_\d{3}", str(doc.get("batch_id"))):
            err.append(f"{ctx}: schema_version must be 1.0 and batch_id BATCH_NNN")
        ctx_stimuli = {}
        for s in doc.get("stimuli", []):
            if s.get("type") not in STIMULUS_TYPES or len(s.get("content", "")) < 20:
                err.append(f"{ctx}:{s.get('stimulus_id')}: bad stimulus type or content")
            if s.get("stimulus_id") in ctx_stimuli:
                err.append(f"{ctx}: duplicate stimulus {s.get('stimulus_id')}")
            ctx_stimuli[s.get("stimulus_id")] = s
        positions = defaultdict(list)
        used = set()
        for q in doc.get("questions", []):
            check_question(q, ctx, err, warn)
            qid = q.get("question_id")
            if qid in ids:
                err.append(f"{ctx}:{qid}: duplicate question_id (also in {ids[qid]})")
            ids[qid] = ctx
            h = hashlib.sha256(fingerprint(q).encode()).hexdigest()
            if h in hashes:
                err.append(f"{ctx}:{qid}: exact duplicate of {hashes[h]}")
            hashes[h] = qid
            if "stimulus_id" in q:
                positions[q["stimulus_id"]].append(q.get("set_position"))
                used.add(q["stimulus_id"])
            all_q.append(q)
        for sid, pos in positions.items():
            if sorted(pos) != list(range(1, len(pos) + 1)):
                err.append(f"{ctx}:{sid}: set_position must run 1..{len(pos)} (got {sorted(pos)})")
        for sid in set(ctx_stimuli) - used:
            warn.append(f"{ctx}:{sid}: stimulus has no questions")
        keys = Counter(q.get("correct_answer") for q in doc.get("questions", []))
        n = sum(keys.values())
        if n >= 40 and max(keys.values()) > 0.32 * n:
            warn.append(f"{ctx}: answer keys are unbalanced {dict(sorted(keys.items()))}; aim for about 25% each")

    # near duplicates: compare only within a subject, and only pairs that share enough word shingles
    by_subject = defaultdict(list)
    for q in all_q:
        by_subject[q.get("subject")].append((q.get("question_id"), fingerprint(q)))
    for items in by_subject.values():
        shingles = {qid: {" ".join(t.split()[i:i + 3]) for i in range(max(1, len(t.split()) - 2))} for qid, t in items}
        index = defaultdict(set)
        for qid, sh in shingles.items():
            for s in sh:
                index[s].add(qid)
        text = dict(items)
        done = set()
        for qid, sh in shingles.items():
            shared = Counter(o for s in sh for o in index[s] if o != qid)
            for other, n in shared.items():
                pair = tuple(sorted((qid, other)))
                if pair in done or n < 0.5 * min(len(sh), len(shingles[other])):
                    continue
                done.add(pair)
                ratio = difflib.SequenceMatcher(None, text[qid], text[other]).ratio()
                if ratio >= NEAR_DUP:
                    warn.append(f"near-duplicate ({ratio:.2f}): {pair[0]} ~ {pair[1]}")
    return err, warn, all_q


def summary(questions):
    exams = Counter(m["exam_id"] for q in questions for m in q.get("exam_mappings", []))
    return {
        "total_questions": len(questions),
        "by_subject": dict(Counter(q.get("subject") for q in questions)),
        "by_difficulty": dict(Counter(q.get("difficulty") for q in questions)),
        "by_exam": dict(sorted(exams.items())),
        "by_source_type": dict(Counter(q.get("source", {}).get("source_type") for q in questions)),
        "by_review_status": dict(Counter(q.get("verification", {}).get("review_status") for q in questions)),
    }


def check_quota(plan_path, questions, subject=None):
    """Compares question counts per (subject, topic, difficulty) and the ID range with a batch plan."""
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    have = Counter((q.get("subject"), q.get("topic"), q.get("difficulty")) for q in questions)
    problems = []
    for s in plan["subjects"]:
        if subject and s["subject"] != subject:
            continue
        lo, hi = s["question_ids"]
        for q in questions:
            if q.get("subject") == s["subject"] and not lo <= q.get("question_id", "") <= hi:
                problems.append(f"{q.get('question_id')} is outside the planned range {lo}..{hi}")
        planned = {(s["subject"], t["topic"], d): n for t in s["topics"] for d, n in t["quota"].items()}
        for key in set(planned) | {k for k in have if k[0] == s["subject"]}:
            if have.get(key, 0) != planned.get(key, 0):
                problems.append(f"{key[1]} / {key[2]}: have {have.get(key, 0)}, plan {planned.get(key, 0)}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["validate", "manifest"])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--plan", help="batch plan JSON: also check topic/difficulty quotas and ID ranges")
    ap.add_argument("--subject", help="with --plan, check only this subject (for a part file)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    err, warn, questions = validate(args.files)
    if args.plan:  # quotas apply to the last file only; earlier files are given for the duplicate check
        latest = json.loads(Path(args.files[-1]).read_text(encoding="utf-8")).get("questions", [])
        err += [f"quota: {p}" for p in sorted(check_quota(args.plan, latest, args.subject))]
    for line in warn:
        print("WARN ", line)
    for line in err:
        print("ERROR", line)
    report = summary(questions)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.command == "manifest":
        taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
        manifest = {
            "generated_on": dt.date.today().isoformat(),
            "target_total": taxonomy["total"],
            "files": [Path(f).name for f in args.files],
            **report,
            "remaining_to_target": taxonomy["total"] - len(questions),
            "validation_errors": len(err),
            "near_duplicate_warnings": sum(1 for x in warn if x.startswith("near-duplicate")),
            "complete": not err and len(questions) == taxonomy["total"]
                        and report["by_review_status"].get("Approved", 0) == taxonomy["total"],
        }
        (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                            encoding="utf-8")
        print(f"wrote {ROOT / 'manifest.json'}")
    print(f"{len(err)} error(s), {len(warn)} warning(s)")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
