"""Load test (15-day plan, Day 15): N users take the free mini mock at the same time.

Each simulated user: OTP login -> consent + profile -> start the mini mock -> 3 batched autosaves -> submit.
Prints p50/p95/max latency per endpoint. Target: save and submit under 300 ms (p95) with 200 users.

    python scripts/loadtest.py --base http://localhost:8000 --users 200

The server must run with APP_ENV=development (OTP returned in the response) and RATE_LIMITS_ENABLED=false (all
users come from one IP). Run it against staging on PostgreSQL; SQLite serialises writes and is not representative.
"""

import argparse
import asyncio
import random
import statistics
import time
from collections import defaultdict

import httpx

timings: dict[str, list[float]] = defaultdict(list)
errors: dict[str, int] = defaultdict(int)


async def call(client: httpx.AsyncClient, name: str, method: str, url: str, **kw) -> httpx.Response:
    t0 = time.perf_counter()
    r = await client.request(method, url, **kw)
    timings[name].append((time.perf_counter() - t0) * 1000)
    if r.status_code >= 400:
        errors[f"{name} {r.status_code}"] += 1
    return r


async def one_user(client: httpx.AsyncClient, i: int, exam_id: str) -> None:
    phone = f"7{random.randint(100000000, 999999999)}"
    otp = (await call(client, "otp_send", "POST", "/v1/auth/otp/send", json={"phone": phone})).json().get("dev_otp")
    tok = (await call(client, "otp_verify", "POST", "/v1/auth/otp/verify", json={"phone": phone, "code": otp})).json()
    h = {"Authorization": f"Bearer {tok['access_token']}"}
    await call(client, "consents", "POST", "/v1/me/consents", headers=h, json={"data_processing": True})
    await call(client, "profile", "PATCH", "/v1/me", headers=h, json={
        "name": f"Load User {i}", "dob": "1999-01-01", "preferred_language": "en", "target_exam_ids": ["ssc-cgl-tier1"]})
    r = await call(client, "attempt_start", "POST", "/v1/attempts", headers=h, json={"exam_id": exam_id})
    if r.status_code >= 400:
        return
    attempt = r.json()
    qs = attempt["questions"]
    for batch in range(3):
        items = [{"question_id": q["question_id"],
                  "answer": q["content"]["options"][0]["key"] if q["type"] == "single" else (["A"] if q["type"] == "multi" else 1),
                  "client_rev": batch + 1, "time_spent_sec": 20 * (batch + 1)} for q in qs[batch * 10:(batch + 1) * 10]]
        await call(client, "autosave", "PUT", f"/v1/attempts/{attempt['id']}/answers", headers=h, json={"answers": items})
        await asyncio.sleep(random.uniform(0.2, 1.0))
    await call(client, "submit", "POST", f"/v1/attempts/{attempt['id']}/submit", headers=h)


async def main(base: str, users: int) -> None:
    async with httpx.AsyncClient(base_url=base, timeout=60) as client:
        exams = (await client.get("/v1/exams", params={"limit": 100})).json()["items"]
        exam_id = next(e["id"] for e in exams if e["is_free_trial"])
        # Warm-up: the first start may assemble a paper; later users reuse the bank.
        t0 = time.perf_counter()
        await asyncio.gather(*(one_user(client, i, exam_id) for i in range(users)))
        wall = time.perf_counter() - t0
    print(f"\n{users} users in {wall:.1f}s\n")
    print(f"{'endpoint':<16}{'calls':>7}{'p50 ms':>10}{'p95 ms':>10}{'max ms':>10}")
    for name, ts in timings.items():
        ts.sort()
        p95 = ts[max(0, int(len(ts) * 0.95) - 1)]
        print(f"{name:<16}{len(ts):>7}{statistics.median(ts):>10.0f}{p95:>10.0f}{ts[-1]:>10.0f}")
    if errors:
        print("\nerrors:", dict(errors))
    slow = [n for n in ("autosave", "submit") if n in timings
            and sorted(timings[n])[max(0, int(len(timings[n]) * 0.95) - 1)] > 300]
    print("\nRESULT:", "FAIL (p95 > 300 ms for " + ", ".join(slow) + ")" if slow else "PASS (autosave and submit p95 <= 300 ms)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:8000")
    ap.add_argument("--users", type=int, default=50)
    a = ap.parse_args()
    asyncio.run(main(a.base, a.users))
