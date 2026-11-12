"""Credit ledger (PDF section 7).

A grant is a row with delta > 0 and an optional expiry. Every use is a row with delta < 0 linked to the grant it
consumed (grant_id). A grant's remaining balance = grant.delta + sum(linked rows). Credits are deducted when an
attempt starts, oldest-expiring first; technical failures restore them automatically.
"""

from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db import utcnow
from app.models import CreditLedger, User

USE_REASONS = ("attempt", "interview")


def grant(db: Session, user_id, credits: int, reason: str, validity_days: int | None, ref_id=None) -> CreditLedger:
    row = CreditLedger(
        user_id=user_id, delta=credits, reason=reason, ref_id=str(ref_id) if ref_id else None,
        expires_at=utcnow() + timedelta(days=validity_days) if validity_days else None,
    )
    db.add(row)
    db.flush()
    return row


def _open_grants(db: Session, user_id) -> list[tuple[CreditLedger, int]]:
    now = utcnow()
    grants = db.scalars(
        select(CreditLedger).where(
            CreditLedger.user_id == user_id, CreditLedger.delta > 0, CreditLedger.grant_id.is_(None),
            (CreditLedger.expires_at.is_(None)) | (CreditLedger.expires_at > now),
        )
    ).all()
    if not grants:
        return []
    used = dict(db.execute(
        select(CreditLedger.grant_id, func.coalesce(func.sum(CreditLedger.delta), 0))
        .where(CreditLedger.grant_id.in_([g.id for g in grants]))
        .group_by(CreditLedger.grant_id)
    ).all())
    out = [(g, g.delta + int(used.get(g.id, 0))) for g in grants]
    out = [(g, r) for g, r in out if r > 0]
    # Oldest-expiring first; never-expiring grants last; ties by creation order.
    out.sort(key=lambda gr: (gr[0].expires_at is None, gr[0].expires_at or now, gr[0].id))
    return out


def balance(db: Session, user_id) -> dict:
    grants = _open_grants(db, user_id)
    return {
        "total": sum(r for _, r in grants),
        "next_expiry": next((g.expires_at for g, _ in grants if g.expires_at), None),
        "grants": [
            {"id": g.id, "remaining": r, "granted": g.delta, "reason": g.reason, "expires_at": g.expires_at,
             "granted_at": g.created_at}
            for g, r in grants
        ],
    }


def consume(db: Session, user: User, amount: int, reason: str, ref_id) -> CreditLedger:
    """Deducts `amount` credits. Locks the user row so concurrent starts cannot double-spend (PostgreSQL)."""
    db.execute(select(User.id).where(User.id == user.id).with_for_update())
    grants = _open_grants(db, user.id)
    if sum(r for _, r in grants) < amount:
        raise AppError(402, "insufficient_credits", "You have no exam credits left. Buy a plan to continue.")
    first = None
    left = amount
    for g, r in grants:
        take = min(r, left)
        row = CreditLedger(user_id=user.id, delta=-take, reason=reason, grant_id=g.id, ref_id=str(ref_id))
        db.add(row)
        db.flush()
        first = first or row
        left -= take
        if left == 0:
            break
    return first


def restore(db: Session, user_id, ref_id, why: str = "refund_restore") -> int:
    """Gives back every credit used for `ref_id` (an attempt or interview id). Idempotent."""
    ref = str(ref_id)
    rows = db.scalars(select(CreditLedger).where(CreditLedger.user_id == user_id, CreditLedger.ref_id == ref)).all()
    used = -sum(r.delta for r in rows if r.reason in USE_REASONS)
    already = sum(r.delta for r in rows if r.reason == why)
    to_restore = used - already
    if to_restore <= 0:
        return 0
    # Restore onto the original grant while it is still valid; otherwise grant a fresh 30-day credit.
    now = utcnow()
    for r in rows:
        if r.reason in USE_REASONS and to_restore > 0:
            g = db.get(CreditLedger, r.grant_id) if r.grant_id else None
            n = min(-r.delta, to_restore)
            if g is not None and (g.expires_at is None or g.expires_at > now):
                db.add(CreditLedger(user_id=user_id, delta=n, reason=why, grant_id=g.id, ref_id=ref))
            else:
                db.add(CreditLedger(user_id=user_id, delta=n, reason=why, ref_id=ref,
                                    expires_at=now + timedelta(days=30)))
            to_restore -= n
    db.flush()
    return used - already


def revoke_grant_remaining(db: Session, grant_row: CreditLedger, reason: str = "refund_revoke") -> int:
    """Removes whatever is left of a grant (used when a purchase is refunded)."""
    left = grant_row.delta + int(db.scalar(
        select(func.coalesce(func.sum(CreditLedger.delta), 0)).where(CreditLedger.grant_id == grant_row.id)
    ) or 0)
    if left > 0:
        db.add(CreditLedger(user_id=grant_row.user_id, delta=-left, reason=reason, grant_id=grant_row.id,
                            ref_id=str(grant_row.id)))
        db.flush()
    return max(left, 0)


def expire_credits(db: Session) -> int:
    """Writes explicit 'expiry' rows for expired grants with a balance, so the ledger tells the full story."""
    now = utcnow()
    expired = db.scalars(select(CreditLedger).where(
        CreditLedger.delta > 0, CreditLedger.grant_id.is_(None), CreditLedger.expires_at <= now,
    )).all()
    n = 0
    for g in expired:
        left = g.delta + int(db.scalar(
            select(func.coalesce(func.sum(CreditLedger.delta), 0)).where(CreditLedger.grant_id == g.id)
        ) or 0)
        if left > 0:
            db.add(CreditLedger(user_id=g.user_id, delta=-left, reason="expiry", grant_id=g.id, ref_id=str(g.id)))
            n += 1
    db.commit()
    return n
