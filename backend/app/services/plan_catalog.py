"""Plans, AI Tutor packs and add-ons from the pricing blueprint (Nov 2026). Prices are GST-inclusive, in paise.

`credits` = full mocks for the whole billing period (1 credit = 1 full mock or 1 interview, as before), so the
existing credit ledger keeps working. Every other AI allowance lives in `entitlements["limits"]`:

- On subscriptions (study plans, tutor packs, combo) limits are per calendar month, whatever the billing period.
- On add-ons limits are a one-off pool that lasts the add-on's validity.
- FREE is what every signed-up student gets, for life (doubts, the sample deep dive) or always (libraries).

Blueprint margins at these prices (monthly plans): Starter 80% typical / 57% max use, Pro 77% / 46%,
Tutor Lite 72% / 30%, Tutor Pro 72% / 29%, Topper Combo 71% / 26%.
"""

# Metered features. A request that wants premium escalation also needs one unit of the "premium_*" twin.
METERED = {
    "sectional_tests": "Sectional tests",
    "doubts": "AI doubts",
    "premium_doubts": "Doubts with premium escalation",
    "personal_notes": "Personal notes and mind maps",
    "topic_decks": "Custom Topic Explainer decks",
    "cheat_code_sessions": "Cheat Code Coach sessions",
    "descriptive_evals": "Descriptive writing evaluations",
    "text_interviews": "Text mock interviews",
    "voice_interviews": "Voice mock interviews",
    "smart_credits": "Smart tutor credits (deep dive = 1, topic deck = 3)",
    "master_credits": "Master tutor credits (deep dive or topper rewrite = 1)",
    "tutor_chat_turns": "Ask Mitra tutor chat turns",
    "photo_doubts": "Photo doubts",
    "ultra_credits": "Ultra credits (deep dive = 1, topic deck = 4)",
}

# Feature switches (not counted).
FLAGS = ("persona", "deep_persona", "study_planner", "revision_ai", "mistake_notebook", "mistake_notebook_visual",
         "current_affairs", "rank_predictor", "topic_library", "shortcut_library", "leaderboard")

LIBRARIES = {"topic_library": True, "shortcut_library": True, "leaderboard": True}

FREE = {
    "group": "free", "period": "lifetime",
    "flags": {**LIBRARIES, "persona": "snapshot"},
    # 1 full mock per exam category comes from the free-trial exam; these are lifetime allowances.
    "limits": {"doubts": 5, "smart_credits": 1},
}

STARTER = {
    "flags": {**LIBRARIES, "persona": "full", "study_planner": True, "revision_ai": True, "mistake_notebook": True},
    "limits": {"sectional_tests": 30, "doubts": 50, "personal_notes": 5, "cheat_code_sessions": 3},
}
PRO = {
    "flags": {**STARTER["flags"], "deep_persona": True, "current_affairs": True, "rank_predictor": True},
    "limits": {"sectional_tests": 100, "doubts": 150, "premium_doubts": 50, "personal_notes": 20, "topic_decks": 5,
               "cheat_code_sessions": 10, "descriptive_evals": 4, "text_interviews": 2},
}
TUTOR_LITE = {
    "flags": {},
    "limits": {"smart_credits": 20, "tutor_chat_turns": 150, "photo_doubts": 15, "cheat_code_sessions": 3},
}
TUTOR_PRO = {
    "flags": {"mistake_notebook_visual": True},
    "limits": {"smart_credits": 40, "master_credits": 10, "tutor_chat_turns": 300, "photo_doubts": 40,
               "cheat_code_sessions": 5},
}


def _merge(*parts: dict) -> dict:
    flags, limits = {}, {}
    for p in parts:
        flags.update(p["flags"])
        for k, v in p["limits"].items():
            limits[k] = limits.get(k, 0) + v
    return {"flags": flags, "limits": limits}


COMBO = _merge(PRO, TUTOR_PRO)

PERIOD_DAYS = {"monthly": 30, "quarterly": 90, "annual": 365}
PERIOD_MONTHS = {"monthly": 1, "quarterly": 3, "annual": 12}


def _sub(code, name, price_rupees, group, period, mocks_per_month, ent) -> dict:
    return {"code": code, "name": name, "price_paise": price_rupees * 100,
            "credits": mocks_per_month * PERIOD_MONTHS[period], "validity_days": PERIOD_DAYS[period],
            "is_recurring": True,
            "entitlements": {"group": group, "period": period, "full_mocks_per_month": mocks_per_month, **ent}}


def _addon(code, name, price_rupees, credits, days, limits=None) -> dict:
    return {"code": code, "name": name, "price_paise": price_rupees * 100, "credits": credits, "validity_days": days,
            "is_recurring": False,
            "entitlements": {"group": "addon", "period": "one_time", "flags": {}, "limits": limits or {}}}


PLANS: list[dict] = [
    {"code": "free_trial", "name": "Free", "price_paise": 0, "credits": 1, "validity_days": 30, "is_recurring": False,
     "entitlements": FREE},
    # Study plans
    _sub("starter_monthly", "Starter (Mock Pass) · monthly", 149, "study", "monthly", 10, STARTER),
    _sub("starter_quarterly", "Starter (Mock Pass) · quarterly", 399, "study", "quarterly", 10, STARTER),
    _sub("starter_annual", "Starter (Mock Pass) · annual", 1199, "study", "annual", 10, STARTER),
    _sub("pro_monthly", "Pro (Selection Pass) · monthly", 299, "study", "monthly", 25, PRO),
    _sub("pro_quarterly", "Pro (Selection Pass) · quarterly", 799, "study", "quarterly", 25, PRO),
    _sub("pro_annual", "Pro (Selection Pass) · annual", 2499, "study", "annual", 25, PRO),
    # AI Tutor packs (work with any plan, including Free)
    _sub("tutor_lite_monthly", "AI Tutor Lite · monthly", 99, "tutor", "monthly", 0, TUTOR_LITE),
    _sub("tutor_lite_annual", "AI Tutor Lite · annual", 999, "tutor", "annual", 0, TUTOR_LITE),
    _sub("tutor_pro_monthly", "AI Tutor Pro · monthly", 299, "tutor", "monthly", 0, TUTOR_PRO),
    _sub("tutor_pro_annual", "AI Tutor Pro · annual", 2999, "tutor", "annual", 0, TUTOR_PRO),
    _sub("combo_monthly", "Topper Combo (Pro + AI Tutor Pro) · monthly", 499, "combo", "monthly", 25, COMBO),
    _sub("combo_annual", "Topper Combo (Pro + AI Tutor Pro) · annual", 4999, "combo", "annual", 25, COMBO),
    # Add-ons
    _addon("single_mock", "Single mock with AI report", 29, 1, 90),
    _addon("extra_mocks_5", "5 extra full mocks", 49, 5, 90),
    _addon("extra_doubts_50", "50 extra Smart doubts", 39, 0, 90, {"doubts": 50}),
    _addon("extra_master_10", "10 extra Master deep dives", 99, 0, 90, {"master_credits": 10}),
    _addon("interview_pack", "Interview Pack (2 voice + 5 text)", 199, 0, 60,
           {"voice_interviews": 2, "text_interviews": 5}),
    # Ultra pack priced at ~2.5x the cost of 10 Ultra deep dives on the default Tier 0 model (Claude Fable 5.2 at
    # $8/$40 per 1M tokens on OpenRouter, Nov 2026: ~Rs 13 per deep dive). Re-price if AI_ULTRA_MODEL changes.
    _addon("ultra_pack", "Ultra pack (10 Ultra credits)", 349, 0, 30, {"ultra_credits": 10}),
]

# Plans from earlier catalogs: kept in the table (old orders reference them) but no longer sold.
RETIRED = ("pay_per_exam", "monthly", "yearly", "credit_pack_10")

# Launch offer from the blueprint (Pro annual at Rs 1,999 for the first 1,000 students) is a coupon, not a plan.
