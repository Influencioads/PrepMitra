"""Fixed-window rate limits backed by Redis (in-memory fallback in single-process dev)."""

from fastapi import Request

from app.config import get_settings
from app.core.cache import get_redis
from app.core.errors import AppError


def hit(key: str, limit: int, window_sec: int) -> None:
    if not get_settings().rate_limits_enabled:
        return
    r = get_redis()
    full = f"rl:{key}"
    try:
        n = r.incr(full)
        if n == 1:
            r.expire(full, window_sec)
    except Exception:  # fail open: a Redis outage must not take the API down
        return
    if n > limit:
        raise AppError(429, "rate_limited", "Too many requests. Please slow down and try again shortly.")


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def limit(name: str, per_minute: int):
    """FastAPI dependency: per-IP limit for an endpoint group."""

    def _dep(request: Request) -> None:
        hit(f"{name}:{client_ip(request)}", per_minute, 60)

    return _dep
