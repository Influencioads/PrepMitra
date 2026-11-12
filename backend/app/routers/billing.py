import uuid

from fastapi import APIRouter, Depends, Header, Query, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.deps import get_current_user
from app.core.errors import AppError, not_found
from app.core.ratelimit import hit
from app.db import get_db
from app.models import Order, Plan, Subscription, User
from app.schemas.common import IapVerifyIn, OrderIn, OrderVerifyIn
from app.services import allowances, credits, payments, pdf

router = APIRouter(tags=["payments"])


@router.get("/me/credits")
def my_credits(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Credit balance with per-grant expiry (oldest-expiring credits are used first)."""
    return credits.balance(db, user.id)


@router.get("/me/allowances")
def my_allowances(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """AI allowances from every plan the student holds now: feature switches, and for each metered feature the
    limit, used and remaining this month (subscriptions), per add-on, and for life (Free)."""
    return allowances.summary(db, user)


@router.post("/orders", status_code=201)
def create_order(body: OrderIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Creates a payment order and returns Razorpay checkout options for web, Android and iOS SDKs."""
    hit(f"orders:{user.id}", 10, 60)
    return payments.create_order(db, user, body.plan_code, body.platform)


@router.post("/orders/verify")
def verify_by_gateway_order(body: OrderVerifyIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """API Plan form: send the three values Razorpay Checkout returns. Idempotent."""
    o = db.scalar(select(Order).where(Order.gateway_order_id == body.razorpay_order_id, Order.user_id == user.id))         if body.razorpay_order_id else None
    if o is None:
        raise not_found("Order")
    o = payments.verify_checkout(db, user, o.id, body.razorpay_payment_id, body.razorpay_signature)
    return payments.order_out(o, db.get(Plan, o.plan_id)) | {"credits": credits.balance(db, user.id)}


@router.get("/orders")
def my_orders(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0),
              user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc())
                      .limit(limit).offset(offset)).all()
    plans = {p.id: p for p in db.scalars(select(Plan))}
    return {"items": [payments.order_out(o, plans.get(o.plan_id)) for o in rows], "limit": limit, "offset": offset}


@router.get("/orders/{order_id}")
def get_order(order_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if o is None or o.user_id != user.id:
        raise not_found("Order")
    return payments.order_out(o, db.get(Plan, o.plan_id))


@router.post("/orders/{order_id}/verify")
def verify(order_id: uuid.UUID, body: OrderVerifyIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Call after checkout succeeds with the gateway's payment id and signature. Idempotent."""
    o = payments.verify_checkout(db, user, order_id, body.razorpay_payment_id, body.razorpay_signature)
    return payments.order_out(o, db.get(Plan, o.plan_id)) | {"credits": credits.balance(db, user.id)}


@router.post("/orders/{order_id}/mock-pay")
def mock_pay(order_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """DEVELOPMENT ONLY: completes an order created against the mock gateway (no real money)."""
    s = get_settings()
    if not (s.is_dev and s.payments_mock):
        raise not_found("Endpoint")
    o = db.get(Order, order_id)
    if o is None or o.user_id != user.id:
        raise not_found("Order")
    payments.fulfil(db, o, f"pay_mock_{uuid.uuid4().hex[:12]}")
    return payments.order_out(o, db.get(Plan, o.plan_id)) | {"credits": credits.balance(db, user.id)}


@router.get("/orders/{order_id}/invoice", response_class=Response)
def invoice(order_id: uuid.UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if o is None or o.user_id != user.id:
        raise not_found("Order")
    return invoice_response(db, o)


def invoice_response(db: Session, o: Order) -> Response:
    if o.status not in ("paid", "refunded") or not o.invoice_no:
        raise AppError(409, "no_invoice", "An invoice is available once the payment succeeds")
    buyer = db.get(User, o.user_id)
    data = pdf.invoice_pdf(order=o, plan_name=db.get(Plan, o.plan_id).name, buyer_name=buyer.name, buyer_state=buyer.state)
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="invoice-{o.invoice_no.replace("/", "-")}.pdf"'})


@router.post("/webhooks/razorpay")
async def webhook_razorpay(request: Request, x_razorpay_signature: str = Header(default=""),
                           x_razorpay_event_id: str | None = Header(default=None), db: Session = Depends(get_db)):
    """Razorpay webhook URL to configure in the Razorpay dashboard (same handler as /webhooks/payments/razorpay)."""
    return payments.handle_webhook(db, "razorpay", await request.body(), x_razorpay_signature, x_razorpay_event_id)


@router.post("/webhooks/payments/{gateway}")
async def webhook(gateway: str, request: Request, x_razorpay_signature: str = Header(default=""),
                  x_razorpay_event_id: str | None = Header(default=None), db: Session = Depends(get_db)):
    """Gateway callbacks. Signature-verified over the raw body and processed idempotently."""
    raw = await request.body()
    return payments.handle_webhook(db, gateway, raw, x_razorpay_signature, x_razorpay_event_id)


@router.get("/subscriptions")
def my_subscriptions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subs = db.scalars(select(Subscription).where(Subscription.user_id == user.id)
                      .order_by(Subscription.created_at.desc())).all()
    return {"items": [{"id": s.id, "plan_id": s.plan_id, "status": s.status, "renews_at": s.renews_at,
                       "current_period_start": s.current_period_start, "cancelled_at": s.cancelled_at,
                       "auto_renew": s.status == "active" and bool(s.mandate_ref)} for s in subs]}


@router.post("/subscriptions/{subscription_id}/cancel")
def cancel(subscription_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Turns off auto-renew. The plan and its credits stay valid until expiry."""
    s = payments.cancel_subscription(db, user, subscription_id)
    return {"id": s.id, "status": s.status, "renews_at": s.renews_at}


@router.post("/iap/verify", status_code=501)
def iap_verify(body: IapVerifyIn, user: User = Depends(get_current_user)):
    """In-app purchase verification (Google Play Billing / Apple StoreKit).

    INCOMPLETE: needs Play Developer API and App Store Server API credentials, plus the legal/payments decision
    from PDF section 7 on store billing vs. web checkout. Mobile apps should use the Razorpay order flow until then.
    """
    raise AppError(501, "not_implemented", "In-app store billing is not enabled yet; use the standard checkout")
