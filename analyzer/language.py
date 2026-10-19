from langdetect import detect

def detect_language(text: str) -> str:
    """Return 'en' for English, 'da' for Danish, or 'unknown'."""
    try:
        # We only need the first 1000 characters to figure out the language
        return detect(text[:1000])
    except Exception:
        return "unknown"
