"""Payment gateway adapters. Card/UPI data never touches our servers; the gateway's checkout handles it (PCI-DSS).

RazorpayGateway   real Razorpay REST API (use TEST-mode keys until launch checks are complete)
MockGateway       used when keys are missing or PAYMENT_GATEWAY=mock; orders are fake and are completed with the
                  dev-only POST /v1/orders/{id}/mock-pay endpoint or with signed webhook fixtures.
Cashfree is named in the PDF as an alternative; it is NOT implemented (add a CashfreeGateway with the same methods).
"""

import hashlib
import hmac
import uuid

import httpx

from app.config import get_settings
from app.core.errors import AppError

DEV_WEBHOOK_SECRET = "dev-webhook-secret"
MOCK_KEY_SECRET = "mock-key-secret"


def hmac_hex(secret: str, message: bytes) -> str:
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


class MockGateway:
    name = "razorpay"
    is_mock = True
    key_id = "rzp_test_mock"
    key_secret = MOCK_KEY_SECRET

    def create_order(self, amount_paise: int, receipt: str, notes: dict) -> str:
        return f"order_mock_{uuid.uuid4().hex[:14]}"

    def refund(self, payment_id: str, amount_paise: int) -> str:
        return f"rfnd_mock_{uuid.uuid4().hex[:10]}"

    def cancel_subscription(self, mandate_ref: str) -> None:
        return None


class RazorpayGateway:
    name = "razorpay"
    is_mock = False
    base = "https://api.razorpay.com/v1"

    def __init__(self):
        s = get_settings()
        self.key_id, self.key_secret = s.razorpay_key_id, s.razorpay_key_secret

    def _post(self, path: str, payload: dict) -> dict:
        try:
            r = httpx.post(f"{self.base}{path}", json=payload, auth=(self.key_id, self.key_secret), timeout=15)
        except httpx.HTTPError as e:
            raise AppError(502, "gateway_unreachable", "Payment gateway is unreachable. Please try again.") from e
        if r.status_code >= 400:
            raise AppError(502, "gateway_error", "Payment gateway rejected the request")
        return r.json()

    def create_order(self, amount_paise: int, receipt: str, notes: dict) -> str:
        return self._post("/orders", {"amount": amount_paise, "currency": "INR", "receipt": receipt[:40],
                                      "notes": notes})["id"]

    def refund(self, payment_id: str, amount_paise: int) -> str:
        return self._post(f"/payments/{payment_id}/refund", {"amount": amount_paise})["id"]

    def cancel_subscription(self, mandate_ref: str) -> None:
        self._post(f"/subscriptions/{mandate_ref}/cancel", {"cancel_at_cycle_end": 1})


def get_gateway():
    return MockGateway() if get_settings().payments_mock else RazorpayGateway()


def webhook_secret() -> str:
    s = get_settings()
    if s.razorpay_webhook_secret:
        return s.razorpay_webhook_secret
    if s.is_dev:
        return DEV_WEBHOOK_SECRET
    raise AppError(503, "webhooks_not_configured", "Payment webhooks are not configured")


def verify_checkout_signature(gateway_order_id: str, payment_id: str, signature: str) -> bool:
    """Razorpay checkout signature: HMAC_SHA256(order_id|payment_id, key_secret)."""
    expected = hmac_hex(get_gateway().key_secret, f"{gateway_order_id}|{payment_id}".encode())
    return hmac.compare_digest(expected, signature or "")


def verify_webhook_signature(raw_body: bytes, signature: str) -> bool:
    return hmac.compare_digest(hmac_hex(webhook_secret(), raw_body), signature or "")
