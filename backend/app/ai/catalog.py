"""Model catalog and feature routing ("PrepMitra AI — AI Features, Model Routing & Pricing Blueprint", Nov 2026).

Three tiers plus an optional Ultra tier:

- Tier 1 (premium): only for the hardest ~15% of work: offline question-bank authoring, Master-mode tutoring,
  doubt escalation, the monthly deep persona and interview scoring.
- Tier 2 (strong, cheap): most real thinking: reports, doubts, tutor chat, notes, interviews, planner.
- Tier 3 (general): routing, tagging, persona micro-updates, revision hints, nudges.
- Tier 0 (Ultra): sold only in the Ultra pack, never inside a subscription.

Every model is called through OpenRouter, so one key reaches all providers and a model can be swapped or re-priced
here without an app release. Model IDs and prices are OpenRouter's list as of 2026-11-12 (USD per 1M tokens);
re-check them at https://openrouter.ai/models before launch and monthly after.

Any alias can be pointed at another OpenRouter model with AI_MODEL_OVERRIDES, e.g.
`AI_MODEL_OVERRIDES=ultra=openai/gpt-6-astra,deepseek=deepseek/deepseek-v4-flash`.
"""

from dataclasses import dataclass, field
from functools import lru_cache

from app.config import get_settings

# ₹ per US$: the blueprint's planning rate, slightly above market as a buffer.
USD_TO_INR = 90.0


@dataclass(frozen=True)
class Model:
    alias: str
    id: str  # OpenRouter model id
    tier: int  # 0 = Ultra, 1 = premium, 2 = strong & cheap, 3 = general
    usd_in: float  # per 1M input tokens
    usd_out: float  # per 1M output tokens
    usd_cached_in: float | None = None
    vision: bool = False


MODELS: dict[str, Model] = {m.alias: m for m in [
    # Tier 0 · Ultra (Ultra pack only). All four models the blueprint named are now listed on OpenRouter.
    Model("fable", "anthropic/claude-fable-5.2", 0, 8.00, 40.00, 0.20, True),
    Model("gemini_carbon", "google/gemini-4-carbon", 0, 2.00, 10.00, 0.10, True),
    Model("gemini_argon", "google/gemini-4-argon", 0, 2.00, 10.00, 0.10, True),
    Model("gpt_astra", "openai/gpt-6-astra", 0, 10.00, 50.00, 1.00, True),
    # Tier 1 · Premium
    Model("opus", "anthropic/claude-opus-5.5", 1, 4.00, 20.00, 0.20, True),
    Model("sonnet", "anthropic/claude-sonnet-5.5", 1, 2.00, 10.00, 0.10, True),
    Model("gpt5", "openai/gpt-5", 1, 1.25, 10.00, 0.125, True),
    Model("gemini_pro", "google/gemini-3.1-pro-preview", 1, 2.00, 12.00, 0.20, True),
    # Tier 2 · Strong, cheap
    Model("deepseek", "deepseek/deepseek-v3.2", 2, 0.26, 0.38, 0.13),
    Model("kimi", "moonshotai/kimi-k2-0905", 2, 0.60, 2.50),
    Model("glm", "z-ai/glm-4.6", 2, 0.50, 2.00, 0.10),
    Model("gemini_flash", "google/gemini-2.5-flash", 2, 0.30, 2.50, 0.03, True),
    Model("gpt5_mini", "openai/gpt-5-mini", 2, 0.25, 2.00, 0.025, True),
    Model("haiku", "anthropic/claude-haiku-5.5", 2, 0.10, 0.50, 0.01, True),
    # Tier 3 · General
    Model("flash_lite", "google/gemini-2.5-flash-lite", 3, 0.10, 0.40, 0.01, True),
    Model("gpt5_nano", "openai/gpt-5-nano", 3, 0.05, 0.40, 0.005, True),
    Model("glm_flash", "z-ai/glm-5.3-flash", 3, 0.04, 0.078, 0.03),
]}


@dataclass(frozen=True)
class Route:
    """How one feature calls AI: primary model, fallbacks for outages, and an optional premium escalation."""

    feature: str
    primary: str
    fallbacks: tuple[str, ...] = ()
    premium: str | None = None  # used only when the caller asks for escalation and the student has premium budget
    max_tokens: int = 2000  # output cap per feature (cost control playbook, rule 6)
    reasoning: bool = False  # thinking only where needed (rule 7)
    timeout: float = 60.0
    indic_primary: str | None = None  # live chat in an Indian language goes to this model instead
    web_search: bool = False  # ground the answer in live web results (current affairs)
    notes: str = ""


def _r(feature, primary, fallbacks=(), **kw) -> Route:
    return Route(feature, primary, tuple(fallbacks), **kw)


# Feature-to-model routing map (blueprint pages 10–14).
ROUTES: dict[str, Route] = {r.feature: r for r in [
    # 1–3. Mock report + time analyser (one combined call); persona micro-update.
    _r("mock_report", "deepseek", ["gemini_flash"], max_tokens=3000, timeout=60,
       notes="Numbers come from code; the model only writes."),
    _r("persona_update", "flash_lite", ["gpt5_nano"], max_tokens=800, timeout=20),
    _r("deep_persona", "gpt5", ["sonnet"], max_tokens=4000, timeout=90, notes="Monthly, Pro only."),
    # 4–5. Study planner and rank predictor.
    _r("study_planner", "gpt5_mini", ["deepseek"], max_tokens=2500, timeout=60),
    _r("rank_predictor", "flash_lite", ["gpt5_nano"], max_tokens=800, timeout=20),
    # 6. Doubt solver: solution store first (no AI), then a cheap router, then the solver.
    _r("doubt_router", "flash_lite", ["gpt5_nano"], max_tokens=300, timeout=15),
    _r("doubt_solve_math", "deepseek", ["haiku"], premium="sonnet", reasoning=True, max_tokens=3000, timeout=60),
    _r("doubt_solve_verbal", "kimi", ["haiku"], premium="sonnet", max_tokens=2500, timeout=45),
    _r("doubt_verify", "gpt5_mini", ["haiku"], max_tokens=800, timeout=30,
       notes="Independent check by a different model; a mismatch escalates to the premium model."),
    _r("doubt_same_method", "flash_lite", ["gpt5_nano"], max_tokens=1200, timeout=20),
    # 7–9. AI Tutor.
    _r("tutor_smart", "glm", ["gemini_flash"], max_tokens=4500, timeout=60),
    _r("tutor_master", "sonnet", ["gemini_pro"], max_tokens=3500, timeout=60),
    _r("tutor_chat", "deepseek", ["haiku"], premium="sonnet", max_tokens=700, timeout=20,
       indic_primary="gemini_flash", notes="Kimi for story/memory-trick replies via tutor_chat_story."),
    _r("tutor_chat_story", "kimi", ["haiku"], premium="sonnet", max_tokens=700, timeout=20,
       indic_primary="gemini_flash"),
    _r("photo_doubt_read", "gemini_flash", ["gpt5_mini"], max_tokens=1500, timeout=30),
    # 10–14.
    _r("notes_personal", "glm", ["gemini_flash"], max_tokens=3000, timeout=60),
    _r("notes_master", "sonnet", ["gemini_flash"], max_tokens=6000, timeout=120, notes="Once per topic, offline."),
    _r("mistake_summary", "flash_lite", ["gpt5_mini"], max_tokens=1200, timeout=30),
    _r("mistake_visual", "glm", ["gpt5_mini"], max_tokens=3000, timeout=60),
    _r("revision_hints", "flash_lite", ["gpt5_nano"], max_tokens=500, timeout=20),
    _r("current_affairs", "gemini_flash", ["gpt5_mini"], max_tokens=6000, timeout=180, web_search=True,
       notes="Once a day for all students; a second model fact-checks."),
    _r("current_affairs_check", "gpt5_mini", ["deepseek"], max_tokens=1500, timeout=90, web_search=True),
    _r("descriptive_eval", "kimi", ["glm"], premium="sonnet", max_tokens=2500, timeout=60),
    # 15. Mock interview: cheap turns, one premium evaluation.
    _r("interview_turn", "kimi", ["glm", "sonnet"], max_tokens=400, timeout=20),
    _r("interview_scoring", "gpt5", ["sonnet"], max_tokens=5000, timeout=90),
    # 16–17. Topic Explainer and Cheat Code Coach.
    _r("topic_deck_outline", "gpt5_mini", ["gemini_flash"], max_tokens=2000, timeout=45),
    _r("topic_deck_smart", "glm", ["gemini_flash"], max_tokens=13500, timeout=120),
    _r("topic_deck_master", "sonnet", ["gemini_pro"], max_tokens=13500, timeout=180),
    _r("cheat_code_coach", "deepseek", ["gemini_flash"], max_tokens=800, timeout=20, indic_primary="gemini_flash"),
    _r("cheat_code_card", "kimi", ["gemini_flash"], max_tokens=600, timeout=20),
    _r("rule_test", "deepseek", ["gemini_flash"], max_tokens=1500, timeout=45,
       notes="Applies a student's rule to 5 bank questions; code compares with the answer key."),
    # Ultra pack (Tier 0): falls back to Opus, then the normal Master route.
    _r("ultra", "fable", ["opus", "sonnet"], max_tokens=6000, timeout=180),
    # Internal.
    _r("question_bank_write", "gpt5", ["gemini_pro"], premium="opus", max_tokens=4000, timeout=180),
    _r("question_bank_verify", "deepseek", ["gemini_pro"], reasoning=True, max_tokens=4000, timeout=180,
       notes="Must be a different model from the writer."),
    _r("translation", "gemini_flash", ["flash_lite"], max_tokens=4000, timeout=90,
       notes="Stand-in until self-hosted IndicTrans2 runs the nightly batch."),
    _r("back_translation", "gpt5_mini", ["deepseek"], max_tokens=2000, timeout=60,
       notes="A different model from the translator."),
    _r("guardrails", "gpt5_nano", ["flash_lite"], max_tokens=200, timeout=10),
    _r("content_qa", "flash_lite", ["gpt5_nano"], max_tokens=600, timeout=30),
    _r("nudges", "glm_flash", ["flash_lite"], max_tokens=300, timeout=20),
    _r("live_translation", "flash_lite", ["gemini_flash"], max_tokens=4000, timeout=45,
       notes="First request in a language; the result is stored and reused."),
]}

# Existing call sites ("purpose" in ai_usage) -> blueprint feature.
PURPOSE_TO_FEATURE = {
    "exam_report": "mock_report",
    "mentor_attempt_note": "persona_update",
    "mentor_plan_note": "study_planner",
    "mentor_chat": "tutor_chat",
    "interview_next": "interview_turn",
    "interview_report": "interview_scoring",
    "question_generate": "question_bank_write",
    "question_verify": "question_bank_verify",
    "translate": "translation",
    "back_translate": "back_translation",
    "lesson": "content_qa",
}


def _overrides() -> dict[str, str]:
    out = {}
    for entry in get_settings().ai_model_overrides.split(","):
        alias, _, model_id = entry.strip().partition("=")
        if alias and model_id:
            out[alias.strip()] = model_id.strip()
    return out


def model(alias: str) -> Model:
    """Resolves an alias (or the special alias "ultra") to a Model, applying AI_MODEL_OVERRIDES."""
    ov = _overrides()
    if alias == "ultra" and "ultra" not in ov:
        alias = get_settings().ai_ultra_model or "fable"
    if alias in ov:
        base = MODELS.get(alias)
        mid = ov[alias]
        known = next((m for m in MODELS.values() if m.id == mid), None)
        if known:
            return known
        return Model(alias, mid, base.tier if base else 2, base.usd_in if base else 0.0,
                     base.usd_out if base else 0.0, base.usd_cached_in if base else None)
    return MODELS[alias]


def route_for(purpose: str) -> Route:
    feature = PURPOSE_TO_FEATURE.get(purpose, purpose)
    if feature not in ROUTES:
        raise KeyError(f"no AI route for {purpose!r}")
    return ROUTES[feature]


def model_chain(route: Route, *, premium: bool = False, language: str | None = None) -> list[Model]:
    """Ordered models for one call: [primary, *fallbacks]. Premium escalation puts the premium model first and
    keeps the normal route behind it; an Indian-language live chat starts on the route's Indian-language model."""
    first = route.primary
    if language and language != "en" and route.indic_primary:
        first = route.indic_primary
    chain = [first] + [a for a in (route.primary, *route.fallbacks) if a != first]
    if premium and route.premium:
        chain = [route.premium] + [a for a in chain if a != route.premium]
    seen, out = set(), []
    for alias in chain:
        m = model(alias)
        if m.id not in seen:
            seen.add(m.id)
            out.append(m)
    return out


@lru_cache(maxsize=256)
def _price_by_id(model_id: str) -> Model | None:
    bare = model_id.split(":")[0]
    for m in MODELS.values():
        if m.id == bare or bare.endswith("/" + m.id.split("/")[-1]):
            return m
    return None


# Direct Anthropic API ids (AI_PROVIDER=claude) and legacy rows in ai_usage.
_DIRECT = {"claude-opus-5-5": "opus", "claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku"}


def cost_usd(model_id: str, input_tokens: int, output_tokens: int, cached_tokens: int = 0) -> float:
    m = next((MODELS[a] for k, a in _DIRECT.items() if model_id.startswith(k)), None) or _price_by_id(model_id)
    if m is None:
        return 0.0
    cached = min(cached_tokens or 0, input_tokens or 0)
    cached_rate = m.usd_cached_in if m.usd_cached_in is not None else m.usd_in
    return ((input_tokens or 0) - cached) / 1e6 * m.usd_in + cached / 1e6 * cached_rate \
        + (output_tokens or 0) / 1e6 * m.usd_out


def routing_table() -> list[dict]:
    """For the admin dashboard and docs: every feature with its resolved models and prices."""
    out = []
    for r in ROUTES.values():
        def desc(alias):
            m = model(alias)
            return {"alias": alias, "id": m.id, "tier": m.tier, "usd_per_mtok": [m.usd_in, m.usd_out]}
        out.append({"feature": r.feature, "primary": desc(r.primary), "fallbacks": [desc(a) for a in r.fallbacks],
                    "premium": desc(r.premium) if r.premium else None, "max_tokens": r.max_tokens,
                    "reasoning": r.reasoning, "timeout_s": r.timeout, "web_search": r.web_search,
                    "indic_primary": desc(r.indic_primary) if r.indic_primary else None, "notes": r.notes})
    return out
