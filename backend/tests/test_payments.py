"""Plans, orders, checkout verification, signed idempotent webhooks, subscriptions, refunds, invoices (PDF 7)."""

import json
import uuid
from datetime import timedelta

from sqlalchemy import select

from app.db import SessionLocal, utcnow
from app.models import CreditLedger, Order, Subscription, User
from app.services import credits
from app.services.gateways import DEV_WEBHOOK_SECRET, MOCK_KEY_SECRET, hmac_hex
from tests.conftest import auth_headers, login


def _order(client, h, plan="pay_per_exam", platform="web"):
    return client.post("/v1/orders", headers=h, json={"plan_code": plan, "platform": platform})


def _webhook(client, body: dict, secret=DEV_WEBHOOK_SECRET, event_id="evt_1"):
    raw = json.dumps(body).encode()
    return client.post("/v1/webhooks/payments/razorpay", content=raw,
                       headers={"X-Razorpay-Signature": hmac_hex(secret, raw), "X-Razorpay-Event-Id": event_id,
                                "Content-Type": "application/json"})


def _captured(gw_order_id, pay_id="pay_1"):
    return {"event": "payment.captured", "payload": {"payment": {"entity": {"id": pay_id, "order_id": gw_order_id}}}}


def test_plans_gst_inclusive(client, catalog_seeded):
    plans = {p["code"]: p for p in client.get("/v1/plans").json()["items"]}
    assert plans["pay_per_exam"]["price_paise"] == 9900 and plans["monthly"]["credits"] == 10
    assert plans["pay_per_exam"]["gst_paise"] == 1510  # 99 * 18/118
    assert plans["free_trial"]["purchasable"] is False


def test_order_checkout_payload_and_signature_verification(client, catalog_seeded, user_headers):
    o = _order(client, user_headers, platform="android").json()
    assert o["mock"] is True and o["checkout_options"]["order_id"] == o["gateway_order_id"]
    bad = client.post(f"/v1/orders/{o['order_id']}/verify", headers=user_headers,
                      json={"razorpay_payment_id": "pay_x", "razorpay_signature": "0" * 64})
    assert bad.status_code == 400
    sig = hmac_hex(MOCK_KEY_SECRET, f"{o['gateway_order_id']}|pay_x".encode())
    ok = client.post(f"/v1/orders/{o['order_id']}/verify", headers=user_headers,
                     json={"razorpay_payment_id": "pay_x", "razorpay_signature": sig}).json()
    assert ok["status"] == "paid" and ok["credits"]["total"] == 1 and ok["invoice_no"].startswith("PM/")
    again = client.post(f"/v1/orders/{o['order_id']}/verify", headers=user_headers,
                        json={"razorpay_payment_id": "pay_x", "razorpay_signature": sig}).json()
    assert again["credits"]["total"] == 1


def test_webhook_bad_signature_rejected(client, catalog_seeded, user_headers):
    o = _order(client, user_headers).json()
    r = _webhook(client, _captured(o["gateway_order_id"]), secret="wrong")
    assert r.status_code == 400 and r.json()["error"]["code"] == "invalid_signature"


def test_repeated_webhook_adds_credits_once(client, catalog_seeded, user_headers, db):
    o = _order(client, user_headers, plan="monthly").json()
    assert _webhook(client, _captured(o["gateway_order_id"]), event_id="evt_A").json()["status"] == "fulfilled"
    assert _webhook(client, _captured(o["gateway_order_id"]), event_id="evt_A").json()["status"] == "duplicate"
    # A different event for the same payment (order.paid) is also harmless.
    assert _webhook(client, _captured(o["gateway_order_id"]), event_id="evt_B").json()["status"] == "already_paid"
    assert client.get("/v1/me/credits", headers=user_headers).json()["total"] == 10
    sub = db.scalar(select(Subscription))
    assert sub.status == "active" and (sub.renews_at - utcnow()).days in (29, 30)
    assert _order(client, user_headers, plan="monthly").status_code == 409  # already subscribed


def test_invoice_pdf_and_order_list(client, catalog_seeded, user_headers):
    o = _order(client, user_headers).json()
    assert client.get(f"/v1/orders/{o['order_id']}/invoice", headers=user_headers).status_code == 409
    client.post(f"/v1/orders/{o['order_id']}/mock-pay", headers=user_headers)
    pdf = client.get(f"/v1/orders/{o['order_id']}/invoice", headers=user_headers)
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")
    items = client.get("/v1/orders", headers=user_headers).json()["items"]
    assert items[0]["status"] == "paid" and items[0]["invoice_url"]


def test_cancel_subscription_keeps_plan_until_expiry(client, catalog_seeded, user_headers):
    o = _order(client, user_headers, plan="monthly").json()
    client.post(f"/v1/orders/{o['order_id']}/mock-pay", headers=user_headers)
    sub = client.get("/v1/subscriptions", headers=user_headers).json()["items"][0]
    out = client.post(f"/v1/subscriptions/{sub['id']}/cancel", headers=user_headers).json()
    assert out["status"] == "cancelled" and out["renews_at"]
    assert client.get("/v1/me/credits", headers=user_headers).json()["total"] == 10


def test_credit_expiry_ordering_and_expiry_job(client, user_headers, db):
    user = db.scalar(select(User))
    late = credits.grant(db, user.id, 2, "purchase", 30)
    early = credits.grant(db, user.id, 1, "purchase", 3)
    forever = credits.grant(db, user.id, 1, "admin_grant", None)
    db.commit()
    b = credits.balance(db, user.id)
    assert [g["id"] for g in b["grants"]] == [early.id, late.id, forever.id] and b["total"] == 4
    expired = credits.grant(db, user.id, 5, "purchase", 1)
    expired.expires_at = utcnow() - timedelta(hours=1)
    db.commit()
    assert credits.balance(db, user.id)["total"] == 4
    assert credits.expire_credits(db) == 1 and credits.expire_credits(db) == 0
    assert db.scalar(select(CreditLedger).where(CreditLedger.reason == "expiry")).delta == -5


def test_admin_refund_revokes_unused_credits(client, catalog_seeded, user_headers, admin_headers):
    o = _order(client, user_headers, plan="monthly").json()
    client.post(f"/v1/orders/{o['order_id']}/mock-pay", headers=user_headers)
    r = client.post(f"/v1/admin/orders/{o['order_id']}/refund", headers=admin_headers, json={"reason": "duplicate payment"})
    assert r.json()["status"] == "refunded"
    assert client.get("/v1/me/credits", headers=user_headers).json()["total"] == 0
    assert client.get("/v1/subscriptions", headers=user_headers).json()["items"][0]["status"] == "expired"


def test_mock_pay_not_available_for_other_users(client, catalog_seeded, user_headers):
    o = _order(client, user_headers).json()
    other = auth_headers(login(client, "9123456780"))
    assert client.post(f"/v1/orders/{o['order_id']}/mock-pay", headers=other).status_code == 404


def test_iap_is_explicitly_not_implemented(client, user_headers):
    r = client.post("/v1/iap/verify", headers=user_headers,
                    json={"platform": "android", "product_id": "monthly", "purchase_token": "x"})
    assert r.status_code == 501 and r.json()["error"]["code"] == "not_implemented"
