def score_policy(findings: dict[str, list[str]], full_text: str) -> dict:
    """
    Gives a simple risk score based on what was found in the policy.
    """
    score = 0
    factors = []

    text = full_text.lower()

    # Sharing data with others adds risk
    if findings["third_party_sharing"]:
        score += 3
        factors.append(("+3", "The policy says data may be shared with third parties"))

    # Collecting many types of personal data adds risk
    data_keywords = [
        "email", "e-mail", "location", "address", "phone",
        "ip address", "navn", "adresse", "telefonnummer", "placering"
    ]
    data_types = sum(1 for keyword in data_keywords if keyword in text)
    if data_types >= 3:
        score += 3
        factors.append(("+3", f"The policy mentions many kinds of personal data ({data_types})"))

    # Tracking adds risk
    if findings["tracking"]:
        score += 2
        factors.append(("+2", "The policy mentions cookies, pixels, or tracking"))

    # User rights lower the risk a little
    if findings["user_rights"]:
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
        "factors": factors
    }
