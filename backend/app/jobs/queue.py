"""Background jobs.

JOB_MODE=eager   run the job inline (automated tests)
JOB_MODE=thread  run in an in-process thread pool (single-instance development)
JOB_MODE=redis   push to a Redis list; `python -m app.worker` processes it (production, horizontally scalable)

Jobs must be idempotent: each one re-reads state from the database and exits if the work is already done.
Callers enqueue only after committing, so a job never races its caller's transaction.
"""

import json
import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

from app.config import get_settings

log = logging.getLogger(__name__)

QUEUE_KEY = "prepmitra:jobs"
_TASKS: dict[str, Callable] = {}


def task(name: str):
    def deco(fn):
        _TASKS[name] = fn
        return fn

    return deco


def _registry() -> dict[str, Callable]:
    import app.jobs.tasks  # noqa: F401  (registers tasks on first use)

    return _TASKS


@lru_cache
def _pool() -> ThreadPoolExecutor:
    return ThreadPoolExecutor(max_workers=4, thread_name_prefix="job")


def run_task(name: str, kwargs: dict) -> None:
    fn = _registry().get(name)
    if fn is None:
        log.error("unknown job %s", name)
        return
    try:
        fn(**kwargs)
    except Exception:
        log.exception("job %s failed (%s)", name, kwargs)


def enqueue(name: str, **kwargs) -> None:
    mode = get_settings().job_mode
    kwargs = {k: str(v) if not isinstance(v, (int, float, bool, type(None))) else v for k, v in kwargs.items()}
    if mode == "eager":
        run_task(name, kwargs)
    elif mode == "redis":
        from app.core.cache import get_redis

        get_redis().rpush(QUEUE_KEY, json.dumps({"name": name, "kwargs": kwargs}))
    else:
        _pool().submit(run_task, name, kwargs)
