from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    app_name: str = "PrepMitra AI"
    app_env: str = "development"  # development | test | production
    api_prefix: str = "/v1"
    cors_origins: str = "http://localhost:5173"
    # Public URL of this API, used to build share links and file URLs for web/mobile clients.
    public_base_url: str = "http://localhost:8000"
    # Public URL of the website, used in share links that open in a browser.
    web_base_url: str = "http://localhost:5173"

    database_url: str = "postgresql+psycopg://prepmitra:prepmitra@localhost:5432/prepmitra"
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Redis: job queue, rate limits, catalog cache. Empty = in-process fallbacks (single instance dev only).
    redis_url: str = ""
    # eager: run jobs inline (tests) | thread: in-process thread pool (dev) | redis: queue consumed by `python -m app.worker`
    job_mode: str = "thread"
    # Run the periodic scheduler (auto-submit, report timeouts, notifications, pre-generation) inside the API process.
    # Set false in production and run `python -m app.worker` instead.
    run_scheduler_in_api: bool = True

    # Auth
    jwt_secret: str = "change-me-in-env"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    otp_length: int = 6
    otp_ttl_seconds: int = 300
    otp_max_attempts: int = 5
    otp_send_limit_per_hour: int = 5
    # Firebase Authentication (phone OTP + Google on the client). Set to accept Firebase ID tokens.
    firebase_project_id: str = ""
    google_client_id: str = ""
    # Extra accepted Google client IDs (Android/iOS apps), comma separated.
    google_extra_client_ids: str = ""
    min_age_years: int = 18
    # Turn off only for load tests on a staging box (all simulated users share one IP).
    rate_limits_enabled: bool = True
    # Phone number that becomes a founder admin on first login (seed convenience).
    bootstrap_admin_phone: str = ""

    # AI
    ai_provider: str = "claude"  # claude | mock
    anthropic_api_key: str = ""
    ai_model_strong: str = "claude-opus-5-5"
    ai_model_fast: str = "claude-haiku-5-5"
    ai_timeout_seconds: float = 120.0
    embedding_dim: int = 256
    dedup_similarity_threshold: float = 0.92
    back_translation_min_similarity: float = 0.75
    review_sample_rate: float = 0.10
    auto_quarantine_reports: int = 3

    # Exams / interviews / reports
    attempt_grace_seconds: int = 30  # autosaves accepted this long after the deadline (network latency)
    report_timeout_minutes: int = 10  # credit restored if the report is not ready by then
    interview_resume_minutes: int = 10
    papers_pool_size: int = 3  # pre-generated ready papers kept per exam
    report_share_days: int = 30

    # Speech (voice interviews). mock = dev adapters; real providers plug in per language (PDF section 8).
    speech_provider: str = "mock"

    # Notifications
    email_provider: str = "console"  # console | smtp (Amazon SES SMTP) | resend
    resend_api_key: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "PrepMitra AI <no-reply@prepmitra.local>"
    push_provider: str = "console"  # console | fcm
    # Firebase service-account JSON for FCM HTTP v1. A relative path is resolved from the backend folder.
    fcm_credentials_file: str = ""

    # Monitoring: errors go to Sentry when a DSN is set.
    sentry_dsn: str = ""
    sentry_traces_sample_rate: float = 0.05

    # Storage
    storage_dir: str = "storage"
    max_resume_bytes: int = 5 * 1024 * 1024
    fonts_dir: str = "fonts"  # put Noto *.ttf files here for Indic-script PDFs

    # Payments (test mode only until production keys and checks are in place)
    payment_gateway: str = "razorpay"  # razorpay | mock
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""
    gst_rate_percent: int = 18
    gstin: str = ""
    company_legal_name: str = "PrepMitra AI (placeholder legal entity)"

    @property
    def is_dev(self) -> bool:
        return self.app_env in ("development", "test")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def google_client_ids(self) -> list[str]:
        ids = [self.google_client_id] + self.google_extra_client_ids.split(",")
        return [i.strip() for i in ids if i.strip()]

    @property
    def payments_mock(self) -> bool:
        return self.payment_gateway == "mock" or not (self.razorpay_key_id and self.razorpay_key_secret)


@lru_cache
def get_settings() -> Settings:
    return Settings()
