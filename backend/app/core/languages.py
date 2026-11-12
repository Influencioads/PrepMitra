"""English + the 22 scheduled Indian languages (PDF section 8)."""

LANGUAGES: dict[str, dict] = {
    "en": {"name": "English", "native": "English", "tier": 1, "rtl": False},
    "hi": {"name": "Hindi", "native": "हिन्दी", "tier": 1, "rtl": False},
    "bn": {"name": "Bengali", "native": "বাংলা", "tier": 1, "rtl": False},
    "mr": {"name": "Marathi", "native": "मराठी", "tier": 1, "rtl": False},
    "te": {"name": "Telugu", "native": "తెలుగు", "tier": 1, "rtl": False},
    "ta": {"name": "Tamil", "native": "தமிழ்", "tier": 1, "rtl": False},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "tier": 1, "rtl": False},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "tier": 1, "rtl": False},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "tier": 1, "rtl": False},
    "or": {"name": "Odia", "native": "ଓଡ଼ିଆ", "tier": 1, "rtl": False},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "tier": 1, "rtl": False},
    "ur": {"name": "Urdu", "native": "اردو", "tier": 1, "rtl": True},
    "as": {"name": "Assamese", "native": "অসমীয়া", "tier": 2, "rtl": False},
    "ne": {"name": "Nepali", "native": "नेपाली", "tier": 2, "rtl": False},
    "kok": {"name": "Konkani", "native": "कोंकणी", "tier": 2, "rtl": False},
    "mai": {"name": "Maithili", "native": "मैथिली", "tier": 2, "rtl": False},
    "sa": {"name": "Sanskrit", "native": "संस्कृतम्", "tier": 2, "rtl": False},
    "sd": {"name": "Sindhi", "native": "سنڌي", "tier": 2, "rtl": True},
    "ks": {"name": "Kashmiri", "native": "کٲشُر", "tier": 2, "rtl": True},
    "doi": {"name": "Dogri", "native": "डोगरी", "tier": 2, "rtl": False},
    "brx": {"name": "Bodo", "native": "बड़ो", "tier": 2, "rtl": False},
    "mni": {"name": "Manipuri", "native": "ꯃꯤꯇꯩꯂꯣꯟ", "tier": 2, "rtl": False},
    "sat": {"name": "Santali", "native": "ᱥᱟᱱᱛᱟᱲᱤ", "tier": 2, "rtl": False},
}


def is_supported(code: str) -> bool:
    return code in LANGUAGES


def language_name(code: str) -> str:
    return LANGUAGES.get(code, LANGUAGES["en"])["name"]
