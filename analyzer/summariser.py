def summarise(findings: dict[str, list[str]]) -> list[str]:
    """
    Creates one short bullet point for each privacy topic.
    If nothing was found for a topic, it says so.
    """
    labels = {
        "data_collection": "Data collected",
        "third_party_sharing": "Who data is shared with",
        "tracking": "Tracking",
        "user_rights": "Your rights",
    }

    bullets = []
    for key, label in labels.items():
        if findings[key]:
            # Show the first matching sentence, shortened to 200 characters
            snippet = findings[key][0][:200]
            bullets.append(f"**{label}:** {snippet}")
        else:
            bullets.append(f"**{label}:** Not clearly mentioned")

    return bullets
