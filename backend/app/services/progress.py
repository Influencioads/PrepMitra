"""Dashboard and progress (PDF 5.7): history, score trend, topic heatmap, credits + plan expiry, recommendations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Attempt,
    Exam,
    InterviewRole,
    InterviewSession,
    Report,
    Subscription,
    Topic,
    User,
    UserTopicMastery,
)
from app.services import credits


def progress(db: Session, user: User) -> dict:
    attempts = db.scalars(select(Attempt).where(Attempt.user_id == user.id).order_by(Attempt.started_at.desc())
                          .limit(100)).all()
    exams = {e.id: e for e in db.scalars(select(Exam).where(Exam.id.in_({a.exam_id for a in attempts})))}
    interviews = db.scalars(select(InterviewSession).where(InterviewSession.user_id == user.id)
                            .order_by(InterviewSession.created_at.desc()).limit(50)).all()
    roles = {r.id: r for r in db.scalars(select(InterviewRole).where(InterviewRole.id.in_({s.role_id for s in interviews})))}
    reports = {r.attempt_id or r.interview_session_id: r for r in db.scalars(
        select(Report).where(Report.user_id == user.id))}

    history = [{
        "kind": "exam", "id": a.id, "title": exams[a.exam_id].name, "exam_id": a.exam_id, "status": a.status,
        "at": a.started_at, "score": a.score, "max_score": a.max_score, "percentile": a.percentile,
        "report_id": reports[a.id].id if a.id in reports else None,
        "report_status": reports[a.id].status if a.id in reports else None,
    } for a in attempts]
    for s in interviews:
        rep = reports.get(s.id)
        overall = (rep.report or {}).get("overall") if rep and rep.status == "ready" else None
        history.append({"kind": "interview", "id": s.id, "title": roles[s.role_id].name, "status": s.status,
                        "at": s.created_at, "score": overall, "max_score": 10 if overall is not None else None,
                        "percentile": None, "report_id": rep.id if rep else None,
                        "report_status": rep.status if rep else None})
    history.sort(key=lambda h: h["at"], reverse=True)

    trend: dict[str, list] = {}
    for a in sorted((a for a in attempts if a.status == "scored"), key=lambda a: a.submitted_at):
        trend.setdefault(str(a.exam_id), []).append({
            "attempt_id": a.id, "at": a.submitted_at, "score": a.score, "max_score": a.max_score,
            "score_pct": round(100 * a.score / a.max_score, 1) if a.max_score else None, "percentile": a.percentile})

    mastery = db.execute(
        select(UserTopicMastery, Topic).join(Topic, Topic.id == UserTopicMastery.topic_id)
        .where(UserTopicMastery.user_id == user.id)).all()
    heat: dict[str, dict] = {}
    all_exams = {e.id: e for e in db.scalars(select(Exam).where(Exam.id.in_({t.exam_id for _, t in mastery})))}
    for m, t in mastery:
        h = heat.setdefault(str(t.exam_id), {"exam_id": t.exam_id, "exam_name": all_exams[t.exam_id].name, "topics": []})
        h["topics"].append({"topic_id": t.id, "name": t.name, "section_key": t.section_key,
                            "mastery": m.mastery_score, "questions_answered": m.attempts_count,
                            "last_seen_at": m.last_seen_at})
    for h in heat.values():
        h["topics"].sort(key=lambda x: x["mastery"])

    subs = db.scalars(select(Subscription).where(Subscription.user_id == user.id,
                                                 Subscription.status.in_(("active", "cancelled")))).all()
    return {
        "history": history[:100],
        "score_trend": [{"exam_id": k, "exam_name": exams[next(a.exam_id for a in attempts if str(a.exam_id) == k)].name,
                         "points": v} for k, v in trend.items()],
        "topic_heatmap": list(heat.values()),
        "credits": credits.balance(db, user.id),
        "subscriptions": [{"id": s.id, "plan_id": s.plan_id, "status": s.status, "renews_at": s.renews_at,
                           "auto_renew": s.status == "active" and bool(s.mandate_ref)} for s in subs],
        "recommended": recommendations(db, user, attempts, reports),
    }


def recommendations(db: Session, user: User, attempts: list[Attempt], reports: dict) -> list[dict]:
    """Next test from the latest report first, then the user's target exams, then the free mini mock."""
    out, seen = [], set()

    def add(exam: Exam | None, reason: str):
        if exam is not None and exam.status == "published" and exam.id not in seen:
            seen.add(exam.id)
            out.append({"exam_id": exam.id, "slug": exam.slug, "name": exam.name, "reason": reason})

    if not attempts:  # first-time users start with the free mini mock (PDF 4)
        add(db.scalar(select(Exam).where(Exam.status == "published", Exam.is_free_trial.is_(True)).limit(1)),
            "Free 30-minute mini mock with a full AI report")
    for a in attempts:
        rep = reports.get(a.id)
        slug = ((rep.report or {}).get("next_test") or {}).get("exam_slug") if rep and rep.status == "ready" else None
        if slug:
            add(db.scalar(select(Exam).where(Exam.slug == slug)),
                ((rep.report or {}).get("next_test") or {}).get("reason") or "Recommended in your last report")
            break
    targets = [str(t) for t in (user.profile.target_exam_ids or [])] if user.profile else []
    for e in db.scalars(select(Exam).where(Exam.status == "published")):
        if str(e.id) in targets or e.slug in targets:
            add(e, "One of your target exams")
    return out[:5]
