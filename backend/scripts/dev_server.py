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


def _env_file_value(key: str) -> str:
    for line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines() if (BACKEND / ".env").exists() else []:
        if line.strip().startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return ""


os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{(BACKEND / 'dev.db').as_posix()}")
# AI: OpenRouter (blueprint model routing) once backend/.env has OPENROUTER_API_KEY, else Claude with an Anthropic
# key, else the free mock AI.
if os.environ.get("OPENROUTER_API_KEY") or _env_file_value("OPENROUTER_API_KEY"):
    os.environ.setdefault("AI_PROVIDER", "openrouter")
elif os.environ.get("ANTHROPIC_API_KEY") or _env_file_value("ANTHROPIC_API_KEY"):
    os.environ.setdefault("AI_PROVIDER", "claude")
else:
    os.environ.setdefault("AI_PROVIDER", "mock")
os.environ.setdefault("PAYMENT_GATEWAY", "mock")
os.environ.setdefault("JOB_MODE", "thread")
os.environ.setdefault("REDIS_URL", "")
os.environ.setdefault("BOOTSTRAP_ADMIN_PHONE", os.environ.get("DEV_ADMIN_PHONE", "9000000009"))
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:8000")
# Port: PORT env var or `--port N` (8000 by default).
port = int(sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else os.environ.get("PORT", "8000"))
os.environ.setdefault("PUBLIC_BASE_URL", f"http://localhost:{port}")


def _add_missing_columns(engine, base) -> None:
    """create_all never alters existing tables. On an older dev.db, add columns introduced since (additive only,
    the dev equivalent of an Alembic upgrade; PostgreSQL uses the real migrations)."""
    from sqlalchemy import inspect, text

    insp = inspect(engine)
    with engine.begin() as conn:
        for table in base.metadata.sorted_tables:
            have = {c["name"] for c in insp.get_columns(table.name)}
            for col in table.columns:
                if col.name in have:
                    continue
                ddl = col.type.compile(dialect=engine.dialect)
                default = col.server_default.arg if col.server_default is not None else None
                suffix = f" DEFAULT {default}" if isinstance(default, str) else ""
                conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {ddl}{suffix}'))
                print(f"dev.db: added {table.name}.{col.name}")


def main() -> None:
    import uvicorn
    from sqlalchemy import inspect

    import app.models  # noqa: F401
    from app.db import Base, engine
    from app.seed import seed

    fresh = not inspect(engine).has_table("exams")
    Base.metadata.create_all(engine)
    _add_missing_columns(engine, Base)
    if fresh:
        # SEED_SCOPE=full publishes all 18 exams and 6 roles instead of the 15-day launch catalog.
        print("Seeding:", seed(scope=os.environ.get("SEED_SCOPE", "launch")))
    else:  # keep prices and allowances in step with app/services/plan_catalog.py
        from app.db import SessionLocal
        from app.seed import seed_plans

        with SessionLocal() as db:
            seed_plans(db)
            db.commit()
    print(f"\nSwagger UI: http://localhost:{port}/docs   (admin phone: {os.environ['BOOTSTRAP_ADMIN_PHONE']})\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
