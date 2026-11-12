"""Blueprint model routing (OpenRouter), per-call cost logging, plan entitlements and monthly AI allowances."""

import json

import httpx
import pytest
from sqlalchemy import select

from app.ai import catalog
from app.ai.provider import AIError, OpenRouterProvider
from app.core.errors import AppError
from app.models import AiUsage, User
from app.services import allowances
from app.services.plan_catalog import PLANS


# ---- catalog and routing ------------------------------------------------------------------------------------------
def test_every_route_uses_known_models_and_every_call_site_has_a_route():
    for r in catalog.ROUTES.values():
        for alias in (r.primary, *r.fallbacks, r.premium, r.indic_primary):
            if alias:
                assert alias in catalog.MODELS or alias == "ultra", (r.feature, alias)
        assert r.fallbacks, f"{r.feature} needs a fallback for outages"
    for purpose in catalog.PURPOSE_TO_FEATURE:
        assert catalog.route_for(purpose)


def test_routing_follows_the_blueprint():
    chain = lambda f, **kw: [m.alias for m in catalog.model_chain(catalog.ROUTES[f], **kw)]  # noqa: E731
    assert chain("mock_report") == ["deepseek", "gemini_flash"]
    assert chain("tutor_chat") == ["deepseek", "haiku"]
    assert chain("tutor_chat", premium=True) == ["sonnet", "deepseek", "haiku"]  # escalation, cheap route behind it
    assert chain("tutor_chat", language="hi") == ["gemini_flash", "deepseek", "haiku"]  # Indian-language chat
    assert chain("mock_report", premium=True) == ["deepseek", "gemini_flash"]  # no premium route: never escalates
    assert chain("ultra") == ["fable", "opus", "sonnet"]
    # The question checker is never the same model as the writer.
    assert catalog.ROUTES["question_bank_write"].primary != catalog.ROUTES["question_bank_verify"].primary
    # ~85% of calls on cheap models: only Tier 1 features have a premium primary.
    tier1 = {f for f, r in catalog.ROUTES.items() if catalog.model(r.primary).tier <= 1}
    assert tier1 == {"deep_persona", "tutor_master", "notes_master", "interview_scoring", "topic_deck_master",
                     "ultra", "question_bank_write"}


def test_model_overrides(monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "ai_model_overrides", "ultra=openai/gpt-6-astra,glm=z-ai/glm-9")
    assert catalog.model("ultra").id == "openai/gpt-6-astra" and catalog.model("ultra").usd_out == 50.0
    assert catalog.model("glm").id == "z-ai/glm-9" and catalog.model("glm").tier == 2
    monkeypatch.setattr(get_settings(), "ai_model_overrides", "")
    monkeypatch.setattr(get_settings(), "ai_ultra_model", "gemini_carbon")
    assert catalog.model("ultra").id == "google/gemini-4-carbon"


def test_cost_in_rupees_matches_blueprint_planning_numbers():
    # Mock report: DeepSeek V3.2, 6,000 in / 2,000 out ~ Rs 0.21 before the 1.5x planning buffer (blueprint Rs 0.22).
    inr = catalog.cost_usd("deepseek/deepseek-v3.2", 6000, 2000) * catalog.USD_TO_INR
    assert 0.1 < inr < 0.25
    # Cached input is billed at the cache rate.
    assert catalog.cost_usd("anthropic/claude-sonnet-5.5", 1_000_000, 0, 1_000_000) == pytest.approx(0.10)
    assert catalog.cost_usd("claude-sonnet-5-5-20261001", 1_000_000, 1_000_000) == pytest.approx(12.0)  # direct API id
    assert catalog.cost_usd("unknown/model", 1000, 1000) == 0.0


# ---- OpenRouter provider (fake transport: no network) -------------------------------------------------------------
def _provider(monkeypatch, handler) -> OpenRouterProvider:
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "openrouter_api_key", "sk-or-test")
    p = OpenRouterProvider()
    p.client = httpx.Client(transport=httpx.MockTransport(handler), headers=p.client.headers)
    return p


def _ok(content: dict, model="deepseek/deepseek-v3.2", cost=0.0021):
    return httpx.Response(200, json={
        "model": model, "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(content)}}],
        "usage": {"prompt_tokens": 6000, "completion_tokens": 2000, "cost": cost,
                  "prompt_tokens_details": {"cached_tokens": 4000}}})


SCHEMA = {"type": "object", "additionalProperties": False, "required": ["note", "tips"],
          "properties": {"note": {"type": "string"}, "tips": {"type": "array", "items": {"type": "string"},
                                                              "maxItems": 3}}}


def test_openrouter_request_shape_and_usage_logging(monkeypatch, db):
    seen = []

    def handler(req: httpx.Request):
        seen.append(json.loads(req.content))
        assert req.headers["Authorization"] == "Bearer sk-or-test"
        return _ok({"note": "Good work", "tips": []})

    p = _provider(monkeypatch, handler)
    out = p.generate_json(purpose="exam_report", system="SYS", prompt="facts", schema=SCHEMA, ref_id="a1", db=db)
    db.commit()
    assert out == {"note": "Good work", "tips": []}
    body = seen[0]
    assert body["models"] == ["deepseek/deepseek-v3.2", "google/gemini-2.5-flash"]
    assert body["provider"] == {"require_parameters": True, "data_collection": "deny"}
    assert body["response_format"]["json_schema"]["strict"] is True
    assert "maxItems" not in json.dumps(body["response_format"])  # stripped for strict mode
    assert body["max_tokens"] == catalog.ROUTES["mock_report"].max_tokens and "reasoning" not in body
    row = db.scalar(select(AiUsage))
    assert row.feature == "mock_report" and row.cached_tokens == 4000 and row.cost_usd == pytest.approx(0.0021)


def test_openrouter_reasoning_and_premium(monkeypatch, db):
    seen = []
    p = _provider(monkeypatch, lambda req: seen.append(json.loads(req.content)) or _ok({"answer": "B", "working": ""}))
    p.generate_json(purpose="question_verify", system="S", prompt="q", schema=SCHEMA, db=db)
    assert seen[-1]["reasoning"]["effort"] == "medium" and seen[-1]["models"][0] == "deepseek/deepseek-v3.2"
    p.generate_json(purpose="mentor_chat", system="S", prompt="q", schema=SCHEMA, db=db, premium=True)
    assert seen[-1]["models"][0] == "anthropic/claude-sonnet-5.5"


def test_openrouter_retries_once_then_fails_and_never_retries_auth_errors(monkeypatch, db):
    calls = []

    def flaky(req):
        calls.append(1)
        return httpx.Response(502, json={"error": {"code": 502, "message": "upstream down"}}) if len(calls) == 1 \
            else _ok({"note": "ok", "tips": []})

    assert _provider(monkeypatch, flaky).generate_json(
        purpose="lesson", system="S", prompt="p", schema=SCHEMA, db=db)["note"] == "ok"
    assert len(calls) == 2

    calls.clear()

    def no_credit(req):
        calls.append(1)
        return httpx.Response(402, json={"error": {"code": 402, "message": "Insufficient credits"}})

    with pytest.raises(AIError, match="402"):
        _provider(monkeypatch, no_credit).generate_json(purpose="lesson", system="S", prompt="p", schema=SCHEMA, db=db)
    assert len(calls) == 1

    trunc = lambda req: httpx.Response(200, json={"choices": [{"finish_reason": "length", "message": {"content": "{"}}],  # noqa: E731
                                                  "usage": {}})
    with pytest.raises(AIError, match="cut off"):
        _provider(monkeypatch, trunc).generate_json(purpose="lesson", system="S", prompt="p", schema=SCHEMA, db=db)


def test_openrouter_accepts_fenced_json(monkeypatch, db):
    fenced = lambda req: httpx.Response(200, json={  # noqa: E731
        "choices": [{"finish_reason": "stop", "message": {"content": '```json\n{"note": "x", "tips": []}\n```'}}]})
    assert _provider(monkeypatch, fenced).generate_json(
        purpose="lesson", system="S", prompt="p", schema=SCHEMA, db=db)["note"] == "x"


# ---- plans and allowances -----------------------------------------------------------------------------------------
def _buy(client, h, code):
    o = client.post("/v1/orders", headers=h, json={"plan_code": code})
    assert o.status_code == 201, o.text
    client.post(f"/v1/orders/{o.json()['order_id']}/mock-pay", headers=h)
    return o


def test_plan_catalog_matches_blueprint_prices():
    price = {p["code"]: p["price_paise"] // 100 for p in PLANS}
    assert (price["starter_monthly"], price["starter_quarterly"], price["starter_annual"]) == (149, 399, 1199)
    assert (price["pro_monthly"], price["pro_quarterly"], price["pro_annual"]) == (299, 799, 2499)
    assert (price["tutor_lite_monthly"], price["tutor_lite_annual"]) == (99, 999)
    assert (price["tutor_pro_monthly"], price["tutor_pro_annual"]) == (299, 2999)
    assert (price["combo_monthly"], price["combo_annual"]) == (499, 4999)
    assert (price["single_mock"], price["extra_mocks_5"], price["extra_doubts_50"], price["extra_master_10"],
            price["interview_pack"]) == (29, 49, 39, 99, 199)


def test_free_allowance_then_hard_limit(client, catalog_seeded, user_headers, db):
    a = client.get("/v1/me/allowances", headers=user_headers).json()
    assert a["plans"] == [] and a["limits"]["doubts"]["limit"] == 5 and a["flags"]["persona"] == "snapshot"
    assert a["limits"]["tutor_chat_turns"]["limit"] == 0
    user = db.scalar(select(User))
    for i in range(5):
        assert allowances.use(db, user, "doubts", ref_id=f"d{i}")["source"] == "free"
    with pytest.raises(AppError) as e:
        allowances.use(db, user, "doubts")
    assert e.value.status_code == 402
    # A failed AI call gives the unit back.
    assert allowances.refund_use(db, user, "doubts", "d4") == 1
    assert allowances.use(db, user, "doubts")["source"] == "free"


def test_pro_monthly_allowances_and_premium_soft_landing(client, catalog_seeded, user_headers, db):
    _buy(client, user_headers, "pro_monthly")
    a = client.get("/v1/me/allowances", headers=user_headers).json()
    assert a["plans"] == ["pro_monthly"] and a["flags"]["deep_persona"] and a["flags"]["persona"] == "full"
    assert a["limits"]["doubts"]["limit"] == 155  # 150 this month + 5 free for life
    assert a["limits"]["premium_doubts"]["limit"] == 50
    user = db.scalar(select(User))
    for _ in range(50):
        assert allowances.use(db, user, "doubts", want_premium=True) == {"premium": True, "source": "plan"}
    # Premium allowance used up: the doubt still runs, on the Tier 2 route.
    assert allowances.use(db, user, "doubts", want_premium=True) == {"premium": False, "source": "plan"}
    db.commit()
    a = client.get("/v1/me/allowances", headers=user_headers).json()
    assert a["limits"]["doubts"]["used"] == 51 and a["limits"]["premium_doubts"]["remaining"] == 0


def test_study_plan_and_tutor_pack_together_but_not_two_study_plans(client, catalog_seeded, user_headers):
    _buy(client, user_headers, "starter_monthly")
    _buy(client, user_headers, "tutor_lite_monthly")
    assert client.post("/v1/orders", headers=user_headers, json={"plan_code": "pro_monthly"}).status_code == 409
    assert client.post("/v1/orders", headers=user_headers, json={"plan_code": "combo_monthly"}).status_code == 409
    a = client.get("/v1/me/allowances", headers=user_headers).json()
    assert set(a["plans"]) == {"starter_monthly", "tutor_lite_monthly"}
    assert a["limits"]["tutor_chat_turns"]["limit"] == 150 and a["limits"]["cheat_code_sessions"]["limit"] == 6
    assert client.get("/v1/me/credits", headers=user_headers).json()["total"] == 10  # Starter's 10 full mocks


def test_addon_pool_is_used_after_the_monthly_plan(client, catalog_seeded, user_headers, db):
    _buy(client, user_headers, "tutor_pro_monthly")
    _buy(client, user_headers, "extra_master_10")
    user = db.scalar(select(User))
    sources = [allowances.use(db, user, "master_credits")["source"] for _ in range(20)]
    assert sources[:10] == ["plan"] * 10 and all(s not in ("plan", "free") for s in sources[10:])
    with pytest.raises(AppError):
        allowances.use(db, user, "master_credits")


def test_admin_ai_cost_dashboard(client, catalog_seeded, ready_user, admin_headers):
    a = client.post("/v1/attempts", headers=ready_user, json={"exam_id": str(catalog_seeded["mini-mock-general-aptitude"])}).json()
    client.post(f"/v1/attempts/{a['id']}/submit", headers=ready_user)
    out = client.get("/v1/admin/ai/costs", headers=admin_headers).json()
    feats = {f["feature"] for f in out["features"]}
    assert "mock_report" in feats and out["usd_to_inr"] == 90.0
    assert any(r["feature"] == "doubt_solve_math" and r["premium"]["alias"] == "sonnet" for r in out["routing"])
