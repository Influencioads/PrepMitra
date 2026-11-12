"""Mentor thresholds and targets. Everything a product owner may want to tune lives here or in settings."""

from app.config import get_settings

# Section keys differ between exams ("quant" in PO, "numerical" in Clerk); the mentor reasons per subject.
SUBJECT_OF_SECTION = {
    "quant": "quant", "numerical": "quant", "maths": "quant",
    "reasoning": "reasoning",
    "english": "english",
    "ga": "general_awareness", "banking_ga": "general_awareness", "general_awareness": "general_awareness",
    "computer": "computer",
}
SUBJECT_NAMES = {
    "quant": "Quantitative Aptitude", "reasoning": "Reasoning", "english": "English",
    "general_awareness": "General / Banking Awareness", "computer": "Computer Knowledge",
}


def subject_of(section_key: str | None) -> str:
    return SUBJECT_OF_SECTION.get(section_key or "", section_key or "other")


# Target seconds per question by subject and difficulty (banking prelims pace). An exam can override them in its
# blueprint: marking_scheme.time_targets = {"<section_key>": {"easy": 30, "medium": 45, "hard": 70}}.
DEFAULT_TIME_TARGETS = {
    "quant": {"easy": 40, "medium": 60, "hard": 90},
    "reasoning": {"easy": 30, "medium": 50, "hard": 80},
    "english": {"easy": 20, "medium": 35, "hard": 55},
    "general_awareness": {"easy": 15, "medium": 20, "hard": 30},
    "computer": {"easy": 15, "medium": 20, "hard": 30},
}


def target_time(scheme: dict | None, section_key: str, difficulty: str, fallback: int) -> int:
    custom = ((scheme or {}).get("time_targets") or {}).get(section_key) or {}
    if difficulty in custom:
        return int(custom[difficulty])
    return int(DEFAULT_TIME_TARGETS.get(subject_of(section_key), {}).get(difficulty) or fallback or 60)


# Time bands, as a ratio of time spent to the target.
SLOW_RATIO = 1.5  # slower than this is "slow"
RUSHED_RATIO = 0.35  # a wrong answer faster than this is a likely guess or misread
SKIP_AFTER_RATIO = 0.5  # skipped after spending at least half the target: time lost for nothing

# Topic status bands on effective accuracy (recent form blended with all-time accuracy).
STATUS_BANDS = [(0.85, "strong"), (0.70, "good"), (0.55, "needs_improvement"), (0.40, "weak"), (0.0, "very_weak")]
RECENT_WEIGHT = 0.6  # share of recent form in the effective accuracy once there are two or more sessions
DECLINE_DROP = 0.15  # recent form this far below the earlier level = declining


def min_evidence() -> int:
    """Questions attempted on a topic before it is classified at all (never "weak" from one or two questions)."""
    return get_settings().mentor_min_evidence


MASTERY_MIN_ATTEMPTED = 15
MASTERY_MIN_SESSIONS = 2
MASTERY_MIN_ACCURACY = 0.85
MASTERY_MAX_TIME_RATIO = 1.3


def revision_intervals() -> list[int]:
    """Days between notebook reviews, one step per consecutive correct answer (spaced revision)."""
    raw = get_settings().mentor_revision_intervals_days
    return [max(1, int(x)) for x in raw.split(",") if x.strip()] or [1, 3, 7, 14, 30]


# Planner
FINAL_PHASE_DAYS = 3  # last days before the exam: revision only, no new difficult concepts
BLOCK_MIN = 30  # smallest topic block
REVIEW_AFTER_MOCK_MIN = 30
MAX_TOPICS_PER_DAY = 3
PRACTICE_REVIEW_FACTOR = 1.5  # practice blocks leave time to review each answer, not only to solve


def mock_every_days(days_left: int) -> int:
    """How often a full mock goes into the plan; closer to the exam, more often."""
    if days_left > 45:
        return 7
    if days_left > 20:
        return 5
    if days_left > 10:
        return 3
    return 2
