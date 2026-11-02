"""Seed data: plans, the proposed launch catalog (PDF 3), interview roles and starter glossary.

    python -m app.seed                 # idempotent upsert
    python -m app.seed --papers 1      # also pre-generate N papers per exam (uses the configured AI provider)

Blueprints follow the publicly known exam patterns at the time of writing; content managers should re-check them
every quarter (PDF 15 risk "official exam pattern changes") and edit them in the admin panel.
The 2 state PSC exams are an open decision in the PDF and are not seeded.
"""

import argparse
import logging

from sqlalchemy import select

from app.ai.embeddings import embed
from app.db import SessionLocal
from app.models import AiLesson, Exam, ExamBlueprint, Glossary, InterviewRole, Plan, Topic

log = logging.getLogger("seed")

TIER1 = ["en", "hi", "bn", "mr", "te", "ta", "gu", "kn", "ml", "or", "pa", "ur"]
ALL = TIER1 + ["as", "ne", "kok", "mai", "sa", "sd", "ks", "doi", "brx", "mni", "sat"]
MIX = {"easy": 30, "medium": 50, "hard": 20}

PLANS = [
    # code, name, price (paise, GST-inclusive), credits, validity days, recurring
    ("free_trial", "Free trial (30-min mini mock)", 0, 1, 30, False),
    ("pay_per_exam", "Pay per exam", 9900, 1, 90, False),
    ("monthly", "Monthly plan", 39900, 10, 30, True),
    ("yearly", "Yearly plan (proposed)", 299900, 150, 365, True),
    ("credit_pack_10", "10-credit pack", 39900, 10, 90, False),
]

T = {  # reusable syllabus topic lists: (name, weightage)
    "reasoning": [("Analogy and classification", 2), ("Coding-decoding", 2), ("Series", 2), ("Blood relations", 1),
                  ("Syllogism", 1), ("Puzzles and seating arrangement", 2)],
    "quant": [("Number system", 2), ("Percentage", 2), ("Profit and loss", 2), ("Ratio and proportion", 1),
              ("Time and work", 1), ("Time, speed and distance", 1), ("Simple and compound interest", 1),
              ("Data interpretation", 2)],
    "advanced_maths": [("Algebra", 2), ("Geometry", 2), ("Trigonometry", 1), ("Mensuration", 1)],
    "english": [("Reading comprehension", 2), ("Error spotting", 2), ("Fill in the blanks", 2),
                ("Synonyms and antonyms", 1), ("Idioms and phrases", 1), ("Sentence improvement", 1)],
    "ga": [("History", 2), ("Polity", 2), ("Geography", 2), ("Economy", 2), ("General science", 2),
           ("Current affairs", 2)],
    "banking_ga": [("Banking awareness", 2), ("Financial awareness", 2), ("Current affairs", 2)],
    "gs_upsc": [("Indian history and culture", 2), ("Indian polity and governance", 2), ("Geography", 2),
                ("Economy", 2), ("Environment and ecology", 2), ("Science and technology", 1), ("Current affairs", 2)],
    "csat": [("Comprehension", 3), ("Logical reasoning", 2), ("Basic numeracy", 2), ("Data interpretation", 1),
             ("Decision making", 1)],
    "varc": [("Reading comprehension", 4), ("Para jumbles", 1), ("Para summary", 1), ("Odd sentence out", 1)],
    "dilr": [("Data interpretation sets", 2), ("Logical reasoning sets", 2), ("Arrangements and games", 1)],
    "qa_cat": [("Arithmetic", 3), ("Algebra", 2), ("Geometry and mensuration", 2), ("Number system", 1),
               ("Modern maths", 1)],
    "ga_gate": [("Verbal aptitude", 1), ("Quantitative aptitude", 1), ("Analytical aptitude", 1), ("Spatial aptitude", 1)],
    "gate_cse": [("Engineering mathematics", 2), ("Digital logic", 1), ("Computer organization", 1),
                 ("Programming and data structures", 2), ("Algorithms", 2), ("Theory of computation", 1),
                 ("Compiler design", 1), ("Operating systems", 1), ("Databases", 1), ("Computer networks", 1)],
    "gate_ece": [("Engineering mathematics", 2), ("Networks, signals and systems", 2), ("Electronic devices", 1),
                 ("Analog circuits", 2), ("Digital circuits", 1), ("Control systems", 1), ("Communications", 2),
                 ("Electromagnetics", 1)],
    "cuet_pg": [("General awareness", 1), ("Language comprehension", 1), ("Analytical reasoning", 1),
                ("Quantitative ability", 1), ("Domain knowledge", 3)],
    "verbal": [("Reading comprehension", 2), ("Grammar", 2), ("Vocabulary", 1), ("Sentence correction", 1)],
}


def S(key, name, n, marks, neg, topics, types=None):
    return {"key": key, "name": name, "question_count": n, "marks_per_question": marks, "negative_marks": neg,
            "question_types": types or {"single": n}, "_topics": topics}


EXAMS = [
    dict(slug="mini-mock-general-aptitude", name="Free Mini Mock - General Aptitude", category="campus_hiring",
         description="A free 30-minute mock with a full AI report, to see how PrepMitra works.", free=True,
         duration=30, langs=ALL, sections=[S("quant", "Quantitative aptitude", 10, 1, 0.25, "quant"),
                                           S("reasoning", "Reasoning", 10, 1, 0.25, "reasoning"),
                                           S("english", "English", 10, 1, 0.25, "english")]),
    dict(slug="ssc-cgl-tier1", name="SSC CGL Tier-1", category="central_govt", duration=60, langs=TIER1,
         description="Mock test based on the SSC CGL Tier-1 pattern: 100 questions, 200 marks, 60 minutes.",
         sections=[S("reasoning", "General Intelligence and Reasoning", 25, 2, 0.5, "reasoning"),
                   S("ga", "General Awareness", 25, 2, 0.5, "ga"),
                   S("quant", "Quantitative Aptitude", 25, 2, 0.5, "quant"),
                   S("english", "English Comprehension", 25, 2, 0.5, "english")]),
    dict(slug="ssc-chsl-tier1", name="SSC CHSL Tier-1", category="central_govt", duration=60, langs=TIER1,
         description="Mock test based on the SSC CHSL Tier-1 pattern.",
         sections=[S("english", "English Language", 25, 2, 0.5, "english"),
                   S("reasoning", "General Intelligence", 25, 2, 0.5, "reasoning"),
                   S("quant", "Quantitative Aptitude", 25, 2, 0.5, "quant"),
                   S("ga", "General Awareness", 25, 2, 0.5, "ga")]),
    dict(slug="rrb-ntpc-cbt1", name="RRB NTPC CBT-1", category="central_govt", duration=90, langs=TIER1,
         description="Mock test based on the RRB NTPC CBT-1 pattern.", calc=False,
         sections=[S("maths", "Mathematics", 30, 1, 1 / 3, "quant"),
                   S("reasoning", "General Intelligence and Reasoning", 30, 1, 1 / 3, "reasoning"),
                   S("ga", "General Awareness", 40, 1, 1 / 3, "ga")]),
    dict(slug="ibps-po-prelims", name="IBPS PO Prelims", category="banking", duration=60, langs=["en", "hi"],
         description="Mock test based on the IBPS PO preliminary exam pattern.",
         sections=[S("english", "English Language", 30, 1, 0.25, "english"),
                   S("quant", "Quantitative Aptitude", 35, 1, 0.25, "quant"),
                   S("reasoning", "Reasoning Ability", 35, 1, 0.25, "reasoning")]),
    dict(slug="ibps-clerk-prelims", name="IBPS Clerk Prelims", category="banking", duration=60, langs=TIER1,
         description="Mock test based on the IBPS Clerk preliminary exam pattern.",
         sections=[S("english", "English Language", 30, 1, 0.25, "english"),
                   S("numerical", "Numerical Ability", 35, 1, 0.25, "quant"),
                   S("reasoning", "Reasoning Ability", 35, 1, 0.25, "reasoning")]),
    dict(slug="sbi-po-prelims", name="SBI PO Prelims", category="banking", duration=60, langs=["en", "hi"],
         description="Mock test based on the SBI PO preliminary exam pattern.",
         sections=[S("english", "English Language", 30, 1, 0.25, "english"),
                   S("quant", "Quantitative Aptitude", 35, 1, 0.25, "quant"),
                   S("reasoning", "Reasoning Ability", 35, 1, 0.25, "reasoning")]),
    dict(slug="upsc-cse-prelims-gs", name="UPSC CSE Prelims - GS Paper I", category="civil_services", duration=120,
         langs=["en", "hi"], description="Mock test based on the UPSC Civil Services Prelims GS Paper I pattern.",
         sections=[S("gs", "General Studies", 100, 2, 0.66, "gs_upsc")]),
    dict(slug="upsc-cse-prelims-csat", name="UPSC CSE Prelims - CSAT", category="civil_services", duration=120,
         langs=["en", "hi"], description="Mock test based on the UPSC CSAT (GS Paper II) pattern.",
         sections=[S("csat", "CSAT", 80, 2.5, 0.83, "csat")]),
    dict(slug="cat", name="CAT", category="higher_education", duration=120, langs=["en"], calc=True,
         description="Mock test based on the CAT pattern, including TITA (type-in-the-answer) questions.",
         scheme={"numeric_negative": False, "numeric_tolerance": 0.01},
         sections=[S("varc", "Verbal Ability and Reading Comprehension", 24, 3, 1, "varc", {"single": 20, "numeric": 4}),
                   S("dilr", "Data Interpretation and Logical Reasoning", 22, 3, 1, "dilr", {"single": 14, "numeric": 8}),
                   S("qa", "Quantitative Ability", 22, 3, 1, "qa_cat", {"single": 14, "numeric": 8})]),
    dict(slug="gate-cse", name="GATE Computer Science (CSE)", category="higher_education", duration=180, langs=["en"],
         calc=True, description="Mock test based on the GATE CS pattern with MCQ, MSQ and NAT questions.",
         scheme={"numeric_negative": False, "multi_negative": False, "numeric_tolerance": 0.01},
         sections=[S("ga", "General Aptitude", 10, 1.5, 0.5, "ga_gate"),
                   S("core1", "Computer Science (1 mark)", 25, 1, 1 / 3, "gate_cse", {"single": 15, "multi": 4, "numeric": 6}),
                   S("core2", "Computer Science (2 marks)", 30, 2, 2 / 3, "gate_cse", {"single": 18, "multi": 5, "numeric": 7})]),
    dict(slug="gate-ece", name="GATE Electronics and Communication (ECE)", category="higher_education", duration=180,
         langs=["en"], calc=True, description="Mock test based on the GATE EC pattern with MCQ, MSQ and NAT questions.",
         scheme={"numeric_negative": False, "multi_negative": False, "numeric_tolerance": 0.01},
         sections=[S("ga", "General Aptitude", 10, 1.5, 0.5, "ga_gate"),
                   S("core1", "Electronics (1 mark)", 25, 1, 1 / 3, "gate_ece", {"single": 15, "multi": 4, "numeric": 6}),
                   S("core2", "Electronics (2 marks)", 30, 2, 2 / 3, "gate_ece", {"single": 18, "multi": 5, "numeric": 7})]),
    dict(slug="cuet-pg", name="CUET-PG (General)", category="higher_education", duration=90, langs=["en", "hi"],
         description="Mock test based on the CUET-PG pattern: 75 questions, +4/-1.",
         sections=[S("paper", "General and Domain", 75, 4, 1, "cuet_pg")]),
    dict(slug="it-placement-aptitude", name="Campus Placement Aptitude (IT services)", category="campus_hiring", duration=60,
         langs=TIER1, description="Placement-style aptitude test used by IT services companies (no negative marking).",
         sections=[S("quant", "Quantitative aptitude", 20, 1, 0, "quant"),
                   S("logical", "Logical reasoning", 20, 1, 0, "reasoning"),
                   S("verbal", "Verbal ability", 20, 1, 0, "verbal")]),
    dict(slug="general-aptitude-reasoning-verbal", name="General Aptitude + Reasoning + Verbal", category="campus_hiring",
         duration=45, langs=ALL, description="Role-agnostic aptitude test for white-collar job seekers.",
         sections=[S("quant", "Aptitude", 15, 1, 0.25, "quant"),
                   S("reasoning", "Reasoning", 15, 1, 0.25, "reasoning"),
                   S("verbal", "Verbal", 15, 1, 0.25, "verbal")]),
]

RUBRIC = {"criteria": [
    {"key": "role_knowledge", "label": "Role knowledge", "description": "Accuracy and depth of role/technical answers"},
    {"key": "answer_structure", "label": "Answer structure", "description": "Clear structure, STAR for situational answers"},
    {"key": "communication", "label": "Communication", "description": "Clarity, conciseness, language fluency"},
    {"key": "confidence", "label": "Confidence", "description": "Composure, ownership, decisiveness"},
    {"key": "resume_consistency", "label": "Resume consistency", "description": "Answers match the resume and claims"},
]}

ROLES = [
    ("software-developer-fresher", "Software developer (fresher)", ["fresher", "1-3"],
     {"role_technical": ["Data structures and their trade-offs", "OOP concepts", "SQL basics", "A project you built",
                         "Debugging approach"], "hr": ["Relocation and shifts", "Learning new technologies"]}),
    ("bank-po-interview", "Bank PO interview", ["fresher", "1-3", "3-5"],
     {"role_technical": ["Banking basics: CRR, SLR, repo rate", "NPAs", "Financial inclusion schemes",
                         "Digital payments and UPI"], "hr": ["Why banking", "Rural posting"]}),
    ("hr-executive", "HR executive", ["fresher", "1-3", "3-5"],
     {"role_technical": ["Recruitment funnel", "Onboarding", "Labour law basics", "Employee engagement",
                         "Handling grievances"]}),
    ("sales-business-development", "Sales / business development", ["fresher", "1-3", "3-5"],
     {"role_technical": ["Prospecting and lead qualification", "Handling objections", "Meeting targets",
                         "CRM usage"], "situational": ["Losing a big deal", "Difficult customer"]}),
    ("accountant-financial-analyst", "Accountant / financial analyst", ["fresher", "1-3", "3-5"],
     {"role_technical": ["GST basics", "Reconciliation", "Financial statements", "Ratio analysis", "Excel skills"]}),
    ("civil-services-personality-test", "Civil services personality test", ["fresher", "1-3", "3-5"],
     {"role_technical": ["Current governance issues", "Ethics dilemmas", "Your home state and district",
                         "Optional subject"], "hr": ["Why civil services", "Service preference"]}),
]

GLOSSARY = [
    ("compound interest", "hi", "चक्रवृद्धि ब्याज"), ("simple interest", "hi", "साधारण ब्याज"),
    ("profit and loss", "hi", "लाभ और हानि"), ("percentage", "hi", "प्रतिशत"),
    ("compound interest", "ta", "கூட்டு வட்டி"), ("simple interest", "ta", "தனி வட்டி"),
    ("percentage", "ta", "சதவீதம்"), ("ratio", "ta", "விகிதம்"),
]


# 15-day launch scope (PrepMitra_15_Day_Plan_Frontend_Backend.xlsx): 3 exams + the free mini mock, 2 interview
# roles, English + Hindi, one-time credit packs (auto-renew plans are Phase 2). Everything else is seeded as draft
# so an admin can publish it later without code.
LAUNCH_EXAMS = {"mini-mock-general-aptitude", "ssc-cgl-tier1", "ibps-po-prelims", "it-placement-aptitude"}
LAUNCH_ROLES = {"software-developer-fresher", "bank-po-interview"}
LAUNCH_PLANS = {"free_trial", "pay_per_exam", "credit_pack_10"}
LAUNCH_LANGS = ["en", "hi"]


def seed(papers_per_exam: int = 0, scope: str = "launch") -> dict:
    """scope="launch": the 15-day MVP catalog. scope="full": the PDF's whole proposed catalog (15 exams, 6 roles)."""
    full = scope == "full"
    with SessionLocal() as db:
        for code, name, price, credits_, days, rec in PLANS:
            p = db.scalar(select(Plan).where(Plan.code == code)) or Plan(code=code)
            p.name, p.price_paise, p.credits, p.validity_days, p.is_recurring = name, price, credits_, days, rec
            p.active = full or code in LAUNCH_PLANS
            db.add(p)

        for spec in EXAMS:
            live = full or spec["slug"] in LAUNCH_EXAMS
            e = db.scalar(select(Exam).where(Exam.slug == spec["slug"]))
            if e is None:
                e = Exam(slug=spec["slug"], status="published" if live else "draft")
                db.add(e)
            elif live:
                e.status = "published"
            e.name, e.category, e.description = spec["name"], spec["category"], spec["description"]
            e.is_free_trial, e.credits_required = spec.get("free", False), 1
            db.flush()
            for sec in spec["sections"]:
                for tname, w in T[sec["_topics"]]:
                    exists = db.scalar(select(Topic).where(Topic.exam_id == e.id, Topic.section_key == sec["key"],
                                                           Topic.name == tname))
                    if exists is None:
                        db.add(Topic(exam_id=e.id, section_key=sec["key"], name=tname, weightage=w))
            if e.current_blueprint_version is None:
                sections = [{k: v for k, v in s.items() if k != "_topics"} for s in spec["sections"]]
                db.add(ExamBlueprint(
                    exam_id=e.id, version=1, sections=sections, duration_min=spec["duration"],
                    marking_scheme=spec.get("scheme", {}), difficulty_mix=MIX,
                    languages=spec["langs"] if full else [l for l in spec["langs"] if l in LAUNCH_LANGS],
                    calculator_allowed=spec.get("calc", False),
                    instructions=("Read each question carefully. You can switch between your language and English. "
                                  "Unanswered questions get 0 marks; wrong answers may carry negative marks. "
                                  "The test submits automatically when time runs out."),
                ))
                e.current_blueprint_version = 1
        for slug, name, levels, themes in ROLES:
            r = db.scalar(select(InterviewRole).where(InterviewRole.slug == slug)) or InterviewRole(slug=slug)
            live = full or slug in LAUNCH_ROLES
            if r.status is None or live:
                r.status = "published" if live else "draft"
            r.name, r.levels, r.rubric, r.duration_min = name, levels, RUBRIC, 20
            r.description = f"Realistic {name} mock interview: introduction, resume, role, situational and HR rounds."
            r.prompt_config = {"persona": "a fair, experienced interview panelist", "question_count": 10,
                               "themes": {"introduction": ["Introduce yourself"],
                                          "situational": themes.get("situational", ["A conflict in a team",
                                                                                    "A tight deadline"]),
                                          "hr": themes.get("hr", ["Strengths and weaknesses", "Career goals"]),
                                          "role_technical": themes["role_technical"],
                                          "resume": ["Most significant project", "A gap or change on the resume"],
                                          "closing": ["Any questions for the panel"]}}
            db.add(r)
        for term, lang, tr in GLOSSARY:
            if db.scalar(select(Glossary).where(Glossary.term == term, Glossary.language == lang)) is None:
                db.add(Glossary(term=term, language=lang, approved_translation=tr))
        starter = "Make sure exactly one option is correct and distractors differ from the answer by more than rounding."
        if db.scalar(select(AiLesson).where(AiLesson.source_ref == "seed")) is None:
            db.add(AiLesson(lesson_text=starter, language="en", source_ref="seed", embedding=embed(starter)))
        db.commit()

        made = 0
        if papers_per_exam:
            from app.services.papers import pregenerate

            made = pregenerate(db, papers_per_exam)
        return {"plans": len(PLANS), "exams": len(EXAMS), "roles": len(ROLES), "papers": made}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers", type=int, default=0, help="pre-generate this many papers per exam")
    ap.add_argument("--scope", choices=["launch", "full"], default="launch",
                    help="launch = 15-day MVP catalog (default); full = all 15 exams and 6 roles")
    args = ap.parse_args()
    print(seed(args.papers, args.scope))
