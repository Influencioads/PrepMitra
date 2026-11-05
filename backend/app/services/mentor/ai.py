"""AI wording for the mentor, checked against the facts it was given.

The model only ever sees numbers computed by code. Its text is accepted only if every number in it can be found in
those facts (as given, as a percentage, rounded, or as a small count); otherwise the caller falls back to wording
built by code. That is how "the AI must not invent performance statistics" is enforced rather than hoped for.
"""

import logging
import re

from app.ai.provider import AIError, get_provider

log = logging.getLogger(__name__)

_NUM = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)")
SMALL_COUNTS = set(range(0, 11))  # "two sectional tests", "3 days": counts the mentor may use in advice


def _collect(value, out: set[float]) -> None:
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, (int, float)):
        v = float(value)
        out.update({round(v, 2), round(v, 1), float(round(v)), float(int(v))})
        if 0 <= v <= 1:  # accuracies stored as fractions are written as percentages
            out.update({float(round(v * 100)), round(v * 100, 1)})
        if v >= 60:  # seconds also read as minutes
            out.update({float(int(v // 60)), float(round(v / 60)), float(int(v % 60))})
        return
    if isinstance(value, str):
        for m in _NUM.findall(value):
            _collect(float(m), out)
        return
    if isinstance(value, dict):
        for v in value.values():
            _collect(v, out)
        return
    if isinstance(value, (list, tuple)):
        for v in value:
            _collect(v, out)


def allowed_numbers(facts) -> set[float]:
    out: set[float] = {float(n) for n in SMALL_COUNTS}
    _collect(facts, out)
    return out


def unsupported_numbers(text: str, facts) -> list[str]:
    allowed = allowed_numbers(facts)
    bad = []
    for m in _NUM.findall(text or ""):
        v = float(m)
        if v not in allowed and round(v, 1) not in allowed and float(round(v)) not in allowed:
            bad.append(m)
    return bad


def grounded_json(*, purpose: str, system: str, prompt: str, schema: dict, facts, text_fields: list[str],
                  ref_id=None, db=None, context: dict | None = None, tier: str = "fast") -> dict | None:
    """Calls the model and returns its JSON only if every number in `text_fields` is backed by `facts`.

    Returns None on any failure; callers always have a code-written fallback.
    """
    for _ in range(2):
        try:
            raw = get_provider().generate_json(purpose=purpose, system=system, prompt=prompt, schema=schema,
                                               tier=tier, ref_id=ref_id, db=db, context=context or {})
        except AIError as e:
            log.info("mentor AI call %s failed: %s", purpose, e)
            return None
        texts = []
        for f in text_fields:
            v = raw.get(f)
            texts.extend(v if isinstance(v, list) else [v])
        bad = [n for t in texts if isinstance(t, str) for n in unsupported_numbers(t, facts)]
        if not bad:
            return raw
        log.info("mentor AI output for %s cited numbers not in the data: %s", purpose, bad[:5])
    return None
