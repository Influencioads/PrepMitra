"""LLM provider abstraction (PDF section 6): swap or mix models without touching business logic.

- `OpenRouterProvider` (AI_PROVIDER=openrouter) routes every call through OpenRouter using the feature routing map
  in `app/ai/catalog.py`: cheap Tier 2/3 models first, automatic fallbacks, and a premium (Tier 1) model only when
  the caller asks for escalation.
- `ClaudeProvider` calls the Anthropic Messages API with strict JSON output. "strong" tier = question generation,
  reports, interviews; "fast" tier = verification solves, translation checks and other simple tasks.
- `MockProvider` is deterministic and free. It is used by the automated tests and for local demos without an API
  key (AI_PROVIDER=mock). Its questions are simple arithmetic so the independent-solve and numeric checks are real.

Every call is logged to `ai_usage` for cost-per-attempt tracking.
"""

import json
import logging
import random
import re
import time
from functools import lru_cache

from app.config import get_settings

log = logging.getLogger(__name__)


class AIError(Exception):
    """The model call failed or returned unusable output. Callers decide whether to retry, skip or fail the job."""


# The one price list for every cost figure (logs, bank builder, dashboard) lives in the model catalog.
from app.ai import catalog  # noqa: E402
from app.ai.catalog import USD_TO_INR, cost_usd  # noqa: E402,F401  (re-exported for existing importers)


def _record_usage(purpose: str, model: str, input_tokens: int, output_tokens: int, ref_id, latency_ms: int,
                  db=None, *, cached_tokens: int = 0, usd: float | None = None, feature: str | None = None) -> None:
    """Adds the usage row to the caller's session when given (committed with its work), else writes it directly.

    `usd` is the provider-reported cost when available (OpenRouter returns it); otherwise it is computed from the
    catalog prices. Logged on every call so cost per student and per feature can be tracked (playbook rule 11)."""
    from app.db import SessionLocal
    from app.models import AiUsage

    if usd is None:
        usd = cost_usd(model, input_tokens, output_tokens, cached_tokens)
    log.info("ai call %s model=%s tokens=%d in (%d cached) / %d out cost=$%.5f (Rs %.3f) latency=%dms", purpose,
             model, input_tokens, cached_tokens, output_tokens, usd, usd * USD_TO_INR, latency_ms)
    row = dict(purpose=purpose, model=model[:60], input_tokens=input_tokens, output_tokens=output_tokens,
               ref_id=str(ref_id) if ref_id else None, latency_ms=latency_ms, cached_tokens=cached_tokens or 0,
               cost_usd=round(float(usd), 6), feature=feature)
    if db is not None:
        db.add(AiUsage(**row))
        return
    try:
        with SessionLocal() as db:
            db.add(AiUsage(**row))
            db.commit()
    except Exception:  # usage logging must never fail the AI call
        log.warning("could not record AI usage for %s", purpose)


class ClaudeProvider:
    name = "claude"

    def __init__(self):
        import anthropic

        s = get_settings()
        self._anthropic = anthropic
        # Explicit key when configured; otherwise the SDK resolves credentials from the environment/profile.
        kwargs = {"timeout": s.ai_timeout_seconds, "max_retries": 2}
        if s.anthropic_api_key:
            kwargs["api_key"] = s.anthropic_api_key
        self.client = anthropic.Anthropic(**kwargs)
        self.models = {"strong": s.ai_model_strong, "fast": s.ai_model_fast}

    def generate_json(self, *, purpose: str, system: str, prompt: str, schema: dict, tier: str = "strong",
                      effort: str | None = None, ref_id=None, context: dict | None = None, db=None,
                      premium: bool = False, language: str | None = None, images: list[str] | None = None) -> dict:
        if images:
            raise AIError("photo questions need AI_PROVIDER=openrouter")
        a = self._anthropic
        model = self.models[tier]
        output_config = {"format": {"type": "json_schema", "schema": schema},
                         "effort": effort or ("medium" if tier == "strong" else "low")}
        started = time.monotonic()
        try:
            # Server-side refusal fallback is enabled by default: on a policy decline the API re-runs the request
            # on a fallback model inside the same call.
            resp = self.client.beta.messages.create(
                model=model, max_tokens=16000, system=system,
                messages=[{"role": "user", "content": prompt}],
                output_config=output_config,
                betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            )
        except a.RateLimitError as e:
            raise AIError(f"rate limited: {e.message}") from e
        except a.APIStatusError as e:
            raise AIError(f"API error {e.status_code}: {e.message}") from e
        except a.APIConnectionError as e:
            raise AIError("network error calling the AI provider") from e
        latency = int((time.monotonic() - started) * 1000)
        _record_usage(purpose, resp.model, resp.usage.input_tokens, resp.usage.output_tokens, ref_id, latency, db)

        if resp.stop_reason == "refusal":
            raise AIError("the model declined this request")
        if resp.stop_reason == "max_tokens":
            raise AIError("the model output was cut off")
        text = "".join(b.text for b in resp.content if b.type == "text")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise AIError("the model returned invalid JSON") from e


_STRICT_UNSUPPORTED = ("maxItems", "minItems", "maxLength", "minLength", "pattern", "format")


def _strict_schema(schema):
    """Drops keywords some providers reject in strict JSON-schema mode. Code re-validates every result anyway."""
    if isinstance(schema, dict):
        return {k: _strict_schema(v) for k, v in schema.items() if k not in _STRICT_UNSUPPORTED}
    if isinstance(schema, list):
        return [_strict_schema(v) for v in schema]
    return schema


def _parse_json(text: str) -> dict:
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    return json.loads(text)


class OpenRouterProvider:
    """One OpenRouter key for every model. Each call's model list comes from its feature route,
    [premium?] + primary + fallbacks, sent as OpenRouter's `models` array, so an outage on one model moves to the
    next inside the same request. One retry on top of that, then AIError (callers already handle it).

    Only anonymised study data is sent: prompts never carry names, phones or emails, and OpenRouter is told to use
    only providers that do not store or train on prompts (`data_collection: deny`)."""

    name = "openrouter"
    URL = "https://openrouter.ai/api/v1/chat/completions"
    # Requests that will fail the same way again: bad request, bad key, out of credit, forbidden.
    NO_RETRY = (400, 401, 402, 403)

    def __init__(self):
        import httpx

        s = get_settings()
        if not s.openrouter_api_key:
            raise RuntimeError("AI_PROVIDER=openrouter needs OPENROUTER_API_KEY")
        self._httpx = httpx
        self.client = httpx.Client(headers={
            "Authorization": f"Bearer {s.openrouter_api_key}",
            "HTTP-Referer": s.public_base_url, "X-Title": s.app_name,
        })

    @staticmethod
    def build_body(models: list, route, system: str, prompt: str, schema: dict, name: str,
                   images: list[str] | None = None) -> dict:
        user_content = prompt
        if images:  # data: URLs or https URLs (photo doubts)
            user_content = [{"type": "text", "text": prompt}] + [
                {"type": "image_url", "image_url": {"url": u}} for u in images]
        body = {
            "models": [m.id for m in models],
            "messages": [
                # cache_control lets Anthropic/Gemini cache the fixed system prompt (playbook rule 1); others ignore it.
                {"role": "system", "content": [{"type": "text", "text": system,
                                                "cache_control": {"type": "ephemeral"}}]},
                {"role": "user", "content": user_content},
            ],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": re.sub(r"[^a-zA-Z0-9_-]", "_", name)[:60], "strict": True, "schema": _strict_schema(schema)}},
            "max_tokens": route.max_tokens,
            "provider": {"require_parameters": True, "data_collection": "deny"},
            "usage": {"include": True},
        }
        if route.web_search:
            body["plugins"] = [{"id": "web", "max_results": 8}]
        if route.reasoning:  # thinking only where needed (maths solves, question checks)
            body["reasoning"] = {"effort": "medium", "exclude": True}
            body["max_tokens"] = route.max_tokens + 8000
        return body

    def generate_json(self, *, purpose: str, system: str, prompt: str, schema: dict, tier: str = "strong",
                      effort: str | None = None, ref_id=None, context: dict | None = None, db=None,
                      premium: bool = False, language: str | None = None, images: list[str] | None = None) -> dict:
        route = catalog.route_for(purpose)
        models = catalog.model_chain(route, premium=premium, language=language)
        if images:
            models = [m for m in models if m.vision] or models
        body = self.build_body(models, route, system, prompt, schema, purpose, images)
        last_err = "no attempt"
        for _ in range(2):
            started = time.monotonic()
            try:
                resp = self.client.post(self.URL, json=body, timeout=route.timeout)
            except self._httpx.HTTPError as e:
                last_err = f"network error calling OpenRouter: {type(e).__name__}"
                continue
            latency = int((time.monotonic() - started) * 1000)
            try:
                data = resp.json()
            except ValueError:
                data = {}
            if resp.status_code != 200 or data.get("error"):
                err = data.get("error") or {}
                last_err = f"OpenRouter error {err.get('code', resp.status_code)}: {str(err.get('message', ''))[:200]}"
                if resp.status_code in self.NO_RETRY:
                    break
                continue
            usage = data.get("usage") or {}
            cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
            _record_usage(purpose, data.get("model") or models[0].id, usage.get("prompt_tokens", 0),
                          usage.get("completion_tokens", 0), ref_id, latency, db, cached_tokens=cached,
                          usd=usage.get("cost"), feature=route.feature)
            choice = (data.get("choices") or [{}])[0]
            if choice.get("error"):
                last_err = f"model error: {str((choice['error'] or {}).get('message', ''))[:200]}"
                continue
            finish = choice.get("finish_reason")
            if finish == "length":
                raise AIError("the model output was cut off")
            if finish in ("content_filter", "refusal"):
                raise AIError("the model declined this request")
            content = (choice.get("message") or {}).get("content") or ""
            if isinstance(content, list):
                content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
            try:
                return _parse_json(content)
            except json.JSONDecodeError:
                last_err = "the model returned invalid JSON"
        raise AIError(last_err)



def synthesize(schema: dict, key: str = "value"):
    """A deterministic value that satisfies `schema` (mock AI for features without a hand-written handler)."""
    t = schema.get("type")
    if "enum" in schema:
        return schema["enum"][0]
    if t == "object":
        return {k: synthesize(v, k) for k, v in schema.get("properties", {}).items()}
    if t == "array":
        n = max(1, min(schema.get("minItems", 1), schema.get("maxItems", 1)))
        return [synthesize(schema.get("items", {"type": "string"}), key) for _ in range(n)]
    if t == "integer":
        return max(schema.get("minimum", 1), 1)
    if t == "number":
        return float(max(schema.get("minimum", 1), 1))
    if t == "boolean":
        return key in ("on_topic", "verified", "works", "is_correct")
    if key == "answer":
        return "A"
    return f"Mock {key.replace('_', ' ')}"


class MockProvider:
    """Deterministic stand-in for the LLM. `force(purpose, payload)` queues a canned response (tests)."""

    name = "mock"
    _forced: dict[str, list] = {}

    @classmethod
    def force(cls, purpose: str, payload) -> None:
        cls._forced.setdefault(purpose, []).append(payload)

    @classmethod
    def reset(cls) -> None:
        cls._forced.clear()

    def generate_json(self, *, purpose: str, system: str, prompt: str, schema: dict, tier: str = "strong",
                      effort: str | None = None, ref_id=None, context: dict | None = None, db=None,
                      premium: bool = False, language: str | None = None, images: list[str] | None = None) -> dict:
        _record_usage(purpose, f"mock-{tier}", len(prompt) // 4, 200, ref_id, 1, db)
        queued = self._forced.get(purpose)
        if queued:
            item = queued.pop(0)
            if isinstance(item, Exception):
                raise item
            return item
        handler = getattr(self, f"_m_{purpose}", None)
        if handler is None:
            # Blueprint features get a schema-valid placeholder; older call sites keep failing over to their
            # code-written fallback, as they always have under the mock.
            if purpose in catalog.PURPOSE_TO_FEATURE:
                raise AIError(f"mock provider has no handler for {purpose}")
            return synthesize(schema, purpose)
        return handler(context or {}, prompt)

    # ---- question pipeline -------------------------------------------------------------------------------------
    _NOUNS = ["pens", "books", "mangoes", "tickets", "chairs", "bulbs", "kites", "bags", "shirts", "lamps", "cups",
              "boxes", "files", "bottles", "plates", "clocks", "candles", "baskets", "ropes", "tiles"]
    _PLACES = ["Pune", "Madurai", "Kochi", "Patna", "Indore", "Surat", "Mysuru", "Guwahati", "Nagpur", "Ranchi",
               "Bhopal", "Agra", "Jaipur", "Vellore", "Udaipur", "Shillong", "Nashik", "Rajkot", "Kota", "Hubli"]

    def _m_question_generate(self, ctx: dict, prompt: str) -> dict:
        rng = random.Random(ctx.get("seed", 0))
        qtype, topic = ctx.get("qtype", "single"), ctx.get("topic", "Arithmetic")
        diff = ctx.get("difficulty", "medium")
        a, b = rng.randint(12, 99), rng.randint(3, 49)
        noun, place = rng.choice(self._NOUNS), rng.choice(self._PLACES)
        lead = f"[{topic}] A trader in {place} packs {noun} in lots."
        if qtype == "multi":
            k = rng.choice([3, 4, 5, 6, 7])
            pool = set()
            while len(pool) < 4:
                pool.add(rng.randint(20, 400))
            nums = sorted(pool)
            divisible = [n for n in nums if n % k == 0]
            if not divisible:  # guarantee at least one correct option
                nums[0] = k * rng.randint(5, 40)
                nums = sorted(set(nums))
                while len(nums) < 4:
                    nums.append(nums[-1] + 1)
            options = [{"key": "ABCD"[i], "text": str(n)} for i, n in enumerate(nums)]
            answer = ",".join(o["key"] for o in options if int(o["text"]) % k == 0)
            return {
                "text": f"{lead} Which of the following lot sizes are exactly divisible by {k}?",
                "options": options, "answer": answer,
                "explanation": f"Divide each number by {k} and keep those with remainder 0.",
                "shortcut": f"Use the divisibility rule for {k} instead of long division.",
                "subtopic": "Divisibility", "difficulty": diff, "expected_time_sec": 60, "numeric_check": "",
            }
        result = a * b
        text = f"{lead} Compute {a} × {b} to find the total number of {noun}."
        if qtype == "numeric":
            return {"text": text, "options": [], "answer": str(result),
                    "explanation": f"{a} × {b} = {result}.",
                    "shortcut": "Split the multiplier: a × b = a × (b − r) + a × r.",
                    "subtopic": "Multiplication", "difficulty": diff, "expected_time_sec": 45,
                    "numeric_check": f"{a}*{b}"}
        distractors = {result + a, result - b, result + 10, result - 10}
        distractors.discard(result)
        values = [result] + sorted(distractors)[:3]
        rng.shuffle(values)
        options = [{"key": "ABCD"[i], "text": str(v)} for i, v in enumerate(values)]
        answer = next(o["key"] for o in options if o["text"] == str(result))
        return {"text": text, "options": options, "answer": answer,
                "explanation": f"{a} × {b} = {result}.",
                "shortcut": "Check the unit digit first: it eliminates most options instantly.",
                "subtopic": "Multiplication", "difficulty": diff, "expected_time_sec": 45,
                "numeric_check": f"{a}*{b}"}

    def _m_question_verify(self, ctx: dict, prompt: str) -> dict:
        """Solves the question from its text alone (never sees the generator's answer)."""
        q = ctx.get("question", {})
        text, options = q.get("text", ""), q.get("options", [])
        m = re.search(r"Compute (\d+) × (\d+)", text)
        if m:
            value = int(m.group(1)) * int(m.group(2))
            if not options:
                return {"answer": str(value), "working": "multiplied"}
            key = next((o["key"] for o in options if o["text"] == str(value)), "")
            return {"answer": key, "working": "multiplied and matched option"}
        m = re.search(r"divisible by (\d+)", text)
        if m:
            k = int(m.group(1))
            keys = [o["key"] for o in options if o["text"].isdigit() and int(o["text"]) % k == 0]
            return {"answer": ",".join(keys), "working": "checked remainders"}
        return {"answer": "", "working": "could not solve"}

    def _m_translate(self, ctx: dict, prompt: str) -> dict:
        lang, q = ctx.get("language", "xx"), ctx.get("question", {})
        tag = f"[{lang}] "
        return {"text": tag + q.get("text", ""),
                "options": [{"key": o["key"], "text": o["text"]} for o in q.get("options", [])],
                "explanation": tag + q.get("explanation", ""), "shortcut": tag + q.get("shortcut", "")}

    def _m_back_translate(self, ctx: dict, prompt: str) -> dict:
        return {"text": re.sub(r"^\[[a-z]+\] ", "", ctx.get("text", ""))}

    def _m_lesson(self, ctx: dict, prompt: str) -> dict:
        return {"lesson": f"When writing {ctx.get('topic', 'this topic')} questions: {ctx.get('resolution', 'double-check the answer key')}."[:300]}

    # ---- reports -------------------------------------------------------------------------------------------------
    def _m_exam_report(self, ctx: dict, prompt: str) -> dict:
        a = ctx.get("analytics", {})
        topics = a.get("topics", [])
        strong = [t for t in topics if t["accuracy"] is not None and t["accuracy"] >= 0.7]
        weak = [t for t in topics if t["wrong_refs"]]
        wrong = [r for t in topics for r in t["wrong_refs"]]
        return {
            "summary": f"You scored {a.get('score')} out of {a.get('max_score')} with {round((a.get('accuracy') or 0) * 100)}% accuracy.",
            "strengths": [{"topic": t["name"], "detail": "Fast and accurate here."} for t in strong[:3]],
            "weaknesses": [{"topic": t["name"], "detail": "Accuracy is low on this topic.", "question_refs": t["wrong_refs"][:5]}
                           for t in weak[:4]],
            "loopholes": [{"pattern": p["type"], "detail": p["description"], "question_refs": p["question_refs"][:5]}
                          for p in a.get("error_patterns", [])],
            "shortcuts": [{"question_ref": r, "technique": "Option elimination",
                           "explanation": "Check the unit digit of each option before calculating fully."} for r in wrong[:5]],
            "study_plan": [{"day": d, "focus": (weak[(d - 1) % len(weak)]["name"] if weak else "Mixed practice"),
                            "tasks": ["Revise the concept", "Solve 20 timed questions"]} for d in range(1, 8)],
            "next_test": {"exam_slug": ctx.get("exam_slug", ""), "reason": "Retake the same pattern to confirm improvement."},
            "encouragement": "Steady practice on weak topics will move your score quickly.",
            "since_last_attempt": "" if not a.get("since_last_attempt") else (
                f"Your score changed by {a['since_last_attempt']['score_change']} since your last attempt."),
        }

    # ---- interviews ----------------------------------------------------------------------------------------------
    def _m_interview_next(self, ctx: dict, prompt: str) -> dict:
        stage, n, role = ctx.get("stage", "introduction"), ctx.get("question_no", 1), ctx.get("role", "this role")
        if ctx.get("must_follow_up") and ctx.get("last_answer"):
            snippet = " ".join(ctx["last_answer"].split()[:6])
            return {"question": f"You mentioned \"{snippet}\". Can you walk me through a specific example of that?",
                    "is_followup": True, "refers_to": snippet}
        bank = {
            "introduction": "Please introduce yourself and tell me why you are interested in this role.",
            "resume": "Tell me about the most significant project or responsibility on your resume.",
            "role_technical": f"What are the core skills a {role} needs, and how have you used them?",
            "situational": "Describe a time you handled a difficult deadline. Use the STAR format.",
            "hr": "Where do you see yourself in three years, and what are your salary expectations?",
            "closing": "Do you have any questions for us before we close?",
        }
        return {"question": f"Q{n}: {bank.get(stage, bank['role_technical'])}", "is_followup": False, "refers_to": ""}

    def _m_interview_report(self, ctx: dict, prompt: str) -> dict:
        answers = ctx.get("answers", [])
        criteria = ctx.get("criteria", [])
        avg_words = sum(len(a["text"].split()) for a in answers) / max(1, len(answers))
        base = 4 + min(5, int(avg_words // 15))
        return {
            "summary": f"You answered {len(answers)} questions. Longer, structured answers scored better.",
            "scores": [{"criterion": c, "score": base, "justification": "Based on answer depth and structure."} for c in criteria],
            "per_question": [{"turn_ref": a["ref"], "good": "Clear and on topic.", "missing": "A concrete, measurable example.",
                              "model_answer": "Situation, task, action and a measurable result from your own experience."}
                             for a in answers],
            "red_flags": ["Very short answers"] if avg_words < 8 else [],
            "study_plan": [{"day": d, "focus": "STAR answers", "tasks": ["Record two answers and review them"]} for d in range(1, 8)],
        }


@lru_cache
def get_provider():
    name = get_settings().ai_provider
    if name == "mock":
        return MockProvider()
    if name == "openrouter":
        return OpenRouterProvider()
    return ClaudeProvider()
