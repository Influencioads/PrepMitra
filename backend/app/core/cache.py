"""Redis access with an in-memory fallback.

Redis is used for: the background job queue, rate limiting and short-lived caches (catalog).
Without REDIS_URL everything still works in a single API process (development, tests); production runs
several API instances and must set REDIS_URL.
"""

import json
import logging
import threading
import time
from functools import lru_cache
from typing import Any

from app.config import get_settings

log = logging.getLogger(__name__)


class MemoryRedis:
    """The small subset of redis-py used by this app, kept in process memory."""

    def __init__(self):
        self._data: dict[str, tuple[Any, float | None]] = {}
        self._lock = threading.Lock()

    def _get(self, key):
        item = self._data.get(key)
        if item is None:
            return None
        value, exp = item
        if exp is not None and exp < time.time():
            self._data.pop(key, None)
            return None
        return value

    def get(self, key):
        with self._lock:
            return self._get(key)

    def set(self, key, value, ex: int | None = None, nx: bool = False):
        with self._lock:
            if nx and self._get(key) is not None:
                return None
            self._data[key] = (value, time.time() + ex if ex else None)
            return True

    def delete(self, *keys):
        with self._lock:
            for k in keys:
                self._data.pop(k, None)

    def incr(self, key):
        with self._lock:
            cur = self._get(key) or 0
            exp = self._data.get(key, (None, None))[1]
            self._data[key] = (int(cur) + 1, exp)
            return int(cur) + 1

    def expire(self, key, seconds):
        with self._lock:
            if key in self._data:
                self._data[key] = (self._data[key][0], time.time() + seconds)

    def ttl(self, key):
        with self._lock:
            item = self._data.get(key)
            if not item or item[1] is None:
                return -1
            return max(0, int(item[1] - time.time()))

    def scan_iter(self, match: str):
        prefix = match.rstrip("*")
        with self._lock:
            return [k for k in list(self._data) if k.startswith(prefix)]

    def flushall(self):
        with self._lock:
            self._data.clear()


@lru_cache
def get_redis():
    url = get_settings().redis_url
    if not url:
        return MemoryRedis()
    import redis

    return redis.Redis.from_url(url, decode_responses=True, socket_timeout=5)


def cache_get_json(key: str):
    try:
        raw = get_redis().get(key)
    except Exception:  # cache must never break a request
        log.warning("cache read failed for %s", key)
        return None
    return json.loads(raw) if raw else None


def cache_set_json(key: str, value, ttl: int) -> None:
    try:
        get_redis().set(key, json.dumps(value, default=str), ex=ttl)
    except Exception:
        log.warning("cache write failed for %s", key)


def cache_delete_prefix(prefix: str) -> None:
    try:
        r = get_redis()
        keys = list(r.scan_iter(match=f"{prefix}*"))
        if keys:
            r.delete(*keys)
    except Exception:
        log.warning("cache invalidation failed for %s", prefix)
