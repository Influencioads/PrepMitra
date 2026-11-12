import io
from datetime import date

from sqlalchemy import select

from app.models import Consent, RefreshToken, User
from tests.conftest import login


def _complete(client, headers):
    client.post("/v1/me/consents", headers=headers, json={"data_processing": True})
    return client.patch("/v1/me", headers=headers, json={
        "name": "Asha Kumar", "dob": "2000-05-14", "preferred_language": "ta",
        "education": "graduate", "target_exam_ids": ["ssc-cgl"],
    })


def test_new_user_profile_is_incomplete(client, user_headers):
    me = client.get("/v1/me", headers=user_headers).json()
    assert me["profile_complete"] is False
    assert set(me["missing_fields"]) >= {"name", "dob", "target_exam_or_role", "data_processing_consent"}
    assert me["consents"]["recruiter_sharing"] is False  # OFF by default


def test_complete_profile(client, user_headers):
    r = _complete(client, user_headers)
    assert r.status_code == 200
    me = r.json()
    assert me["profile_complete"] is True and me["missing_fields"] == []
    assert me["preferred_language"] == "ta" and me["profile"]["target_exam_ids"] == ["ssc-cgl"]


def test_under_18_rejected(client, user_headers):
    today = date.today()
    r = client.patch("/v1/me", headers=user_headers, json={"dob": f"{today.year - 17}-01-01"})
    assert r.status_code == 403 and r.json()["error"]["code"] == "underage"


def test_unsupported_language_and_bad_education(client, user_headers):
    assert client.patch("/v1/me", headers=user_headers, json={"preferred_language": "xx"}).status_code == 422
    assert client.patch("/v1/me", headers=user_headers, json={"education": "phd"}).status_code == 422


def test_consent_required_and_recorded(client, user_headers, db):
    r = client.post("/v1/me/consents", headers=user_headers, json={"data_processing": False})
    assert r.status_code == 422
    r = client.post("/v1/me/consents", headers=user_headers, json={"data_processing": True, "recruiter_sharing": True})
    assert r.json() == {"data_processing": True, "recruiter_sharing": True, "marketing": False}
    rows = db.scalars(select(Consent)).all()
    assert all(c.policy_version for c in rows) and len(rows) == 3
    # Withdraw recruiter sharing at any time
    assert client.delete("/v1/me/consents/recruiter_sharing", headers=user_headers).status_code == 204
    assert client.get("/v1/me", headers=user_headers).json()["consents"]["recruiter_sharing"] is False


def test_resume_upload_validation(client, user_headers):
    bad = client.post("/v1/me/resume", headers=user_headers,
                      files={"file": ("cv.txt", b"hello", "text/plain")})
    assert bad.status_code == 415
    fake_pdf = client.post("/v1/me/resume", headers=user_headers,
                           files={"file": ("cv.pdf", b"not a pdf", "application/pdf")})
    assert fake_pdf.status_code == 415
    big = client.post("/v1/me/resume", headers=user_headers,
                      files={"file": ("cv.pdf", b"%PDF" + b"0" * (5 * 1024 * 1024 + 1), "application/pdf")})
    assert big.status_code == 413


def test_resume_upload_docx(client, user_headers, db):
    from docx import Document

    buf = io.BytesIO()
    doc = Document()
    doc.add_paragraph("Python developer with Django experience")
    doc.save(buf)
    r = client.post("/v1/me/resume", headers=user_headers, files={"file": ("cv.docx", buf.getvalue(), "application/octet-stream")})
    assert r.status_code == 200 and r.json()["profile"]["has_resume"] is True
    user = db.scalar(select(User))
    db.refresh(user.profile)
    assert "Django" in user.profile.resume_text
    assert client.delete("/v1/me/resume", headers=user_headers).json()["profile"]["has_resume"] is False


def test_export_data(client, user_headers):
    _complete(client, user_headers)
    data = client.get("/v1/me/export", headers=user_headers).json()
    assert data["account"]["name"] == "Asha Kumar"
    assert {c["type"] for c in data["consents"]} == {"data_processing", "recruiter_sharing", "marketing"}


def test_delete_account_scrubs_pii_and_revokes(client, db):
    tokens = login(client)
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    _complete(client, headers)
    assert client.delete("/v1/me", headers=headers).status_code == 204
    user = db.scalar(select(User))
    assert user.status == "deleted" and user.phone is None and user.name is None and user.dob is None
    assert all(t.revoked_at is not None for t in db.scalars(select(RefreshToken)))
    assert client.get("/v1/me", headers=headers).status_code == 401
    # Same phone can sign up again as a brand-new account
    assert login(client)["is_new_user"] is True
