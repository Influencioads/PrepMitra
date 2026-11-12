"""Checks the OpenRouter key and every model in the routing table with one tiny call each.

    cd backend && .venv/Scripts/python scripts/openrouter_smoke.py            # every model alias, ~Rs 1 in total
    cd backend && .venv/Scripts/python scripts/openrouter_smoke.py deepseek   # only the listed aliases

Reads OPENROUTER_API_KEY from backend/.env. Prints, per model: OK/FAIL, the model that answered, latency and cost.
Sends no student data. Writes nothing to the database.
"""

import json
import os
import sys
import time
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
os.chdir(BACKEND)
os.environ["AI_PROVIDER"] = "openrouter"

import httpx  # noqa: E402

from app.ai import catalog  # noqa: E402
from app.ai.provider import OpenRouterProvider  # noqa: E402

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["answer"],
          "properties": {"answer": {"type": "string"}}}


def main(aliases: list[str]) -> int:
    p = OpenRouterProvider()
    key = p.client.get("https://openrouter.ai/api/v1/key", timeout=20)
    if key.status_code != 200:
        print(f"Key check failed: HTTP {key.status_code} {key.text[:200]}")
        return 1
    info = key.json().get("data", {})
    print(f"Key OK. Limit: {info.get('limit')}  used: ${info.get('usage', 0):.4f}\n")
    route = catalog.Route("smoke", "deepseek", max_tokens=300, timeout=60)
    failed = 0
    for alias in aliases or ["ultra", *catalog.MODELS]:
        m = catalog.model(alias)
        body = p.build_body([m], route, "Reply with JSON only.", "What is 12 x 12? Put only the number in answer.",
                            SCHEMA, "smoke")
        started = time.monotonic()
        try:
            r = p.client.post(p.URL, json=body, timeout=route.timeout)
            data = r.json()
        except (httpx.HTTPError, ValueError) as e:
            data, r = {"error": {"message": type(e).__name__}}, None
        ms = int((time.monotonic() - started) * 1000)
        if r is None or r.status_code != 200 or data.get("error"):
            failed += 1
            print(f"FAIL {alias:14s} {m.id:36s} {str((data.get('error') or {}).get('message', ''))[:90]}")
            continue
        content = (data["choices"][0]["message"].get("content") or "").strip()
        usd = (data.get("usage") or {}).get("cost") or 0
        try:
            ok = json.loads(content.strip("`").removeprefix("json")).get("answer", "").strip() == "144"
        except (ValueError, AttributeError):
            ok = False
        failed += not ok
        print(f"{'OK  ' if ok else 'BAD '} {alias:14s} {data.get('model', m.id):36s} {ms:6d} ms  "
              f"Rs {usd * catalog.USD_TO_INR:.4f}  {content[:40]!r}")
    print(f"\n{failed} problem(s).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
