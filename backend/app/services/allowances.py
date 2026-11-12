"""Monthly AI allowances ("hard allowances with soft landings", blueprint rule 4).

A student's entitlements are the sum of every plan they hold right now: Free, plus each paid order still inside its
validity (a study plan, a tutor pack, add-ons). Subscription limits reset every calendar month (UTC); add-on limits
are a pool that lasts the add-on's validity; the free allowance is for life.

`use()` spends one unit of a feature: this month's plan allowance first, then add-ons (oldest-expiring first), then
the free allowance. When a student asks for premium escalation but the premium allowance is used up, the request
still runs, on the cheaper route (`premium=False`), instead of being blocked.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db import utcnow
from app.models import FeatureUse, Order, Plan, User
from app.services.plan_catalog import FREE, METERED


@dataclass
class Pool:
    source: str  # "plan" | "free" | add-on order id
    limit: int
    since: datetime | None  # count uses from here (None = all time)
    expires_at: datetime | None


def _aware(dt: datetime | None) -> datetime | None:
    return dt.replace(tzinfo=timezone.utc) if dt is not None and dt.tzinfo is None else dt


def month_start(now: datetime | None = None) -> datetime:
    now = now or utcnow()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def active_purchases(db: Session, user_id) -> list[tuple[Order, Plan]]:
    now = utcnow()
    rows = db.execute(select(Order, Plan).join(Plan, Plan.id == Order.plan_id).where(
        Order.user_id == user_id, Order.status == "paid", Order.paid_at.is_not(None))).all()
    return [(o, p) for o, p in rows if _aware(o.paid_at) + timedelta(days=p.validity_days) > now]


def _pools(db: Session, user_id) -> tuple[dict, dict[str, list[Pool]], list[str]]:
    flags = dict(FREE["flags"])
    pools: dict[str, list[Pool]] = {}
    plan_limits: dict[str, int] = {}
    codes = []
    for o, p in sorted(active_purchases(db, user_id), key=lambda op: _aware(op[0].paid_at)):
        ent = p.entitlements or {}
        codes.append(p.code)
        for k, v in (ent.get("flags") or {}).items():
            if v and (k != "persona" or flags.get(k) != "full"):
                flags[k] = v
        if ent.get("group") == "addon":
            exp = _aware(o.paid_at) + timedelta(days=p.validity_days)
            for k, n in (ent.get("limits") or {}).items():
                pools.setdefault(k, []).append(Pool(str(o.id), n, _aware(o.paid_at), exp))
        else:
            for k, n in (ent.get("limits") or {}).items():
                plan_limits[k] = plan_limits.get(k, 0) + n
    start = month_start()
    for k, n in plan_limits.items():
        pools.setdefault(k, []).insert(0, Pool("plan", n, start, None))
    for k, n in FREE["limits"].items():
        pools.setdefault(k, []).append(Pool("free", n, None, None))
    for k, ps in pools.items():  # plan first, then add-ons oldest-expiring first, then free
        ps.sort(key=lambda p: (p.source != "plan", p.source == "free", p.expires_at or datetime.max.replace(
            tzinfo=timezone.utc)))
    return flags, pools, codes


def _used(db: Session, user_id, feature: str, pool: Pool) -> int:
    q = select(func.count()).select_from(FeatureUse).where(
        FeatureUse.user_id == user_id, FeatureUse.feature == feature, FeatureUse.source == pool.source)
    if pool.since is not None:
        q = q.where(FeatureUse.created_at >= pool.since)
    return int(db.scalar(q) or 0)


def summary(db: Session, user: User) -> dict:
    flags, pools, codes = _pools(db, user.id)
    limits = {}
    for feature, label in METERED.items():
        ps = pools.get(feature, [])
        lim = sum(p.limit for p in ps)
        used = sum(min(p.limit, _used(db, user.id, feature, p)) for p in ps)
        limits[feature] = {"label": label, "limit": lim, "used": used, "remaining": max(lim - used, 0),
                           "sources": [{"source": p.source, "limit": p.limit,
                                        "used": min(p.limit, _used(db, user.id, feature, p)),
                                        "expires_at": p.expires_at} for p in ps]}
    return {"plans": codes, "flags": flags, "limits": limits, "resets_at": _next_month(month_start())}


def _next_month(start: datetime) -> datetime:
    return (start + timedelta(days=32)).replace(day=1)


def has_flag(db: Session, user: User, flag: str) -> bool:
    return bool(_pools(db, user.id)[0].get(flag))


def _take(db: Session, user: User, feature: str, pools: dict, ref_id) -> str | None:
    for p in pools.get(feature, []):
        if _used(db, user.id, feature, p) < p.limit:
            db.add(FeatureUse(user_id=user.id, feature=feature, source=p.source,
                              ref_id=str(ref_id) if ref_id else None))
            db.flush()
            return p.source
    return None


def use(db: Session, user: User, feature: str, *, ref_id=None, want_premium: bool = False,
        units: int = 1) -> dict:
    """Spends `units` of `feature`. Returns {"premium": bool, "source": str}; raises 402 when nothing is left.

    Locks the user row so two concurrent requests cannot spend the last unit twice (PostgreSQL)."""
    if feature not in METERED:
        raise ValueError(f"unknown metered feature {feature!r}")
    db.execute(select(User.id).where(User.id == user.id).with_for_update())
    _, pools, _ = _pools(db, user.id)
    remaining = sum(max(p.limit - _used(db, user.id, feature, p), 0) for p in pools.get(feature, []))
    if remaining < units:
        raise AppError(402, "allowance_exhausted",
                       f"You have used all your {METERED[feature].lower()} for now. Upgrade or add a pack to continue.")
    source = None
    for _ in range(units):
        source = _take(db, user, feature, pools, ref_id)
    premium = False
    if want_premium:
        twin = f"premium_{feature}"
        premium = twin in METERED and _take(db, user, twin, pools, ref_id) is not None
    return {"premium": premium, "source": source}


def refund_use(db: Session, user: User, feature: str, ref_id) -> int:
    """Gives back units spent on `ref_id` when the AI call failed (technical failures never cost the student)."""
    rows = db.scalars(select(FeatureUse).where(
        FeatureUse.user_id == user.id, FeatureUse.ref_id == str(ref_id),
        FeatureUse.feature.in_((feature, f"premium_{feature}")))).all()
    for r in rows:
        db.delete(r)
    db.flush()
    return len(rows)
