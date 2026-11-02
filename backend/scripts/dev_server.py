"""Zero-setup dev server for trying the API in Swagger (no Docker, no API keys).

    cd backend && .venv/Scripts/python scripts/dev_server.py [--port 8000]

Uses a local SQLite file (backend/dev.db), the mock AI provider and the mock payment gateway, creates + seeds the
schema on first run, and makes DEV_ADMIN_PHONE (default 9000000009) a founder admin at first login.
Any of these can be overridden with real environment variables. Not for production: use PostgreSQL + Alembic.
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
os.environ.setdefault("PAYMENT_GATEWAY", "mock")
os.environ.setdefault("JOB_MODE", "thread")
os.environ.setdefault("REDIS_URL", "")
os.environ.setdefault("BOOTSTRAP_ADMIN_PHONE", os.environ.get("DEV_ADMIN_PHONE", "9000000009"))
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:8000")
# Port: PORT env var or `--port N` (8000 by default).
port = int(sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else os.environ.get("PORT", "8000"))
os.environ.setdefault("PUBLIC_BASE_URL", f"http://localhost:{port}")


def main() -> None:
    import uvicorn
    from sqlalchemy import inspect

    import app.models  # noqa: F401
    from app.db import Base, engine
    from app.seed import seed

    fresh = not inspect(engine).has_table("exams")
    Base.metadata.create_all(engine)
    if fresh:
        # SEED_SCOPE=full publishes all 15 exams and 6 roles instead of the 15-day launch catalog.
        print("Seeding:", seed(scope=os.environ.get("SEED_SCOPE", "launch")))
    print(f"\nSwagger UI: http://localhost:{port}/docs   (admin phone: {os.environ['BOOTSTRAP_ADMIN_PHONE']})\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
