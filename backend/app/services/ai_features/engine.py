"""Shared plumbing for the student AI features.

- `charge()`: spends an allowance and gives it back automatically if the AI work fails (technical failures never
  cost the student).
- `ask()`: one routed AI call (model chosen by app/ai/catalog.py), in the student's language when the route has an
  Indian-language model.
- `cached()` / `store()`: generated content shared by key and language ("solve once, store forever").
- `localize()`: English JSON made once, translated per language on first request and stored.
- `distress()`: the wellbeing check; a stressed message gets support options, never a lecture.

Only anonymised study data is ever sent to a model: no name, phone or email (wrap_data strips them anyway).
"""

import json
import re
from contextlib import contextmanager

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.provider import AIError, get_provider
from app.ai.safety import DATA_RULES, wrap_data
from app.core.errors import AppError
from app.core.languages import is_supported, language_name
from app.models import AiArtifact, User
from app.services import allowances

TELE_MANAS = ("It sounds like this is weighing on you. You are not alone: India's free Tele-MANAS helpline (14416 or "
              "1-800-891-4416) has trained counsellors 24x7, in many languages. A score is never the measure of you. "
              "When you feel ready, we can take one small step together.")

_DISTRESS = re.compile(r"\b(kill myself|suicid|end my life|want to die|no point living|can'?t go on|"
                       r"hurt myself|self[- ]harm|jeena nahi|marna chahta|marna chahti)\b", re.I)

COACH_RULES = (
    "Tone: warm, direct and never shaming. Use simple words a student in India understands. Only help with exam "
    "preparation (aptitude, reasoning, English, general awareness, subjects of Indian competitive exams). Politely "
    "decline anything else (other homework, coding, chit-chat) and steer back to preparation. "
    + DATA_RULES
)


def distress(text: str | None) -> bool:
    return bool(text and _DISTRESS.search(text))


def lang_of(user: User, requested: str | None = None) -> str:
    lang = (requested or user.preferred_language or "en").lower()
    if not is_supported(lang):
        raise AppError(422, "unsupported_language", f"Language {lang!r} is not supported")
    return lang


@contextmanager
def charge(db: Session, user: User, feature: str, *, ref_id, units: int = 1, want_premium: bool = False):
    """Spends `units` of a metered allowance for the block's work; refunds them if the block raises."""
    used = allowances.use(db, user, feature, ref_id=ref_id, want_premium=want_premium, units=units)
    try:
        yield used
    except Exception:
        db.rollback()
        allowances.refund_use(db, user, feature, ref_id)
        db.commit()
        raise


def require_flag(db: Session, user: User, flag: str, plan_hint: str) -> None:
    if not allowances.has_flag(db, user, flag):
        raise AppError(402, "plan_required", f"This feature is part of {plan_hint}.")


def ask(db: Session, *, purpose: str, system: str, prompt: str, schema: dict, ref_id=None, premium=False,
        language: str | None = None, images: list[str] | None = None, context: dict | None = None) -> dict:
    """One routed AI call. AIError becomes a friendly 503 so the student can retry (and the allowance is refunded
    by `charge`)."""
    try:
        return get_provider().generate_json(purpose=purpose, system=system, prompt=prompt, schema=schema,
                                            ref_id=ref_id, db=db, premium=premium, language=language, images=images,
                                            context=context or {})
    except AIError as e:
        raise AppError(503, "ai_unavailable", "The AI tutor is busy right now. Please try again in a minute.",
                       {"reason": str(e)[:200]}) from e


def language_instruction(language: str) -> str:
    if language == "en":
        return "Write every text field in English."
    return (f"Write every text field in {language_name(language)} ({language}), in its native script. Keep numbers, "
            "formulas, option letters and exam terms in standard digits and Latin letters.")


def cached(db: Session, kind: str, key: str, language: str = "en", user_id=None) -> AiArtifact | None:
    q = select(AiArtifact).where(AiArtifact.kind == kind, AiArtifact.cache_key == key[:300],
                                 AiArtifact.language == language, AiArtifact.status != "hidden")
    q = q.where(AiArtifact.user_id.is_(None)) if user_id is None else q.where(AiArtifact.user_id == user_id)
    return db.scalar(q.order_by(AiArtifact.created_at.desc()).limit(1))


def store(db: Session, kind: str, key: str, payload: dict, *, language: str = "en", user_id=None, title: str = "",
          model: str = "") -> AiArtifact:
    a = AiArtifact(kind=kind, cache_key=key[:300], language=language, payload=payload, user_id=user_id,
                   title=(title or payload.get("title") or "")[:300], model=model)
    db.add(a)
    db.flush()
    return a


def artifact_out(a: AiArtifact, *, cached_hit: bool | None = None) -> dict:
    out = {"id": a.id, "kind": a.kind, "title": a.title, "language": a.language, "created_at": a.created_at,
           "payload": a.payload, "shared": a.user_id is None or a.status == "shared"}
    if cached_hit is not None:
        out["from_cache"] = cached_hit
    return out


# ---- live translation (stored after the first request) ------------------------------------------------------------
TRANSLATE_SYSTEM = ("You translate study material for Indian exam candidates. Translate every string value of the JSON "
                    "faithfully; keep keys, structure, numbers, formulas, option letters and Mermaid code unchanged. "
                    + DATA_RULES)


def _string_schema(value):
    """Schema mirroring a JSON value with every leaf as a string or number, for strict structured output."""
    if isinstance(value, dict):
        return {"type": "object", "additionalProperties": False, "required": list(value),
                "properties": {k: _string_schema(v) for k, v in value.items()}}
    if isinstance(value, list):
        return {"type": "array", "items": _string_schema(value[0]) if value else {"type": "string"}}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, (int, float)):
        return {"type": "number"}
    return {"type": "string"}


def localize(db: Session, payload: dict, language: str, *, ref_id=None) -> dict:
    """Translates an English payload into `language` (Gemini Flash-Lite route). English is returned unchanged."""
    if language == "en" or not payload:
        return payload
    out = ask(db, purpose="live_translation", system=TRANSLATE_SYSTEM, schema=_string_schema(payload),
              prompt=f"Target language: {language_name(language)} ({language}).\n"
                     + wrap_data("content", json.dumps(payload, ensure_ascii=False), 30000), ref_id=ref_id)
    return out if isinstance(out, dict) else payload


def cached_localized(db: Session, kind: str, key: str, language: str, make_english, *, user_id=None,
                     title: str = "") -> tuple[AiArtifact, bool]:
    """Returns (artifact in `language`, from_cache). Builds the English version once with `make_english()`, then
    translates it once per language. Both are stored, so the next student pays nothing."""
    hit = cached(db, kind, key, language, user_id)
    if hit is not None:
        hit.times_served += 1
        return hit, True
    en = cached(db, kind, key, "en", user_id)
    if en is None:
        payload, model = make_english()
        en = store(db, kind, key, payload, user_id=user_id, title=title, model=model)
        if language == "en":
            return en, False
    en.times_served += 1
    return store(db, kind, key, localize(db, en.payload, language, ref_id=en.id), language=language,
                 user_id=user_id, title=en.title, model=en.model), False
