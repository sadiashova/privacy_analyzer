import re


def score_policy(findings: dict[str, list[str]], full_text: str) -> dict:
    """
    Gives a simple risk score based on what was found in the policy.
    Supports both standard keys ('sharing', 'rights', 'tracking')
    and legacy keys ('third_party_sharing', 'user_rights').
    """
    score = 0
    factors = []

    text = full_text.lower()

    # Sharing data with others adds risk
    sharing_findings = findings.get("sharing") or findings.get("third_party_sharing", [])
    if sharing_findings:
        score += 3
        factors.append(("+3", "The policy says data may be shared with third parties"))

    # Collecting many types of personal data adds risk
    data_keywords = [
        "email", "e-mail", "location", "address", "phone",
        "ip address", "navn", "adresse", "telefonnummer", "placering",
    ]
    data_types = sum(
        1 for keyword in data_keywords
        if re.search(rf"\b{re.escape(keyword)}\b", text, flags=re.IGNORECASE)
    )
    if data_types >= 3:
        score += 3
        factors.append(("+3", f"The policy mentions many kinds of personal data ({data_types})"))

    # Tracking adds risk
    tracking_findings = findings.get("tracking", [])
    if tracking_findings:
        score += 2
        factors.append(("+2", "The policy mentions cookies, pixels, or tracking"))

    # User rights lower the risk a little
    rights_findings = findings.get("rights") or findings.get("user_rights", [])
    if rights_findings:
        score -= 1
        factors.append(("-1", "The policy mentions user rights like delete, access, or opt out"))

    # Turn the final score into a simple level
    if score <= 3:
        level = "Low"
    elif score <= 7:
        level = "Medium"
    else:
        level = "High"

    return {
        "score": score,
        "level": level,
        "factors": factors,
    }
