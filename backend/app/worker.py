"""Background worker: `python -m app.worker` (needs REDIS_URL and JOB_MODE=redis on the API side).

Consumes the Redis job queue (reports, interview evaluation, notifications, paper generation) and runs the periodic
scheduler. Run several workers for throughput; periodic tasks are de-duplicated with Redis locks.
"""

import json
import logging
import signal

from app.config import get_settings
from app.core.cache import get_redis
from app.jobs.queue import QUEUE_KEY, run_task
from app.jobs.scheduler import Scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("worker")


def main() -> None:
    if not get_settings().redis_url:
        raise SystemExit("REDIS_URL is required for the worker (without Redis, jobs run inside the API process)")
    r = get_redis()
    scheduler = Scheduler()
    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    log.info("worker started")
    while running:
        scheduler.tick()
        # Must stay below the client's socket_timeout (5s), or an idle queue raises TimeoutError.
        item = r.blpop([QUEUE_KEY], timeout=2)
        if item is None:
            continue
        job = json.loads(item[1])
        run_task(job["name"], job.get("kwargs", {}))
    log.info("worker stopped")


if __name__ == "__main__":
    main()
