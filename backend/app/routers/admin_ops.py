"""Admin: users and credits (support), payments/plans/revenue (finance), quality dashboard (founder/product),
audit log."""

import uuid
from datetime import date, datetime, time, timedelta, timezone
from statistics import mean
from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.ai.provider import USD_TO_INR, cost_usd
from app.core.audit import audit
from app.core.deps import require_admin
from app.core.errors import AppError, not_found
from app.db import get_db, utcnow
from app.models import (
    AdminUser,
    AiUsage,
    Attempt,
    AuditLog,
    CreditLedger,
    Exam,
    InterviewSession,
    Order,
    Plan,
    Question,
    QuestionGenerationLog,
    QuestionReport,
    RefreshToken,
    Report,
    Subscription,
    User,
)
from app.routers.billing import invoice_response
from app.services import credits, payments

router = APIRouter(prefix="/admin", tags=["admin: operations"])
support = require_admin("support")
finance = require_admin("finance")
quality = require_admin("product")
founder = require_admin("founder")
ADMIN_ROLES = ("founder", "content_manager", "subject_expert", "language_reviewer", "support", "finance", "product")


# ---- users --------------------------------------------------------------------------------------------------------
def _user_out(u: User) -> dict:
    return {"id": u.id, "phone": u.phone, "email": u.email, "name": u.name, "state": u.state,
            "preferred_language": u.preferred_language, "status": u.status, "created_at": u.created_at,
            "last_active_at": u.last_active_at, "admin_role": u.admin.role if u.admin else None}


@router.get("/users")
def search_users(q: str | None = None, status: str | None = None, limit: int = Query(default=50, ge=1, le=200),
                 offset: int = Query(default=0, ge=0), admin: User = Depends(support), db: Session = Depends(get_db)):
    stmt = select(User)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(or_(User.phone.ilike(like), User.name.ilike(like), User.email.ilike(like)))
    if status:
        stmt = stmt.where(User.status == status)
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = db.scalars(stmt.order_by(User.created_at.desc()).limit(limit).offset(offset)).all()
    return {"items": [_user_out(u) for u in rows], "total": total, "limit": limit, "offset": offset}


@router.get("/users/{user_id}")
def get_user(user_id: uuid.UUID, admin: User = Depends(support), db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if u is None:
        raise not_found("User")
    attempts = db.scalars(select(Attempt).where(Attempt.user_id == u.id).order_by(Attempt.started_at.desc()).limit(50)).all()
    interviews = db.scalars(select(InterviewSession).where(InterviewSession.user_id == u.id)
                            .order_by(InterviewSession.created_at.desc()).limit(50)).all()
    orders = db.scalars(select(Order).where(Order.user_id == u.id).order_by(Order.created_at.desc()).limit(50)).all()
    ledger = db.scalars(select(CreditLedger).where(CreditLedger.user_id == u.id).order_by(CreditLedger.id.desc()).limit(100)).all()
    p = u.profile
    return _user_out(u) | {
        "profile": {"education": p.education, "stream": p.stream, "target_exam_ids": p.target_exam_ids,
                    "target_role_ids": p.target_role_ids, "experience_years": p.experience_years} if p else None,
        "credits": credits.balance(db, u.id),
        "attempts": [{"id": a.id, "exam_id": a.exam_id, "status": a.status, "score": a.score, "max_score": a.max_score,
                      "started_at": a.started_at, "tab_switch_count": a.tab_switch_count} for a in attempts],
        "interviews": [{"id": s.id, "role_id": s.role_id, "status": s.status, "mode": s.mode,
                        "created_at": s.created_at} for s in interviews],
        "orders": [payments.order_out(o) for o in orders],
        "credit_ledger": [{"id": c.id, "delta": c.delta, "reason": c.reason, "expires_at": c.expires_at,
                           "ref_id": c.ref_id, "created_at": c.created_at} for c in ledger],
    }


class CreditGrantIn(BaseModel):
    credits: int = Field(ge=1, le=500)
    validity_days: int | None = Field(default=90, ge=1, le=3650)
    note: str = Field(min_length=3, max_length=300)


@router.post("/users/{user_id}/credits", status_code=201)
def add_credits(user_id: uuid.UUID, body: CreditGrantIn, admin: User = Depends(support), db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if u is None:
        raise not_found("User")
    g = credits.grant(db, u.id, body.credits, "admin_grant", body.validity_days, ref_id=f"admin:{admin.id}")
    audit(db, admin, "credits.grant", "user", u.id, credits=body.credits, note=body.note, ledger_id=g.id)
    db.commit()
    return credits.balance(db, u.id)


class RestoreIn(BaseModel):
    ref_id: str = Field(description="Attempt or interview id whose credit should be restored")
    note: str = Field(min_length=3, max_length=300)


@router.post("/users/{user_id}/credits/restore")
def restore_credits(user_id: uuid.UUID, body: RestoreIn, admin: User = Depends(support), db: Session = Depends(get_db)):
    restored = credits.restore(db, user_id, body.ref_id)
    if not restored:
        raise AppError(409, "nothing_to_restore", "No unrestored credit was used for this reference")
    audit(db, admin, "credits.restore", "user", user_id, ref_id=body.ref_id, restored=restored, note=body.note)
    db.commit()
    return {"restored": restored, "credits": credits.balance(db, user_id)}


class BlockIn(BaseModel):
    reason: str = Field(min_length=3, max_length=300)


@router.post("/users/{user_id}/block")
def block(user_id: uuid.UUID, body: BlockIn, admin: User = Depends(support), db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if u is None or u.status == "deleted":
        raise not_found("User")
    if u.admin is not None and u.admin.role == "founder":
        raise AppError(403, "forbidden", "Founder accounts cannot be blocked")
    u.status = "blocked"
    for t in db.scalars(select(RefreshToken).where(RefreshToken.user_id == u.id, RefreshToken.revoked_at.is_(None))):
        t.revoked_at = utcnow()
    audit(db, admin, "user.block", "user", u.id, reason=body.reason)
    db.commit()
    return _user_out(u)


@router.post("/users/{user_id}/unblock")
def unblock(user_id: uuid.UUID, admin: User = Depends(support), db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if u is None or u.status != "blocked":
        raise not_found("Blocked user")
    u.status = "active"
    audit(db, admin, "user.unblock", "user", u.id)
    db.commit()
    return _user_out(u)


class AdminRoleIn(BaseModel):
    role: Literal["founder", "content_manager", "subject_expert", "language_reviewer", "support", "finance", "product"] | None


@router.put("/users/{user_id}/admin-role")
def set_admin_role(user_id: uuid.UUID, body: AdminRoleIn, admin: User = Depends(founder), db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if u is None or u.status != "active":
        raise not_found("User")
    if body.role is None:
        if u.admin is not None:
            db.delete(u.admin)
    elif u.admin is None:
        db.add(AdminUser(user_id=u.id, role=body.role, permissions=[]))
    else:
        u.admin.role = body.role
    audit(db, admin, "admin_role.set", "user", u.id, role=body.role)
    db.commit()
    db.refresh(u)
    return _user_out(u)


# ---- payments -----------------------------------------------------------------------------------------------------
def _range(start: date | None, end: date | None) -> tuple[datetime, datetime]:
    end_dt = datetime.combine(end or utcnow().date(), time.max, tzinfo=timezone.utc)
    start_dt = datetime.combine(start or (end_dt.date() - timedelta(days=30)), time.min, tzinfo=timezone.utc)
    return start_dt, end_dt


@router.get("/payments")
@router.get("/orders")
def list_orders(status: str | None = None, user_id: uuid.UUID | None = None, start: date | None = None,
                end: date | None = None, limit: int = Query(default=50, ge=1, le=200), offset: int = Query(default=0, ge=0),
                admin: User = Depends(finance), db: Session = Depends(get_db)):
    s, e = _range(start, end)
    stmt = select(Order).where(Order.created_at >= s, Order.created_at <= e)
    if status:
        stmt = stmt.where(Order.status == status)
    if user_id:
        stmt = stmt.where(Order.user_id == user_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    plans = {p.id: p for p in db.scalars(select(Plan))}
    rows = db.scalars(stmt.order_by(Order.created_at.desc()).limit(limit).offset(offset)).all()
    return {"items": [payments.order_out(o, plans.get(o.plan_id)) | {"user_id": o.user_id, "refund_reason": o.refund_reason}
                      for o in rows], "total": total, "limit": limit, "offset": offset}


class RefundIn(BaseModel):
    reason: str = Field(min_length=3, max_length=500)


@router.post("/orders/{order_id}/refund")
def refund(order_id: uuid.UUID, body: RefundIn, admin: User = Depends(finance), db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if o is None:
        raise not_found("Order")
    payments.refund(db, o, body.reason)
    audit(db, admin, "order.refund", "order", o.id, reason=body.reason, amount_paise=o.amount_paise)
    db.commit()
    return payments.order_out(o, db.get(Plan, o.plan_id))


@router.get("/orders/{order_id}/invoice")
def admin_invoice(order_id: uuid.UUID, admin: User = Depends(finance), db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if o is None:
        raise not_found("Order")
    return invoice_response(db, o)


@router.get("/subscriptions")
def list_subscriptions(status: str | None = None, admin: User = Depends(finance), db: Session = Depends(get_db)):
    stmt = select(Subscription)
    if status:
        stmt = stmt.where(Subscription.status == status)
    return {"items": [{"id": s.id, "user_id": s.user_id, "plan_id": s.plan_id, "status": s.status,
                       "renews_at": s.renews_at, "mandate_ref": s.mandate_ref, "cancelled_at": s.cancelled_at}
                      for s in db.scalars(stmt.order_by(Subscription.created_at.desc()).limit(500))]}


@router.get("/revenue")
def revenue(start: date | None = None, end: date | None = None, admin: User = Depends(finance), db: Session = Depends(get_db)):
    """Revenue report: gross, GST, net, refunds, by plan and by day."""
    s, e = _range(start, end)
    paid = db.scalars(select(Order).where(Order.paid_at >= s, Order.paid_at <= e,
                                          Order.status.in_(("paid", "refunded")))).all()
    plans = {p.id: p for p in db.scalars(select(Plan))}
    by_plan, by_day = {}, {}
    for o in paid:
        code = plans[o.plan_id].code
        bp = by_plan.setdefault(code, {"orders": 0, "gross_paise": 0, "gst_paise": 0, "refunded_paise": 0})
        bp["orders"] += 1
        bp["gross_paise"] += o.amount_paise
        bp["gst_paise"] += o.gst_amount_paise
        if o.status == "refunded":
            bp["refunded_paise"] += o.amount_paise
        d = by_day.setdefault(o.paid_at.date().isoformat(), 0)
        by_day[o.paid_at.date().isoformat()] = d + o.amount_paise
    gross = sum(o.amount_paise for o in paid)
    gst = sum(o.gst_amount_paise for o in paid)
    refunded = sum(o.amount_paise for o in paid if o.status == "refunded")
    return {"from": s, "to": e, "orders": len(paid), "gross_paise": gross, "gst_paise": gst,
            "refunded_paise": refunded, "net_of_gst_and_refunds_paise": gross - gst - refunded,
            "by_plan": by_plan, "by_day": [{"date": k, "gross_paise": v} for k, v in sorted(by_day.items())]}


class PlanIn(BaseModel):
    code: str = Field(pattern=r"^[a-z0-9_]{2,30}$")
    name: str
    price_paise: int = Field(ge=0)
    credits: int = Field(ge=1)
    validity_days: int = Field(ge=1, le=3650)
    is_recurring: bool = False
    active: bool = True


@router.get("/plans")
def admin_plans(admin: User = Depends(finance), db: Session = Depends(get_db)):
    return {"items": [payments.plan_out(p) | {"active": p.active} for p in db.scalars(select(Plan).order_by(Plan.id))]}


@router.put("/plans")
def upsert_plan(body: PlanIn, admin: User = Depends(finance), db: Session = Depends(get_db)):
    """Create or update a plan by code (prices are proposals in the PDF; finance can change them here)."""
    p = db.scalar(select(Plan).where(Plan.code == body.code))
    if p is None:
        p = Plan(code=body.code)
        db.add(p)
    for k, v in body.model_dump().items():
        setattr(p, k, v)
    db.flush()
    audit(db, admin, "plan.upsert", "plan", p.id, **body.model_dump())
    db.commit()
    return payments.plan_out(p) | {"active": p.active}


# ---- quality dashboard --------------------------------------------------------------------------------------------
def _cost_inr(rows) -> float:
    return round(sum(cost_usd(model, tin, tout) for model, tin, tout in rows) * USD_TO_INR, 2)


@router.get("/quality")
def quality_dashboard(days: int = Query(default=30, ge=1, le=365), admin: User = Depends(quality),
                      db: Session = Depends(get_db)):
    """Report ratings, flag rate per exam and language, verification failure rate, AI cost per attempt, report
    generation time (PDF 12)."""
    since = utcnow() - timedelta(days=days)
    ratings = db.execute(select(Report.kind, func.avg(Report.user_rating), func.count(Report.user_rating))
                         .where(Report.created_at >= since, Report.user_rating.is_not(None)).group_by(Report.kind)).all()
    gen = [r for r in db.scalars(select(Report.generation_ms).where(Report.created_at >= since,
                                                                    Report.generation_ms.is_not(None)))]
    gen.sort()
    status_counts = dict(db.execute(select(Report.status, func.count()).where(Report.created_at >= since)
                                    .group_by(Report.status)).all())

    served = dict(db.execute(select(Question.exam_id, func.sum(Question.times_served)).group_by(Question.exam_id)).all())
    flags = db.execute(select(Question.exam_id, QuestionReport.language, func.count())
                       .join(Question, Question.id == QuestionReport.question_id)
                       .where(QuestionReport.created_at >= since)
                       .group_by(Question.exam_id, QuestionReport.language)).all()
    exams = {e.id: e.name for e in db.scalars(select(Exam))}
    flag_rows = [{"exam_id": eid, "exam": exams.get(eid), "language": lang, "reports": n,
                  "questions_served": int(served.get(eid) or 0),
                  "flag_rate": round(n / served[eid], 4) if served.get(eid) else None} for eid, lang, n in flags]

    outcomes = dict(db.execute(select(QuestionGenerationLog.outcome, func.count())
                               .where(QuestionGenerationLog.created_at >= since)
                               .group_by(QuestionGenerationLog.outcome)).all())
    total_gen = sum(outcomes.values())
    usage = db.execute(select(AiUsage.model, func.sum(AiUsage.input_tokens), func.sum(AiUsage.output_tokens))
                       .where(AiUsage.created_at >= since).group_by(AiUsage.model)).all()
    attempts = db.scalar(select(func.count()).select_from(Attempt).where(Attempt.started_at >= since)) or 0
    interviews = db.scalar(select(func.count()).select_from(InterviewSession)
                           .where(InterviewSession.created_at >= since)) or 0
    cost = _cost_inr(usage)
    return {
        "window_days": days,
        "report_ratings": [{"kind": k, "average": round(float(a), 2), "count": c} for k, a, c in ratings],
        "report_status": status_counts,
        "report_generation_ms": {"p50": gen[len(gen) // 2] if gen else None,
                                 "p95": gen[int(len(gen) * 0.95) - 1] if gen else None,
                                 "mean": round(mean(gen)) if gen else None},
        "flag_rate": flag_rows,
        "question_generation": {"outcomes": outcomes, "total": total_gen,
                                "verification_failure_rate": round(
                                    (outcomes.get("rejected_verification", 0) + outcomes.get("rejected_numeric_check", 0))
                                    / total_gen, 4) if total_gen else None},
        "ai_cost": {"estimated_inr": cost, "attempts_and_interviews": attempts + interviews,
                    "per_attempt_inr": round(cost / (attempts + interviews), 2) if attempts + interviews else None,
                    "target_per_attempt_inr": 20, "by_model": [{"model": m, "input_tokens": int(i or 0),
                                                                "output_tokens": int(o or 0)} for m, i, o in usage]},
    }


@router.get("/audit-log")
def audit_log(actor_user_id: uuid.UUID | None = None, target_type: str | None = None,
              limit: int = Query(default=100, ge=1, le=500), offset: int = Query(default=0, ge=0),
              admin: User = Depends(founder), db: Session = Depends(get_db)):
    stmt = select(AuditLog)
    if actor_user_id:
        stmt = stmt.where(AuditLog.actor_user_id == actor_user_id)
    if target_type:
        stmt = stmt.where(AuditLog.target_type == target_type)
    rows = db.scalars(stmt.order_by(AuditLog.id.desc()).limit(limit).offset(offset)).all()
    return {"items": [{"id": a.id, "actor_user_id": a.actor_user_id, "action": a.action, "target_type": a.target_type,
                       "target_id": a.target_id, "details": a.details, "at": a.at} for a in rows],
            "limit": limit, "offset": offset}


@router.get("/stats")
def stats(days: int = Query(default=30, ge=1, le=365), admin: User = Depends(require_admin("finance", "product", "support")),
          db: Session = Depends(get_db)):
    """Headline numbers for the admin home (API Plan #36): users, attempts, revenue, report rating, AI cost, report time."""
    since = utcnow() - timedelta(days=days)
    q = quality_dashboard(days=days, admin=admin, db=db)
    paid = db.execute(select(func.count(), func.coalesce(func.sum(Order.amount_paise), 0),
                             func.coalesce(func.sum(Order.gst_amount_paise), 0))
                      .where(Order.status == "paid", Order.paid_at >= since)).one()
    ratings = db.execute(select(func.avg(Report.user_rating), func.count(Report.user_rating))
                         .where(Report.created_at >= since, Report.user_rating.is_not(None))).one()
    return {
        "window_days": days,
        "users": {"total": db.scalar(select(func.count()).select_from(User).where(User.status != "deleted")),
                  "new": db.scalar(select(func.count()).select_from(User).where(User.created_at >= since)),
                  "active": db.scalar(select(func.count()).select_from(User).where(User.last_active_at >= since))},
        "attempts": {"started": db.scalar(select(func.count()).select_from(Attempt).where(Attempt.started_at >= since)),
                     "completed": db.scalar(select(func.count()).select_from(Attempt).where(
                         Attempt.started_at >= since, Attempt.status == "scored")),
                     "free_trial": db.scalar(select(func.count()).select_from(Attempt).where(
                         Attempt.started_at >= since, Attempt.is_free_trial.is_(True)))},
        "interviews": db.scalar(select(func.count()).select_from(InterviewSession)
                                .where(InterviewSession.created_at >= since)),
        "revenue": {"orders": paid[0], "gross_paise": int(paid[1]), "gst_paise": int(paid[2]),
                    "net_paise": int(paid[1]) - int(paid[2])},
        "report_rating": {"average": round(float(ratings[0]), 2) if ratings[0] is not None else None, "count": ratings[1]},
        "ai_cost_per_attempt_inr": q["ai_cost"]["per_attempt_inr"],
        "ai_cost_total_inr": q["ai_cost"]["estimated_inr"],
        "report_time_ms": q["report_generation_ms"],
        "open_flags": db.scalar(select(func.count()).select_from(QuestionReport).where(QuestionReport.status == "open")),
        "question_verification_failure_rate": q["question_generation"]["verification_failure_rate"],
    }


# ---- AI cost and routing (blueprint: track Rs per student and per feature) -----------------------------------------
@router.get("/ai/costs")
def ai_costs(days: int = Query(default=30, ge=1, le=365), admin: User = Depends(quality),
             db: Session = Depends(get_db)):
    """AI spend per feature and per model in the window, cache-hit share, and the routing table in force."""
    from app.ai import catalog

    since = utcnow() - timedelta(days=days)
    rows = db.execute(select(AiUsage.feature, AiUsage.purpose, AiUsage.model, func.count(),
                             func.sum(AiUsage.input_tokens), func.sum(AiUsage.cached_tokens),
                             func.sum(AiUsage.output_tokens), func.sum(AiUsage.cost_usd))
                      .where(AiUsage.created_at >= since)
                      .group_by(AiUsage.feature, AiUsage.purpose, AiUsage.model)).all()
    by_feature: dict[str, dict] = {}
    total = 0.0
    for feature, purpose, model, calls, tin, tcached, tout, usd in rows:
        key = feature or catalog.PURPOSE_TO_FEATURE.get(purpose, purpose)
        if usd is None:
            usd = cost_usd(model, tin or 0, tout or 0, tcached or 0)
        inr = float(usd) * USD_TO_INR
        total += inr
        f = by_feature.setdefault(key, {"feature": key, "calls": 0, "cost_inr": 0.0, "input_tokens": 0,
                                        "cached_tokens": 0, "output_tokens": 0, "models": {}})
        f["calls"] += calls
        f["cost_inr"] += inr
        f["input_tokens"] += tin or 0
        f["cached_tokens"] += tcached or 0
        f["output_tokens"] += tout or 0
        f["models"][model] = f["models"].get(model, 0) + calls
    features = sorted(by_feature.values(), key=lambda f: -f["cost_inr"])
    for f in features:
        f["cost_inr"] = round(f["cost_inr"], 2)
        f["cost_per_call_inr"] = round(f["cost_inr"] / f["calls"], 4) if f["calls"] else None
        f["cache_hit_share"] = round(f["cached_tokens"] / f["input_tokens"], 3) if f["input_tokens"] else None
    return {"window_days": days, "total_inr": round(total, 2), "usd_to_inr": USD_TO_INR, "features": features,
            "routing": catalog.routing_table()}
