from datetime import timedelta

from sqlalchemy import select

from app.db import utcnow
from app.models import OtpCode, User
from tests.conftest import auth_headers, login


def test_health(client):
    assert client.get("/v1/health").json()["status"] == "ok"


def test_otp_signup_creates_user_and_returns_tokens(client, db):
    tokens = login(client, "+91 98765 43210")
    assert tokens["is_new_user"] is True
    assert tokens["access_token"] and tokens["refresh_token"]
    user = db.scalar(select(User).where(User.phone == "+919876543210"))
    assert user is not None and user.profile is not None
    # OTP stored hashed, never in plain text
    otp = db.scalar(select(OtpCode))
    assert len(otp.code_hash) == 64 and otp.consumed_at is not None


def test_second_login_is_not_new(client):
    login(client)
    assert login(client)["is_new_user"] is False


def test_invalid_phone_rejected(client):
    r = client.post("/v1/auth/otp/send", json={"phone": "12345"})
    assert r.status_code == 422


def test_wrong_otp_and_lockout(client):
    client.post("/v1/auth/otp/send", json={"phone": "9876543210"})
    for _ in range(5):
        r = client.post("/v1/auth/otp/verify", json={"phone": "9876543210", "code": "000000"})
        assert r.status_code in (400, 429)
    # Even a guess after 5 failures is refused
    r = client.post("/v1/auth/otp/verify", json={"phone": "9876543210", "code": "000000"})
    assert r.status_code == 429 and r.json()["error"]["code"] == "otp_locked"


def test_expired_otp(client, db):
    code = client.post("/v1/auth/otp/send", json={"phone": "9876543210"}).json()["dev_otp"]
    otp = db.scalar(select(OtpCode))
    otp.expires_at = utcnow() - timedelta(seconds=1)
    db.commit()
    r = client.post("/v1/auth/otp/verify", json={"phone": "9876543210", "code": code})
    assert r.status_code == 400 and r.json()["error"]["code"] == "otp_expired"


def test_otp_send_rate_limit(client):
    for _ in range(5):
        assert client.post("/v1/auth/otp/send", json={"phone": "9876543210"}).status_code == 200
    r = client.post("/v1/auth/otp/send", json={"phone": "9876543210"})
    assert r.status_code == 429


def test_refresh_rotation_and_reuse_detection(client):
    tokens = login(client)
    r1 = client.post("/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert r1.status_code == 200
    new = r1.json()
    # Reusing the old (rotated) token is rejected and revokes the new one too
    assert client.post("/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}).status_code == 401
    assert client.post("/v1/auth/refresh", json={"refresh_token": new["refresh_token"]}).status_code == 401


def test_logout_revokes_refresh(client):
    tokens = login(client)
    assert client.post("/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]}).status_code == 204
    assert client.post("/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}).status_code == 401


def test_me_requires_token(client):
    assert client.get("/v1/me").status_code == 401
    assert client.get("/v1/me", headers={"Authorization": "Bearer junk"}).status_code == 401


def test_blocked_user_cannot_use_api(client, db):
    tokens = login(client)
    user = db.scalar(select(User))
    user.status = "blocked"
    db.commit()
    assert client.get("/v1/me", headers=auth_headers(tokens)).status_code == 403


def test_google_not_configured(client):
    r = client.post("/v1/auth/google", json={"id_token": "x" * 20})
    assert r.status_code == 503
