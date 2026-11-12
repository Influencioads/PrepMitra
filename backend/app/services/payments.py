"""Plans, orders, payment verification, webhooks, subscriptions, refunds and GST invoices (PDF section 7)."""

import json
import logging
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.audit import track
from app.core.errors import AppError, not_found
from app.db import utcnow
from app.models import CreditLedger, Order, PaymentWebhookEvent, Plan, Subscription, User
from app.services import credits
from app.services.gateways import get_gateway, verify_checkout_signature, verify_webhook_signature
from app.services.notifications import dispatch_after_commit, notify

log = logging.getLogger(__name__)


def gst_split(price_paise: int) -> tuple[int, int]:
    """Prices are GST-inclusive (assumed until the owner decides, see docs). Returns (taxable, gst)."""
    rate = get_settings().gst_rate_percent
    gst = round(price_paise * rate / (100 + rate))
    return price_paise - gst, gst


def plan_out(p: Plan) -> dict:
    taxable, gst = gst_split(p.price_paise)
    return {"id": p.id, "code": p.code, "name": p.name, "price_paise": p.price_paise, "price_inr": p.price_paise / 100,
            "taxable_paise": taxable, "gst_paise": gst, "gst_inclusive": True, "credits": p.credits,
            "validity_days": p.validity_days, "is_recurring": p.is_recurring,
            "group": (p.entitlements or {}).get("group"), "period": (p.entitlements or {}).get("period"),
            "entitlements": p.entitlements or {},
            "purchasable": p.code != "free_trial" and p.price_paise > 0}


# A student can hold one study plan and one AI Tutor pack at a time; the Topper Combo is both.
_SLOTS = {"study": {"study"}, "tutor": {"tutor"}, "combo": {"study", "tutor"}}


def _slots(plan: Plan) -> set[str]:
    return _SLOTS.get((plan.entitlements or {}).get("group"), {"study"})


def list_plans(db: Session) -> list[dict]:
    return [plan_out(p) for p in db.scalars(select(Plan).where(Plan.active.is_(True)).order_by(Plan.price_paise))]


def create_order(db: Session, user: User, plan_code: str, platform: str) -> dict:
    plan = db.scalar(select(Plan).where(Plan.code == plan_code, Plan.active.is_(True)))
    if plan is None or plan.price_paise <= 0:
        raise not_found("Plan")
    if plan.is_recurring:
        held = db.scalars(select(Plan).join(Subscription, Subscription.plan_id == Plan.id).where(
            Subscription.user_id == user.id, Subscription.status == "active")).all()
        if any(_slots(h) & _slots(plan) for h in held):
            raise AppError(409, "already_subscribed", "You already have an active subscription of this kind")
    _, gst = gst_split(plan.price_paise)
    order = Order(user_id=user.id, plan_id=plan.id, amount_paise=plan.price_paise, gst_amount_paise=gst,
                  gateway="razorpay", status="created", client_platform=platform)
    db.add(order)
    db.flush()
    gw = get_gateway()
    order.gateway_order_id = gw.create_order(plan.price_paise, str(order.id),
                                             {"order_id": str(order.id), "plan": plan.code})
    db.commit()
    return checkout_payload(order, plan, user)


def checkout_payload(order: Order, plan: Plan, user: User) -> dict:
    gw = get_gateway()
    return {
        "order_id": order.id, "status": order.status, "gateway": order.gateway, "mock": gw.is_mock,
        "gateway_order_id": order.gateway_order_id, "key_id": gw.key_id, "amount_paise": order.amount_paise,
        "currency": "INR", "plan": plan_out(plan),
        # Razorpay Checkout (web) / Razorpay Android & iOS SDK options; the client opens checkout with these.
        "checkout_options": {"key": gw.key_id, "order_id": order.gateway_order_id, "amount": order.amount_paise,
                             "currency": "INR", "name": get_settings().app_name, "description": plan.name,
                             "prefill": {"name": user.name or "", "contact": user.phone or "", "email": user.email or ""},
                             "notes": {"order_id": str(order.id)}},
    }


def _own_order(db: Session, user: User, order_id) -> Order:
    o = db.get(Order, order_id)
    if o is None or o.user_id != user.id:
        raise not_found("Order")
    return o


def verify_checkout(db: Session, user: User, order_id, payment_id: str, signature: str) -> Order:
    """Client-side confirmation after checkout. The webhook does the same work, idempotently, as a backstop."""
    o = _own_order(db, user, order_id)
    if o.status == "paid":
        return o
    if not verify_checkout_signature(o.gateway_order_id, payment_id, signature):
        raise AppError(400, "invalid_signature", "Payment could not be verified")
    fulfil(db, o, payment_id)
    return o


def _next_invoice_no(db: Session) -> str:
    now = utcnow()
    fy_start = now.year if now.month >= 4 else now.year - 1
    prefix = f"PM/{fy_start}-{str(fy_start + 1)[-2:]}/"
    n = db.scalar(select(func.count()).select_from(Order).where(Order.invoice_no.like(f"{prefix}%"))) or 0
    return f"{prefix}{n + 1:06d}"


def fulfil(db: Session, order: Order, payment_id: str | None) -> bool:
    """Marks an order paid and grants credits exactly once. Returns False if it was already paid."""
    db.execute(select(Order.id).where(Order.id == order.id).with_for_update())
    db.refresh(order)
    if order.status == "paid":
        return False
    if order.status == "refunded":
        raise AppError(409, "order_refunded", "This order was refunded")
    plan = db.get(Plan, order.plan_id)
    order.status = "paid"
    order.paid_at = utcnow()
    order.gateway_payment_id = payment_id or order.gateway_payment_id
    order.invoice_no = _next_invoice_no(db)
    g = credits.grant(db, order.user_id, plan.credits, "purchase", plan.validity_days, ref_id=order.id)
    order.credit_grant_id = g.id
    if plan.is_recurring:
        sub = db.scalar(select(Subscription).where(Subscription.user_id == order.user_id,
                                                   Subscription.plan_id == plan.id,
                                                   Subscription.status.in_(("active", "cancelled"))))
        if sub is None:
            sub = Subscription(user_id=order.user_id, plan_id=plan.id, gateway=order.gateway)
            db.add(sub)
        sub.status = "active"
        sub.current_period_start = order.paid_at
        sub.renews_at = order.paid_at + timedelta(days=plan.validity_days)
        db.flush()
        order.subscription_id = sub.id
    track(db, order.user_id, "purchase", plan=plan.code, amount_paise=order.amount_paise,
          platform=order.client_platform)
    n = notify(db, order.user_id, "payment_receipt", {"order_id": str(order.id), "screen": "orders"},
               amount=f"{order.amount_paise / 100:.0f}", plan=plan.name, credits=plan.credits,
               expires=g.expires_at.strftime("%d %b %Y") if g.expires_at else "-", invoice=order.invoice_no)
    db.commit()
    dispatch_after_commit(n.id)
    return True


def handle_webhook(db: Session, gateway: str, raw_body: bytes, signature: str, event_id: str | None) -> dict:
    if gateway != "razorpay":
        raise AppError(404, "unknown_gateway", "Unknown payment gateway")
    if not verify_webhook_signature(raw_body, signature):
        raise AppError(400, "invalid_signature", "Webhook signature verification failed")
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise AppError(400, "invalid_payload", "Webhook body is not JSON")
    event = payload.get("event", "")
    entity = (payload.get("payload", {}).get("payment") or {}).get("entity") or {}
    eid = event_id or f"{event}:{entity.get('id') or payload.get('created_at')}"
    try:
        db.add(PaymentWebhookEvent(gateway=gateway, event_id=eid, payload=payload))
        db.flush()
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate"}

    result = "ignored"
    if event in ("payment.captured", "order.paid"):
        gw_order = entity.get("order_id") or ((payload.get("payload", {}).get("order") or {}).get("entity") or {}).get("id")
        order = db.scalar(select(Order).where(Order.gateway_order_id == gw_order))
        if order is not None:
            db.commit()  # persist the idempotency row first
            result = "fulfilled" if fulfil(db, order, entity.get("id")) else "already_paid"
    elif event == "payment.failed":
        order = db.scalar(select(Order).where(Order.gateway_order_id == entity.get("order_id")))
        if order is not None and order.status == "created":
            order.status = "failed"
            result = "marked_failed"
    elif event == "subscription.charged":
        result = _renew_subscription(db, payload)
    elif event in ("subscription.cancelled", "subscription.halted"):
        sub_entity = (payload.get("payload", {}).get("subscription") or {}).get("entity") or {}
        sub = db.scalar(select(Subscription).where(Subscription.mandate_ref == sub_entity.get("id")))
        if sub is not None:
            sub.status = "cancelled"
            sub.cancelled_at = utcnow()
            result = "subscription_cancelled"
    db.commit()
    return {"status": result}


def _renew_subscription(db: Session, payload: dict) -> str:
    """Auto-renew charge from the gateway mandate: a new paid order + fresh credits (old ones expire at renewal)."""
    sub_entity = (payload.get("payload", {}).get("subscription") or {}).get("entity") or {}
    pay = (payload.get("payload", {}).get("payment") or {}).get("entity") or {}
    sub = db.scalar(select(Subscription).where(Subscription.mandate_ref == sub_entity.get("id")))
    if sub is None:
        return "unknown_subscription"
    plan = db.get(Plan, sub.plan_id)
    _, gst = gst_split(plan.price_paise)
    order = Order(user_id=sub.user_id, plan_id=plan.id, amount_paise=plan.price_paise, gst_amount_paise=gst,
                  gateway=sub.gateway, status="created", gateway_order_id=pay.get("order_id"),
                  subscription_id=sub.id)
    db.add(order)
    db.flush()
    fulfil(db, order, pay.get("id"))
    return "renewed"


def cancel_subscription(db: Session, user: User, subscription_id: int) -> Subscription:
    """Auto-renew off; the plan stays active until the end of the paid period (PDF 7)."""
    sub = db.get(Subscription, subscription_id)
    if sub is None or sub.user_id != user.id:
        raise not_found("Subscription")
    if sub.status != "active":
        return sub
    if sub.mandate_ref:
        get_gateway().cancel_subscription(sub.mandate_ref)
    sub.status = "cancelled"
    sub.cancelled_at = utcnow()
    db.commit()
    return sub


def expire_subscriptions(db: Session) -> int:
    now = utcnow()
    n = 0
    for sub in db.scalars(select(Subscription).where(Subscription.status.in_(("active", "cancelled")),
                                                     Subscription.renews_at < now - timedelta(days=1))):
        # Active subscriptions without a renewal charge within a day of the due date lapse as well.
        sub.status = "expired"
        n += 1
    db.commit()
    return n


def refund(db: Session, order: Order, reason: str) -> Order:
    if order.status != "paid":
        raise AppError(409, "not_refundable", "Only paid orders can be refunded")
    if order.gateway_payment_id:
        get_gateway().refund(order.gateway_payment_id, order.amount_paise)
    order.status = "refunded"
    order.refunded_at = utcnow()
    order.refund_reason = reason
    if order.credit_grant_id:
        credits.revoke_grant_remaining(db, db.get(CreditLedger, order.credit_grant_id))
    if order.subscription_id:
        sub = db.get(Subscription, order.subscription_id)
        if sub is not None and sub.status in ("active", "cancelled"):
            sub.status = "expired"
    n = notify(db, order.user_id, "refund_processed", {"order_id": str(order.id)},
               amount=f"{order.amount_paise / 100:.0f}", order=order.invoice_no or str(order.id)[:8])
    db.commit()
    dispatch_after_commit(n.id)
    return order


def order_out(o: Order, plan: Plan | None = None) -> dict:
    base = get_settings().public_base_url.rstrip("/") + get_settings().api_prefix
    return {"id": o.id, "plan_id": o.plan_id, "plan_code": plan.code if plan else None,
            "plan_name": plan.name if plan else None, "amount_paise": o.amount_paise,
            "gst_amount_paise": o.gst_amount_paise, "status": o.status, "gateway": o.gateway,
            "gateway_order_id": o.gateway_order_id, "invoice_no": o.invoice_no, "client_platform": o.client_platform,
            "created_at": o.created_at, "paid_at": o.paid_at, "refunded_at": o.refunded_at,
            "invoice_url": f"{base}/orders/{o.id}/invoice" if o.status in ("paid", "refunded") else None}
