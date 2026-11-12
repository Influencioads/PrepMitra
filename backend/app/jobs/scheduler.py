"""Periodic task loop. Runs inside the API (dev) or the worker (production).

With Redis, a short lock per task ensures only one instance runs each periodic task at a time even when several
API/worker processes are up.
"""

import logging
import threading
import time

from app.core.cache import get_redis

log = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        from app.jobs.tasks import periodic

        self.tasks = periodic()
        self.last_run = {i: 0.0 for i in range(len(self.tasks))}
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def tick(self) -> None:
        now = time.time()
        for i, (interval, fn) in enumerate(self.tasks):
            if now - self.last_run[i] < interval:
                continue
            self.last_run[i] = now
            name = getattr(fn, "__name__", str(i))
            try:
                if not get_redis().set(f"sched:{name}", "1", ex=max(5, interval - 1), nx=True):
                    continue
            except Exception:
                pass  # no Redis lock available: run anyway (single instance)
            try:
                result = fn()
                if result:
                    log.info("periodic %s -> %s", name, result)
            except Exception:
                log.exception("periodic task %s failed", name)

    def _loop(self) -> None:
        while not self._stop.is_set():
            self.tick()
            self._stop.wait(5)

    def start(self) -> None:
        self._thread = threading.Thread(target=self._loop, name="scheduler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
