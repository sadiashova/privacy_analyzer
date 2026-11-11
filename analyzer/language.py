try:
    from langdetect import detect
except ImportError:
    detect = None


def detect_language(text: str) -> str:
    """Return 'en' for English, 'da' for Danish, or 'unknown'."""
    text = (text or "").strip()
    if not text:
        return "unknown"

    if detect is not None:
        try:
            return detect(text[:1000])
        except Exception:
            pass

    # Heuristic fallback if langdetect is unavailable or fails
    text_sample = text[:1000].lower()
    danish_markers = [
        "vi ", " og ", " i ", " er ", " på ", " for ",
        "dine ", "personoplysninger", "æ", "ø", "å",
    ]
    da_count = sum(1 for marker in danish_markers if marker in text_sample)
    if da_count >= 2:
        return "da"

    return "en"
