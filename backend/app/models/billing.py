import uuid
from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base, TimestampMixin, utcnow, JSONType, TZDateTime


class Plan(TimestampMixin, Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True)  # free_trial | pay_per_exam | monthly | yearly
    name: Mapped[str] = mapped_column(String(80))
    price_paise: Mapped[int] = mapped_column(Integer)  # GST-inclusive
    credits: Mapped[int] = mapped_column(Integer)
    validity_days: Mapped[int] = mapped_column(Integer)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    # What the plan unlocks (blueprint pricing): group (study | tutor | combo | addon), billing period and AI
    # allowances. Subscription allowances are per calendar month; add-on allowances last the add-on's validity.
    entitlements: Mapped[dict] = mapped_column(JSONType, default=dict)


class FeatureUse(Base):
    """One use of a metered AI feature (a doubt, a deep dive, a tutor chat turn...). `source` says which allowance
    paid for it: "plan" (this month's subscription allowance), "free" (lifetime free allowance) or an add-on order id."""

    __tablename__ = "feature_uses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    feature: Mapped[str] = mapped_column(String(40), index=True)
    source: Mapped[str] = mapped_column(String(64))
    ref_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow, index=True)


class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id", ondelete="RESTRICT"))
    amount_paise: Mapped[int] = mapped_column(Integer)
    gst_amount_paise: Mapped[int] = mapped_column(Integer)
    gateway: Mapped[str] = mapped_column(String(20))  # razorpay | cashfree
    gateway_order_id: Mapped[str | None] = mapped_column(String(80), unique=True)
    gateway_payment_id: Mapped[str | None] = mapped_column(String(80))
    # created | paid | failed | refunded
    status: Mapped[str] = mapped_column(String(20), default="created", index=True)
    invoice_no: Mapped[str | None] = mapped_column(String(40), unique=True)
    # web | android | ios: where the purchase started (app-store billing rules differ per platform)
    client_platform: Mapped[str] = mapped_column(String(10), default="web")
    paid_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    refunded_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    refund_reason: Mapped[str | None] = mapped_column(Text)
    credit_grant_id: Mapped[int | None] = mapped_column(ForeignKey("credit_ledger.id", ondelete="SET NULL"))
    subscription_id: Mapped[int | None] = mapped_column(ForeignKey("subscriptions.id", ondelete="SET NULL"))


class Subscription(TimestampMixin, Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id", ondelete="RESTRICT"))
    # active | cancelled (auto-renew off, valid until expiry) | expired
    status: Mapped[str] = mapped_column(String(20), default="active")
    renews_at: Mapped[datetime | None] = mapped_column(TZDateTime)
    mandate_ref: Mapped[str | None] = mapped_column(String(80))
    gateway: Mapped[str] = mapped_column(String(20), default="razorpay")
    current_period_start: Mapped[datetime | None] = mapped_column(TZDateTime)
    cancelled_at: Mapped[datetime | None] = mapped_column(TZDateTime)


class CreditLedger(Base):
    """Every credit added (delta > 0, a 'grant') or used (delta < 0, linked to the grant it consumed)."""

    __tablename__ = "credit_ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    delta: Mapped[int] = mapped_column(Integer)
    # free_trial | purchase | admin_grant | attempt | interview | refund_restore | expiry
    reason: Mapped[str] = mapped_column(String(30))
    expires_at: Mapped[datetime | None] = mapped_column(TZDateTime, index=True)
    grant_id: Mapped[int | None] = mapped_column(ForeignKey("credit_ledger.id", ondelete="SET NULL"), index=True)
    ref_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)


class PaymentWebhookEvent(Base):
    """Idempotency store: a gateway event id is processed at most once."""

    __tablename__ = "payment_webhook_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gateway: Mapped[str] = mapped_column(String(20))
    event_id: Mapped[str] = mapped_column(String(120), unique=True)
    payload: Mapped[dict] = mapped_column(JSONType, default=dict)
    processed_at: Mapped[datetime] = mapped_column(TZDateTime, default=utcnow)
