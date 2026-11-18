"""Validator and manifest builder for PrepMitra NEET (UG) question batches (stdlib only).

    python docs/neet-bank/tools/qbank.py validate docs/neet-bank/batches/*.json
    python docs/neet-bank/tools/qbank.py manifest docs/neet-bank/batches/*.json

Same approach as the banking validator (docs/question-bank/tools/qbank.py): checks every file against
question.schema.json plus the rules a JSON Schema cannot express (section mapping, topic in the NMC-based taxonomy,
fixed option sets for assertion-reason / two-statement questions, match-list codes, source honesty, duplicates across
all files). Exits 1 on any error. Near-duplicates are warnings for a human reviewer.
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
PREFIX = {"Physics": "PHY", "Chemistry": "CHE", "Botany": "BOT", "Zoology": "ZOO"}
SECTION = {"Physics": "physics", "Chemistry": "chemistry", "Botany": "botany", "Zoology": "zoology"}
DIFFICULTIES = {"Basic", "Intermediate", "Advanced"}
FORMATS = {"direct", "numerical", "assertion_reason", "statement_pair", "match_list", "multi_statement"}
REVIEW = {"Draft", "Pending Human Review", "Approved", "Rejected"}
SOURCE_TYPES = {"Original", "Official PYQ", "Licensed"}
STIMULUS_TYPES = {"data_table", "experiment", "passage"}
NEAR_DUP = 0.92
REQUIRED = ["question_id", "exam_mappings", "subject", "topic", "subtopic", "difficulty", "question_type", "format",
            "language", "question_text", "options", "correct_answer", "solution", "suggested_time_seconds", "source",
            "verification"]

# Fixed option sets, in this order, so students meet the same wording every time (as in the NEET paper).
ASSERTION_REASON = [
    "Both A and R are true and R is the correct explanation of A.",
    "Both A and R are true but R is NOT the correct explanation of A.",
    "A is true but R is false.",
    "A is false but R is true.",
]
STATEMENT_PAIR = [
    "Both Statement I and Statement II are true.",
    "Both Statement I and Statement II are false.",
    "Statement I is true but Statement II is false.",
    "Statement I is false but Statement II is true.",
]
MATCH_CODE = re.compile(r"^A-(I|II|III|IV), B-(I|II|III|IV), C-(I|II|III|IV), D-(I|II|III|IV)$")


def default_mappings(subject: str) -> list:
    return [{"exam_id": "NEET_UG", "stage": "UG", "section_key": SECTION[subject]}]


def load_reference():
    patterns = json.loads((ROOT / "exam_patterns.json").read_text(encoding="utf-8"))
    sections = {}
    for exam in patterns["exams"]:
        for stage in exam["stages"]:
            for sec in stage["sections"]:
                sections[(exam["exam_id"], stage["stage"], sec["section_key"])] = set(sec["subjects"])
    taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
    topics = {s["subject"]: {t["topic"]: set(t["subtopics"]) for t in s["topics"]} for s in taxonomy["subjects"]}
    return sections, topics


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[,;!?\"'“”‘’()\[\]{}]+|(?<!\d)\.|\.(?!\d)", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fingerprint(q: dict) -> str:
    opts = sorted(normalize(o["text"]) for o in q.get("options", []))
    return " | ".join([normalize(q.get("question_text", "")), *opts, q.get("stimulus_id") or ""])


def is_date(v) -> bool:
    try:
        dt.date.fromisoformat(v)
        return True
    except (TypeError, ValueError):
        return False


def check_format(q, e):
    fmt, texts, stem = q["format"], [o.get("text", "") for o in q["options"]], q["question_text"]
    if fmt == "assertion_reason":
        if texts != ASSERTION_REASON:
            e("assertion_reason options must be the fixed set, in order (see qbank.ASSERTION_REASON)")
        if "Assertion (A):" not in stem or "Reason (R):" not in stem:
            e("assertion_reason stem needs 'Assertion (A):' and 'Reason (R):'")
    elif fmt == "statement_pair":
        if texts != STATEMENT_PAIR:
            e("statement_pair options must be the fixed set, in order (see qbank.STATEMENT_PAIR)")
        if "Statement I:" not in stem or "Statement II:" not in stem:
            e("statement_pair stem needs 'Statement I:' and 'Statement II:'")
    elif fmt == "match_list":
        if "List-I" not in stem or "List-II" not in stem:
            e("match_list stem needs List-I and List-II")
        for t in texts:
            m = MATCH_CODE.match(t)
            if not m:
                e(f"match_list option {t!r} must look like 'A-II, B-III, C-I, D-IV'")
            elif len(set(m.groups())) != 4:
                e(f"match_list option {t!r} must use each of I-IV once")


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
    if not re.fullmatch(rf"NEET_{PREFIX[subject]}_\d{{6}}", qid):
        e(f"id must be NEET_{PREFIX[subject]}_NNNNNN for {subject}")
    if q["topic"] not in ctx_topics[subject]:
        e(f"topic {q['topic']!r} is not in taxonomy.json for {subject}")
    elif q["subtopic"] not in ctx_topics[subject][q["topic"]]:
        w(f"subtopic {q['subtopic']!r} is not listed under {q['topic']!r} in taxonomy.json")
    if q["difficulty"] not in DIFFICULTIES:
        e(f"difficulty {q['difficulty']!r}")
    if q["format"] not in FORMATS:
        e(f"format {q['format']!r}")
    if q["question_type"] != "MCQ" or q["language"] != "en":
        e("question_type must be MCQ and language en")
    if len(q["question_text"].strip()) < 10:
        e("question_text too short")

    opts = q["options"]
    keys = [o.get("key") for o in opts]
    if keys != list("ABCD"):
        e(f"options must be exactly 4 with keys A, B, C, D in order (got {keys})")
    # case matters here: genotypes (TT, Tt, tt) and formulas (CO, Co) are different options
    texts = [re.sub(r"\s+", " ", o.get("text", "")).strip() for o in opts]
    if any(not t for t in texts) or len(set(texts)) != len(texts):
        e("options must be non-empty and distinct")
    if q["correct_answer"] not in keys:
        e(f"correct_answer {q['correct_answer']!r} is not an option key")
    if q["format"] in FORMATS:
        check_format(q, e)

    sol = q["solution"]
    for k in ("concept", "explanation", "steps", "final_answer"):
        if not sol.get(k):
            e(f"solution.{k} is empty")
    if sol.get("final_answer") and not sol["final_answer"].startswith(f"Option {q['correct_answer']}"):
        e(f"solution.final_answer must start with 'Option {q['correct_answer']}'")
    if subject in ("Botany", "Zoology") and not sol.get("ncert_reference"):
        w("biology question without solution.ncert_reference")
    if not 20 <= q["suggested_time_seconds"] <= 180:
        e("suggested_time_seconds must be 20-180")

    for m in q["exam_mappings"]:
        key = (m.get("exam_id"), m.get("stage"), m.get("section_key"))
        if key not in ctx_sections:
            e(f"exam mapping {key} does not exist in exam_patterns.json")
        elif subject not in ctx_sections[key]:
            e(f"section {key} does not test {subject}")

    if "stimulus_id" in q:
        if q["stimulus_id"] not in ctx_stimuli:
            e(f"stimulus {q['stimulus_id']} is not defined in this file")
        if not isinstance(q.get("set_position"), int):
            e("set_position is required with stimulus_id")

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
    for c in v.get("fact_checks") or []:
        if not str(c.get("source_url", "")).startswith("http") or not is_date(c.get("checked_on")):
            e("fact_check needs source_url (http...) and checked_on date")


def validate(paths):
    global ctx_sections, ctx_topics, ctx_stimuli
    ctx_sections, ctx_topics = load_reference()
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
            ctx_stimuli[s.get("stimulus_id")] = s
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
            all_q.append(q)
        keys = Counter(q.get("correct_answer") for q in doc.get("questions", []))
        n = sum(keys.values())
        if n >= 40 and max(keys.values()) > 0.32 * n:
            warn.append(f"{ctx}: answer keys are unbalanced {dict(sorted(keys.items()))}; aim for about 25% each")

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
    return {
        "total_questions": len(questions),
        "by_subject": dict(Counter(q.get("subject") for q in questions)),
        "by_difficulty": dict(Counter(q.get("difficulty") for q in questions)),
        "by_format": dict(Counter(q.get("format") for q in questions)),
        "by_source_type": dict(Counter(q.get("source", {}).get("source_type") for q in questions)),
        "by_review_status": dict(Counter(q.get("verification", {}).get("review_status") for q in questions)),
    }


def check_package(plan_path, package, questions):
    """Compares a package file with its plan: count per (topic, difficulty), ID range and order."""
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == package for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == package)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((q.get("topic"), q.get("difficulty")) for q in questions)
    problems = [f"{t} / {d}: have {have.get((t, d), 0)}, plan {planned.get((t, d), 0)}"
                for t, d in sorted(set(planned) | set(have)) if have.get((t, d), 0) != planned.get((t, d), 0)]
    lo, hi = pkg["question_ids"]
    prefix, start = lo.rsplit("_", 1)
    expected = [f"{prefix}_{n:06d}" for n in range(int(start), int(hi.rsplit("_", 1)[1]) + 1)]
    if [q.get("question_id") for q in questions] != expected:
        problems.append(f"question_ids must be exactly {lo}..{hi} in order")
    if any(q.get("subject") != subj["subject"] for q in questions):
        problems.append(f"every question must be {subj['subject']}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["validate", "manifest"])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--plan", help="batch plan JSON; with --package, check the LAST file against that package")
    ap.add_argument("--package", help="package name from the plan, e.g. PHY_001_p1")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    err, warn, questions = validate(args.files)
    if args.plan and args.package:
        latest = json.loads(Path(args.files[-1]).read_text(encoding="utf-8")).get("questions", [])
        err += [f"quota: {p}" for p in check_package(args.plan, args.package, latest)]
    for line in warn:
        print("WARN ", line)
    for line in err:
        print("ERROR", line)
    report = summary(questions)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.command == "manifest":
        taxonomy = json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8"))
        manifest = {"generated_on": dt.date.today().isoformat(), "target_total": taxonomy["total"],
                    "files": [Path(f).name for f in args.files], **report,
                    "remaining_to_target": taxonomy["total"] - len(questions), "validation_errors": len(err),
                    "near_duplicate_warnings": sum(1 for x in warn if x.startswith("near-duplicate"))}
        (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {ROOT / 'manifest.json'}")
    print(f"{len(err)} error(s), {len(warn)} warning(s)")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
