"""Creates local test accounts (one per admin role plus learners with credits) in the development database.

    cd backend && .venv/Scripts/python scripts/dev_test_accounts.py

Development only: refuses to run unless APP_ENV is development/test and the database is SQLite. Log in on the website
with VITE_AUTH_PROVIDER=demo: enter the phone number, and the development backend shows the OTP on screen.
Safe to re-run: existing accounts keep their data; learners are topped up to at least 20 credits.
"""

import os
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
os.chdir(BACKEND)
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{(BACKEND / 'dev.db').as_posix()}")
os.environ.setdefault("AI_PROVIDER", "mock")

from sqlalchemy import select  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models import AdminUser, User  # noqa: E402
from app.services import credits  # noqa: E402
from app.services.auth import _create_user, normalize_phone  # noqa: E402

# phone, name, admin role (None = learner)
ACCOUNTS = [
    ("9000000009", "Founder Admin", "founder"),
    ("9000000010", "Content Manager", "content_manager"),
    ("9000000011", "Subject Expert", "subject_expert"),
    ("9000000012", "Language Reviewer", "language_reviewer"),
    ("9000000013", "Support Agent", "support"),
    ("9000000014", "Finance Admin", "finance"),
    ("9000000101", "Test Learner One", None),
    ("9000000102", "Test Learner Two", None),
    ("9000000103", "Test Learner Three", None),
]
LEARNER_CREDITS = 20


def main() -> None:
    s = get_settings()
    if not s.is_dev or not s.database_url.startswith("sqlite"):
        sys.exit("Refusing to run: this script only writes to the local SQLite development database.")
    with SessionLocal() as db:
        for phone, name, role in ACCOUNTS:
            p = normalize_phone(phone)
            user = db.scalar(select(User).where(User.phone == p)) or _create_user(db, phone=p)
            user.name = user.name or name
            if role:
                if user.admin is None:
                    db.add(AdminUser(user_id=user.id, role=role, permissions=[]))
                else:
                    user.admin.role = role
            else:
                have = credits.balance(db, user.id)["total"]
                if have < LEARNER_CREDITS:
                    credits.grant(db, user.id, LEARNER_CREDITS - have, "admin_grant", None, ref_id="dev_test_accounts")
            db.flush()
            print(f"{phone}  {name:20} {role or f'learner ({LEARNER_CREDITS} credits)'}")
        db.commit()


if __name__ == "__main__":
    main()
