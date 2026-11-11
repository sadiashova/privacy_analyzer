import re

PATTERNS_EN = {
    "collection": [
        "collect", "collects", "collection", "gather", "gathers", "obtain", "obtains",
        "receive", "receives", "email", "e-mail", "location", "address", "phone", "ip address",
    ],
    "purpose": [
        "purpose", "in order to", "so that", "personalize", "provide", "provider", "providers",
        "improve", "analyse", "analyze",
    ],
    "sharing": [
        "share", "shares", "sharing", "shared", "disclose", "disclosure", "sell", "selling",
        "partners", "advertisers", "third party", "third-party",
    ],
    "tracking": [
        "cookie", "cookies", "pixel", "pixels", "tracking", "beacon", "beacons",
        "profile", "profiling", "analytics",
    ],
    "retention": [
        "retain", "retention", "store", "stored", "keep", "delete after",
    ],
    "security": [
        "security", "protect", "protects", "encrypt", "encryption", "secure",
    ],
    "rights": [
        "access", "delete", "deletion", "erase", "erasure", "correct", "correction",
        "withdraw", "withdrawal", "opt out", "opt-out", "object", "right to",
    ],
}

PATTERNS_DA = {
    "collection": [
        "indsamle", "indsamler", "modtage", "modtager", "navn", "adresse",
        "telefonnummer", "placering",
    ],
    "purpose": [
        "formål", "for at", "til at", "personalisere", "levere", "forbedre", "analysere",
    ],
    "sharing": [
        "dele", "deler", "videregive", "videregiver", "sælge", "sælger",
        "tredjepart", "partnere", "annoncører",
    ],
    "tracking": [
        "sporing", "spore", "profilering", "cookie", "cookies",
    ],
    "retention": [
        "opbevare", "opbevarer", "opbevaret", "opbevaring", "gemme", "gemmer", "slette efter",
    ],
    "security": [
        "sikkerhed", "beskytte", "kryptere", "kryptering", "sikker",
    ],
    "rights": [
        "indsigt", "slette", "sletter", "slettet", "rettelse", "tilbagekalde",
        "fravælge", "gøre indsigelse", "ret til",
    ],
}

# Complete union for backwards compatibility and generic checks
PATTERNS = {
    category: list(dict.fromkeys(PATTERNS_EN.get(category, []) + PATTERNS_DA.get(category, [])))
    for category in PATTERNS_EN
}

NEGATED_ACTIONS = {
    "collection": [
        r"\b(?:do not|don't|does not|doesn't|will not|won't|never)\s+(?:(?:\w+[\s,]+){0,3})(?:collect|gather|obtain|receive)\b",
        r"\b(?:indsamler|modtager)\s+ikke\b",
    ],
    "sharing": [
        r"\b(?:do not|don't|does not|doesn't|will not|won't|never)\s+(?:(?:\w+[\s,]+){0,3})(?:share|disclose|sell)\b",
        r"\b(?:deler|videregiver|sælger)\s+ikke\b",
    ],
    "tracking": [
        r"\b(?:do not|don't|does not|doesn't|will not|won't|never)\s+(?:(?:\w+[\s,]+){0,3})(?:track|profile)\b",
        r"\b(?:sporer|profilerer)\s+ikke\b",
    ],
}


def is_negated(sentence: str, category: str) -> bool:
    """Checks if the sentence negates actions for a given category."""
    return any(
        re.search(pattern, sentence, flags=re.IGNORECASE)
        for pattern in NEGATED_ACTIONS.get(category, [])
    )


def _match_keyword(keyword: str, sentence: str) -> bool:
    """Matches a keyword using word boundaries to prevent substring false positives."""
    if keyword == "for at":
        pattern = r"\bfor at\b(?! least)"
    else:
        pattern = rf"\b{re.escape(keyword)}\b"
    return bool(re.search(pattern, sentence, flags=re.IGNORECASE))


def classify_sentence(sentence: str, language: str | None = None) -> dict[str, int]:
    """
    Classifies a sentence into privacy categories.
    Can optionally target patterns by detected language ('en', 'da').
    """
    predictions = {}

    for category in PATTERNS:
        if language == "en":
            keywords = PATTERNS_EN.get(category, [])
        elif language == "da":
            keywords = PATTERNS_DA.get(category, [])
        else:
            keywords = PATTERNS.get(category, [])

        matched = any(_match_keyword(keyword, sentence) for keyword in keywords)
        predictions[category] = int(matched and not is_negated(sentence, category))

    return predictions


def extract_findings(sentences: list[str], language: str | None = None) -> dict[str, list[str]]:
    """
    Extracts sentences matching privacy categories.
    """
    findings = {category: [] for category in PATTERNS}

    for sentence in sentences:
        predictions = classify_sentence(sentence, language=language)

        for category, predicted in predictions.items():
            if predicted == 1:
                findings[category].append(sentence)

    return findings
