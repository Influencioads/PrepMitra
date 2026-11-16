"""Cheat codes (redesign): exam-safe shortcuts with a worked example, the trap, and a 3-question drill.

The catalogue and drill answers are fixed content; drills are marked by code. A code unlocks for a student when they
get 2 of 3 drill questions right (stored as an `ai_artifacts` row, kind "cheat_unlock").
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError, not_found
from app.models import AiArtifact, User


def _q(text: str, options: list[str], answer: str, why: str) -> dict:
    return {"text": text, "options": [{"key": k, "text": t} for k, t in zip("ABCD", options)], "answer": answer,
            "explanation": why}


CODES: list[dict] = [
    {"id": "ci-1331", "topic": "Compound interest", "title": "×1.331 for 10% CI, 3 yrs", "saves_seconds": 40,
     "trick": "1.1³ = 1.331. Multiply the principal once — no year-by-year.",
     "example": "₹8,000 at 10% CI for 3 years: 8,000 × 1.331 = ₹10,648.",
     "trap": "Only for 10% compounded annually. Half-yearly at 10% is 5% for 6 periods — 1.05⁶, not 1.331.",
     "exams": ["SSC CGL", "IBPS PO", "SBI PO"],
     "drill": [_q("Amount on ₹5,000 at 10% p.a. compound interest for 3 years?", ["₹6,500", "₹6,655", "₹6,600", "₹6,750"], "B", "5,000 × 1.331 = 6,655."),
               _q("Compound interest on ₹10,000 at 10% p.a. for 3 years?", ["₹3,000", "₹3,100", "₹3,310", "₹3,331"], "C", "10,000 × 1.331 = 13,310, so CI = 3,310."),
               _q("₹2,000 at 10% p.a. compounded annually amounts to what after 3 years?", ["₹2,662", "₹2,600", "₹2,620", "₹2,731"], "A", "2,000 × 1.331 = 2,662.")]},
    {"id": "ci-si-2yr", "topic": "Compound interest", "title": "CI − SI for 2 years = P(r/100)²", "saves_seconds": 35,
     "trick": "The difference is just interest on the first year's interest.",
     "example": "P = ₹5,000, r = 10%: 5,000 × (0.1)² = ₹50.",
     "trap": "Only for exactly 2 years. For 3 years use P(r/100)² × (3 + r/100).",
     "exams": ["SSC CGL", "IBPS PO"],
     "drill": [_q("CI − SI on ₹8,000 at 5% for 2 years?", ["₹20", "₹40", "₹10", "₹80"], "A", "8,000 × 0.05² = 20."),
               _q("CI − SI on ₹12,000 at 10% for 2 years?", ["₹100", "₹120", "₹144", "₹240"], "B", "12,000 × 0.1² = 120."),
               _q("CI − SI for 2 years at 20% is ₹160. The principal is:", ["₹3,200", "₹4,000", "₹800", "₹1,600"], "B", "P × 0.04 = 160, so P = 4,000.")]},
    {"id": "x-percent-of-y", "topic": "Percentages", "title": "x% of y = y% of x", "saves_seconds": 20,
     "trick": "Swap the two numbers when one side is friendlier.",
     "example": "16% of 25 = 25% of 16 = 4.",
     "trap": "If neither side is friendly (say 37% of 83), swapping saves nothing — approximate instead.",
     "exams": ["SSC CHSL", "IBPS Clerk"],
     "drill": [_q("8% of 50 = ?", ["4", "40", "0.4", "5"], "A", "50% of 8 = 4."),
               _q("24% of 25 = ?", ["5", "6", "8", "12"], "B", "25% of 24 = 6."),
               _q("36% of 75 = ?", ["24", "25", "27", "30"], "C", "75% of 36 = 27.")]},
    {"id": "two-changes", "topic": "Percentages", "title": "Two changes: a + b + ab/100", "saves_seconds": 30,
     "trick": "Net % change of two successive changes, in one line.",
     "example": "+20% then −10%: 20 − 10 + (20 × −10)/100 = +8%.",
     "trap": "Keep the signs inside ab/100. For three changes apply it twice — never just add all three.",
     "exams": ["SSC CGL", "IBPS PO", "SBI Clerk"],
     "drill": [_q("Price up 10%, then up 10%. Net change?", ["+20%", "+21%", "+19%", "+22%"], "B", "10 + 10 + 100/100 = 21."),
               _q("Price up 25%, then down 20%. Net change?", ["+5%", "0%", "−5%", "+2%"], "B", "25 − 20 − 500/100 = 0."),
               _q("Salary down 10%, then up 20%. Net change?", ["+10%", "+8%", "+12%", "−8%"], "B", "−10 + 20 − 200/100 = 8.")]},
    {"id": "together-ab", "topic": "Time & work", "title": "Together = ab / (a + b)", "saves_seconds": 30,
     "trick": "Two workers, days a and b: product over sum.",
     "example": "A takes 12 days, B takes 18: 216 ÷ 30 = 7.2 days together.",
     "trap": "Only two workers at constant speed. Three workers, or someone leaving midway — switch to LCM units.",
     "exams": ["SSC CGL", "SSC CHSL"],
     "drill": [_q("A: 10 days, B: 15 days. Together?", ["5 days", "6 days", "12.5 days", "7 days"], "B", "150 ÷ 25 = 6."),
               _q("A: 20 days, B: 30 days. Together?", ["12 days", "25 days", "10 days", "15 days"], "A", "600 ÷ 50 = 12."),
               _q("A: 6 days, B: 12 days. Together?", ["9 days", "3 days", "4 days", "5 days"], "C", "72 ÷ 18 = 4.")]},
    {"id": "lcm-work", "topic": "Time & work", "title": "Total work = LCM of the days", "saves_seconds": 45,
     "trick": "Make work a whole number of units. Rates become integers.",
     "example": "A 10 days, B 15: work = 30 units; A = 3/day, B = 2/day; together 30 ÷ 5 = 6 days.",
     "trap": "If speeds come as a ratio (\"A is twice as fast as B\"), take units from the ratio, not the LCM.",
     "exams": ["SSC CGL", "IBPS PO", "SBI PO"],
     "drill": [_q("A: 12 days, B: 18 days, C: 36 days. All together?", ["6 days", "8 days", "9 days", "4 days"], "A", "Work 36: rates 3 + 2 + 1 = 6, so 6 days."),
               _q("A: 8 days, B: 12 days. A works 2 days alone, then B finishes. B takes?", ["8 days", "9 days", "6 days", "10 days"], "B", "Work 24: A does 3 × 2 = 6, left 18, B at 2/day = 9 days."),
               _q("A and B together: 10 days. A alone: 15 days. B alone?", ["25 days", "30 days", "20 days", "35 days"], "B", "Work 30: A+B = 3, A = 2, B = 1/day, so 30 days.")]},
    {"id": "unit-digit", "topic": "DI", "title": "Unit-digit check", "saves_seconds": 25,
     "trick": "Multiply only the last digits. Kill options with the wrong ending.",
     "example": "347 × 28: 7 × 8 = 56 → ends in 6. Of 9,712 / 9,716 / 9,718, only 9,716 survives.",
     "trap": "If two options end in the same digit, follow up with a digit-sum (casting out nines) check.",
     "exams": ["SSC CGL", "IBPS PO", "IBPS Clerk"],
     "drill": [_q("413 × 27 = ?", ["11,149", "11,151", "11,153", "11,157"], "B", "3 × 7 = 21 → ends in 1. Only 11,151."),
               _q("268 × 34 = ?", ["9,110", "9,114", "9,112", "9,118"], "C", "8 × 4 = 32 → ends in 2. Only 9,112."),
               _q("159 × 47 = ?", ["7,473", "7,475", "7,477", "7,471"], "A", "9 × 7 = 63 → ends in 3. Only 7,473.")]},
    {"id": "round-two-figures", "topic": "DI", "title": "Round to 2 figures when options are far apart", "saves_seconds": 50,
     "trick": "Options 10%+ apart? Round both numbers and divide in your head.",
     "example": "4,872 ÷ 19.6 ≈ 4,900 ÷ 20 = 245 (exact: 248.6).",
     "trap": "If options sit within 5% of each other, compute exactly — rounding can pick the wrong one.",
     "exams": ["IBPS PO", "SBI PO", "SSC CGL"],
     "drill": [_q("Approximately 6,018 ÷ 29.8 = ?", ["150", "200", "250", "300"], "B", "6,000 ÷ 30 = 200."),
               _q("Approximately 39.7% of 1,206 = ?", ["360", "420", "480", "540"], "C", "40% of 1,200 = 480."),
               _q("Approximately 2,987 × 0.51 = ?", ["1,200", "1,500", "1,800", "2,100"], "B", "3,000 × 0.5 = 1,500.")]},
    {"id": "pin-one-both-cases", "topic": "Seating puzzles", "title": "Pin one, then draw both cases", "saves_seconds": 60,
     "trick": "Start from the clue that fixes a seat. Draw Case 1 and Case 2 side by side.",
     "example": "\"A sits at the extreme left; B is second to the right of A\" → A = 1, B = 3. Every later clue now has an anchor.",
     "trap": "If two clues still leave 4+ cases open, skip the puzzle and come back. It is a time sink.",
     "exams": ["IBPS PO", "SBI PO", "IBPS Clerk"],
     "drill": [_q("Five in a row facing north. P is at the extreme left, Q is second to the right of P. Q's seat number from the left?", ["2", "3", "4", "5"], "B", "P = 1, so Q = 3."),
               _q("Six around a circle facing the centre. A is 2nd to the right of D. Counting from D, which way do you go?", ["Clockwise", "Anticlockwise", "Either", "Cannot say"], "B", "Facing the centre, right is anticlockwise."),
               _q("Which clue should you place first?", ["C is not next to D", "B sits between A and D", "A sits at an extreme end", "E is opposite B"], "C", "A clue that fixes a seat is the anchor.")]},
    {"id": "some-all-some", "topic": "Syllogism", "title": "Some + All = Some", "saves_seconds": 20,
     "trick": "Some A are B + All B are C → Some A are C. The middle term carries it.",
     "example": "Some pens are books. All books are bags. ⇒ Some pens are bags.",
     "trap": "\"All A are B\" + \"Some B are C\" gives NO definite link between A and C — only a possibility.",
     "exams": ["IBPS PO", "SBI Clerk"],
     "drill": [_q("Some cats are dogs. All dogs are birds. Conclusion: Some cats are birds.", ["Follows", "Does not follow", "Only a possibility", "Cannot say"], "A", "Some + All = Some."),
               _q("All roses are flowers. Some flowers are red. Conclusion: Some roses are red.", ["Follows", "Does not follow", "Definitely false", "Always true"], "B", "All + Some gives no definite conclusion."),
               _q("Some pens are books. All books are bags. Conclusion: All pens are bags.", ["Follows", "Does not follow", "Always true", "Partly follows"], "B", "Only Some pens are bags follows.")]},
    {"id": "cross-out-of", "topic": "English", "title": "Cross out \"of the …\" to find the subject", "saves_seconds": 15,
     "trick": "Strike the phrase after \"of\". The verb agrees with what is left.",
     "example": "\"One of the boys were absent\" → One … was absent.",
     "trap": "\"A number of\" takes a plural verb; \"The number of\" takes a singular one. The strike-out rule does not apply.",
     "exams": ["SSC CGL", "IBPS PO", "SBI Clerk"],
     "drill": [_q("Each of the students ___ a book.", ["have", "has", "are having", "were having"], "B", "Each … has."),
               _q("The quality of the mangoes ___ poor.", ["was", "were", "are", "have been"], "A", "Quality … was."),
               _q("A number of students ___ absent today.", ["is", "was", "are", "has been"], "C", "\"A number of\" takes a plural verb.")]},
    {"id": "stem-first-scan", "topic": "Reading", "title": "Stem-first scan", "saves_seconds": 20,
     "trick": "On any question over two lines, read the last sentence (the ask) first, then the data.",
     "example": "\"…How long will it take to cross a 360 m platform?\" Read that first: you need time, so look for speed and total distance.",
     "trap": "On one-line questions the ask is already in front of you — just read normally.",
     "exams": ["IBPS PO", "SBI PO", "SSC CGL"],
     "drill": [_q("A word problem is four lines long. What do you read first?", ["The first number", "The last sentence", "The options", "The units"], "B", "The last sentence tells you what to find."),
               _q("\"…What is the ratio of their present ages?\" Which quantity must your answer be?", ["A ratio", "An age in years", "A difference", "A sum"], "A", "The ask is a ratio."),
               _q("When is stem-first scanning not needed?", ["DI sets", "Long word problems", "One-line questions", "Caselets"], "C", "Short questions show the ask at once.")]},
    {"id": "elimination", "topic": "Exam strategy", "title": "Eliminate two, then guess", "saves_seconds": 15,
     "trick": "Cross out two options before any guess. A blind guess with 5 options is worth 0 marks on average.",
     "example": "With 3 options left: +1 × 1/3 − 0.25 × 2/3 = +1/6 mark per guess on average.",
     "trap": "If you cannot remove even one option, skip — guessing costs time and gains nothing.",
     "exams": ["IBPS PO", "SBI PO", "SSC CGL"],
     "drill": [_q("5 options, −0.25 per wrong. Expected marks of a blind guess?", ["+0.2", "0", "−0.05", "+0.25"], "B", "1/5 − 0.25 × 4/5 = 0."),
               _q("3 options left, −0.25 per wrong. Expected marks of a guess?", ["0", "+1/6", "+1/3", "−1/6"], "B", "1/3 − 0.25 × 2/3 = 1/6."),
               _q("You cannot rule out any option. Best move?", ["Guess A", "Skip", "Guess the longest", "Guess C"], "B", "A blind guess is worth 0 and costs time.")]},
]
BY_ID = {c["id"]: c for c in CODES}
TOPIC_ALIASES = {"Compound interest": ["compound", "interest"], "Percentages": ["percent"],
                 "Time & work": ["work", "pipe"], "DI": ["data interpretation", "di ", "simplification", "approximation"],
                 "Seating puzzles": ["seating", "arrangement", "puzzle"], "Syllogism": ["syllogism"],
                 "English": ["grammar", "error", "sentence", "english"], "Reading": ["reading", "comprehension"]}


def _public(c: dict, unlocked: bool) -> dict:
    return {k: v for k, v in c.items() if k != "drill"} | {"unlocked": unlocked, "drill_size": len(c["drill"])}


def _unlocked(db: Session, user: User) -> dict[str, AiArtifact]:
    rows = db.scalars(select(AiArtifact).where(AiArtifact.user_id == user.id, AiArtifact.kind == "cheat_unlock")).all()
    return {r.cache_key: r for r in rows}


def _suggested(weak_topics: list[str]) -> list[str]:
    """Codes that match the student's weak topics, in weakness order."""
    out = []
    for w in weak_topics:
        wl = w.lower()
        for c in CODES:
            if c["id"] not in out and any(a in wl for a in TOPIC_ALIASES.get(c["topic"], [c["topic"].lower()])):
                out.append(c["id"])
    return out


def catalogue(db: Session, user: User, weak_topics: list[str] | None = None) -> dict:
    unlocked = _unlocked(db, user)
    yours = list(dict.fromkeys([*unlocked, *_suggested(weak_topics or [])]))[:6] or [c["id"] for c in CODES[:6]]
    topics: dict[str, int] = {}
    for c in CODES:
        topics[c["topic"]] = topics.get(c["topic"], 0) + 1
    return {"total": len(CODES), "unlocked_count": len(unlocked),
            "topics": [{"name": k, "count": v} for k, v in topics.items()],
            "yours": [_public(BY_ID[i], i in unlocked) for i in yours if i in BY_ID],
            "items": [_public(c, c["id"] in unlocked) for c in CODES]}


def drill(code_id: str) -> dict:
    c = BY_ID.get(code_id)
    if c is None:
        raise not_found("Cheat code")
    return {"code_id": code_id, "title": c["title"],
            "questions": [{"text": q["text"], "options": q["options"]} for q in c["drill"]]}


def check(db: Session, user: User, code_id: str, answers: list[str | None]) -> dict:
    c = BY_ID.get(code_id)
    if c is None:
        raise not_found("Cheat code")
    if len(answers) != len(c["drill"]):
        raise AppError(422, "bad_request", f"Send {len(c['drill'])} answers")
    results = [{"correct": (a or "").upper() == q["answer"], "answer": q["answer"], "explanation": q["explanation"]}
               for a, q in zip(answers, c["drill"])]
    right = sum(r["correct"] for r in results)
    unlocked = _unlocked(db, user)
    newly = right >= 2 and code_id not in unlocked
    if newly:
        db.add(AiArtifact(user_id=user.id, kind="cheat_unlock", cache_key=code_id, title=c["title"],
                          payload={"right": right}, model="code"))
        db.commit()
    return {"code_id": code_id, "right": right, "of": len(results), "results": results,
            "unlocked": right >= 2 or code_id in unlocked, "newly_unlocked": newly}
