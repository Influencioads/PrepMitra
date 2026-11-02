"""Speech adapters for voice interviews (PDF 5.4, 8).

Providers are chosen per language (Bhashini, Sarvam AI, AI4Bharat, Google Cloud, Azure) after accuracy/cost
evaluation. Until then `MockSpeech` is used:
- STT: audio chunks that are UTF-8 text are treated as the transcript (lets clients and tests exercise the flow);
  real audio returns "[voice transcription unavailable in dev]".
- TTS: returns None, so clients fall back to on-device text-to-speech.
INCOMPLETE: no real STT/TTS provider is integrated yet (needs provider accounts).
"""

import re

from app.config import get_settings
from app.core.languages import LANGUAGES

FILLERS = {
    "en": ["um", "uh", "erm", "like", "basically", "actually", "you know", "i mean", "so yeah", "kind of"],
    "hi": ["matlab", "toh", "haan", "accha", "woh", "na", "yaani", "um", "uh"],
    "ta": ["vandhu", "apdi", "ennanaa", "um", "uh"],
}


class MockSpeech:
    name = "mock"

    def transcribe(self, audio: bytes, language: str, mime: str | None = None) -> str:
        try:
            text = audio.decode("utf-8")
            if text.isprintable() or "\n" in text:
                return text.strip()
        except UnicodeDecodeError:
            pass
        return "[voice transcription unavailable in dev]"

    def synthesize(self, text: str, language: str) -> bytes | None:
        return None


def get_speech():
    # Real providers plug in here, selected per language.
    return MockSpeech()


def voice_supported(language: str) -> bool:
    """Voice launches in Tier 1 languages first (PDF 8); Tier 2 follows after speech-quality testing."""
    return LANGUAGES.get(language, {}).get("tier") == 1


def filler_count(text: str, language: str) -> dict[str, int]:
    low = f" {text.lower()} "
    out = {}
    for f in FILLERS.get(language, []) + (FILLERS["en"] if language != "en" else []):
        n = len(re.findall(rf"(?<!\w){re.escape(f)}(?!\w)", low))
        if n:
            out[f] = out.get(f, 0) + n
    return out


def speaking_metrics(turns: list[tuple[str, float | None]], language: str) -> dict:
    """turns: (transcript, duration_sec). Pace and filler words are computed by code (PDF 5.6)."""
    words = sum(len(t.split()) for t, _ in turns)
    seconds = sum(d for _, d in turns if d)
    fillers: dict[str, int] = {}
    for t, _ in turns:
        for k, v in filler_count(t, language).items():
            fillers[k] = fillers.get(k, 0) + v
    return {"words": words, "speaking_sec": round(seconds, 1),
            "words_per_minute": round(words / (seconds / 60), 1) if seconds else None,
            "filler_count": sum(fillers.values()), "fillers": fillers, "speech_provider": get_settings().speech_provider}
