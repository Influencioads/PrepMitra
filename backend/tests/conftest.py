"""Test harness.

Default: a throwaway SQLite database (schema from the models), so the suite runs anywhere with no services.
Set TEST_DATABASE_URL=postgresql+psycopg://... to run the same suite against PostgreSQL + pgvector, migrated
with Alembic (this is what CI should do).
"""

import os
import tempfile
from pathlib import Path

_TMP = Path(tempfile.mkdtemp(prefix="prepmitra-tests-"))
os.environ["APP_ENV"] = "test"
os.environ["AI_PROVIDER"] = "mock"
os.environ["JOB_MODE"] = "eager"
os.environ["RUN_SCHEDULER_IN_API"] = "false"
os.environ["PAYMENT_GATEWAY"] = "mock"
os.environ["REDIS_URL"] = ""
os.environ["RAZORPAY_WEBHOOK_SECRET"] = ""
os.environ["FIREBASE_PROJECT_ID"] = ""
os.environ["PUSH_PROVIDER"] = "console"
os.environ["STORAGE_DIR"] = str(_TMP / "storage")
os.environ["JWT_SECRET"] = "test-secret-not-for-production-use-0123456789"
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL") or f"sqlite:///{(_TMP / 'test.db').as_posix()}"

import pytest  # noqa: E402
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import select, text  # noqa: E402

from app.ai.provider import MockProvider  # noqa: E402
from app.core.cache import get_redis  # noqa: E402
from app.db import Base, SessionLocal, engine, is_postgres  # noqa: E402
from app.main import app  # noqa: E402
from app.models import AdminUser, Exam, User  # noqa: E402

BACKEND = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def migrated_db():
    if is_postgres():
        with engine.begin() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
        cfg = Config(str(BACKEND / "alembic.ini"))
        cfg.set_main_option("script_location", str(BACKEND / "alembic"))
        cfg.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
        command.upgrade(cfg, "head")
    else:
        Base.metadata.create_all(engine)
    yield


@pytest.fixture(autouse=True)
def clean_state():
    MockProvider.reset()
    get_redis().flushall()
    yield
    MockProvider.reset()
    tables = list(reversed(Base.metadata.sorted_tables))
    with engine.begin() as conn:
        if is_postgres():
            conn.execute(text(f"TRUNCATE {', '.join(f'"{t.name}"' for t in tables)} RESTART IDENTITY CASCADE"))
        else:
            conn.execute(text("PRAGMA foreign_keys=OFF"))
            for t in tables:
                conn.execute(t.delete())
            conn.execute(text("PRAGMA foreign_keys=ON"))


@pytest.fixture
def db():
    with SessionLocal() as s:
        yield s


@pytest.fixture
def client():
    return TestClient(app)


def login(client: TestClient, phone: str = "9876543210") -> dict:
    otp = client.post("/v1/auth/otp/send", json={"phone": phone}).json()["dev_otp"]
    return client.post("/v1/auth/otp/verify", json={"phone": phone, "code": otp}).json()


def auth_headers(tokens: dict) -> dict:
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def complete_profile(client: TestClient, headers: dict, language: str = "en") -> None:
    assert client.post("/v1/me/consents", headers=headers, json={"data_processing": True}).status_code == 200
    r = client.patch("/v1/me", headers=headers, json={
        "name": "Asha Kumar", "dob": "2000-05-14", "preferred_language": language, "education": "graduate",
        "target_exam_ids": ["ssc-cgl-tier1"]})
    assert r.status_code == 200, r.text


@pytest.fixture
def user_headers(client):
    return auth_headers(login(client))


@pytest.fixture
def ready_user(client):
    """Logged-in user with a complete profile."""
    h = auth_headers(login(client, "9876500001"))
    complete_profile(client, h)
    return h


def make_admin(client: TestClient, role: str = "founder", phone: str = "9000000001") -> dict:
    login(client, phone)
    with SessionLocal() as s:
        u = s.scalar(select(User).where(User.phone == f"+91{phone}"))
        s.add(AdminUser(user_id=u.id, role=role, permissions=[]))
        s.commit()
    return auth_headers(login(client, phone))  # fresh token after the role exists


@pytest.fixture
def admin_headers(client):
    return make_admin(client)


@pytest.fixture
def catalog_seeded():
    from app.seed import seed

    seed(scope="full")
    with SessionLocal() as s:
        return {e.slug: e.id for e in s.scalars(select(Exam))}


def grant_credits(phone: str, n: int = 5, days: int = 90) -> None:
    from app.services import credits

    with SessionLocal() as s:
        u = s.scalar(select(User).where(User.phone == f"+91{phone}"))
        credits.grant(s, u.id, n, "admin_grant", days)
        s.commit()
