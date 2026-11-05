import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import get_settings
from app.core.errors import install_error_handlers
from app.core.languages import LANGUAGES
from app.db import SessionLocal
from app.routers import (
    admin_content,
    admin_ops,
    attempts,
    auth,
    billing,
    catalog,
    engagement,
    interviews,
    me,
    mentor,
    reports,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
settings = get_settings()

if settings.sentry_dsn:
    try:
        import sentry_sdk

        # send_default_pii=False: no IPs, headers or bodies (answers, resumes) leave our servers.
        sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.app_env, send_default_pii=False,
                        traces_sample_rate=settings.sentry_traces_sample_rate)
    except ImportError:
        logging.getLogger(__name__).warning("SENTRY_DSN is set but sentry-sdk is not installed")


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = None
    if settings.run_scheduler_in_api and settings.job_mode != "eager":
        from app.jobs.scheduler import Scheduler

        scheduler = Scheduler()
        scheduler.start()
    yield
    if scheduler is not None:
        scheduler.stop()


TAGS = [
    {"name": "auth", "description": "Mobile OTP and Google sign-in, JWT access + rotating refresh tokens."},
    {"name": "me", "description": "Profile, consents (DPDP), data export, account deletion, resume."},
    {"name": "catalog", "description": "Exams, interview roles, plans, enums and policies. Public."},
    {"name": "exams", "description": "Timed mock exams: start, resume, autosave, anti-cheat events, submit, review."},
    {"name": "reports", "description": "AI result reports: poll, rate, share, PDF."},
    {"name": "interviews", "description": "AI mock interviews over REST or WebSocket (text and voice)."},
    {"name": "payments", "description": "Credits, orders, checkout verification, webhooks, subscriptions, invoices."},
    {"name": "dashboard & notifications", "description": "Progress dashboard, notification inbox, push devices."},
]

app = FastAPI(
    title=f"{settings.app_name} API", version="1.0.0", lifespan=lifespan, openapi_tags=TAGS,
    # Swagger UI keeps the Authorize token across page reloads; long lists stay collapsed.
    swagger_ui_parameters={"persistAuthorization": True, "docExpansion": "none", "displayRequestDuration": True,
                           "tryItOutEnabled": True},
    description="One REST + WebSocket API for the website and the Android/iOS apps. All endpoints are under /v1. "
                "Errors always look like {\"error\": {\"code\", \"message\", \"details\"?}}. See docs/API.md.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "Content-Disposition"],
)
install_error_handlers(app)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if not settings.is_dev:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.get(f"{settings.api_prefix}/health", tags=["catalog"])
def health():
    with SessionLocal() as db:
        db.execute(text("select 1"))
    redis_ok = None
    if settings.redis_url:
        from app.core.cache import get_redis

        try:
            redis_ok = bool(get_redis().ping())
        except Exception:
            redis_ok = False
    from app.ai.provider import get_provider

    return {"status": "ok", "app": settings.app_name, "env": settings.app_env, "version": app.version,
            "ai_provider": get_provider().name, "payments": "mock" if settings.payments_mock else "razorpay",
            "jobs": settings.job_mode, "redis": redis_ok}


@app.get(f"{settings.api_prefix}/languages", tags=["catalog"])
def languages():
    return [{"code": k, **v} for k, v in LANGUAGES.items()]


for r in (auth.router, me.router, me.uploads, catalog.router, attempts.router, reports.router, interviews.router,
          billing.router, engagement.router, mentor.router, admin_content.router, admin_ops.router):
    app.include_router(r, prefix=settings.api_prefix)
