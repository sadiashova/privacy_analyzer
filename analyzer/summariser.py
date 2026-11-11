def summarise(findings: dict[str, list[str]]) -> list[str]:
    """
    Creates short bullet points for privacy topics found in the policy.
    If nothing was found for a topic, it notes that.
    Supports both standard (7 categories) and legacy (4 categories) findings.
    """
    labels = {
        "collection": "Data collected",
        "purpose": "Processing purpose",
        "sharing": "Who data is shared with",
        "tracking": "Tracking & profiling",
        "retention": "Data retention",
        "security": "Data security",
        "rights": "Your rights",
    }

    alias_map = {
        "data_collection": "collection",
        "third_party_sharing": "sharing",
        "user_rights": "rights",
    }

    # Normalize findings keys to canonical names
    normalized: dict[str, list[str]] = {}
    for key, val in findings.items():
        canonical_key = alias_map.get(key, key)
        normalized.setdefault(canonical_key, []).extend(val)

    # Use 4-topic format if findings only contains legacy keys
    is_legacy_only = bool(findings) and set(findings.keys()).issubset(
        {"data_collection", "third_party_sharing", "tracking", "user_rights"}
    )

    if is_legacy_only:
        active_keys = ["collection", "sharing", "tracking", "rights"]
    else:
        active_keys = list(labels.keys())

    bullets = []
    for key in active_keys:
        label = labels.get(key, key.replace("_", " ").title())
        matches = normalized.get(key, [])
        if matches:
            snippet = matches[0][:200]
            bullets.append(f"**{label}:** {snippet}")
        else:
            bullets.append(f"**{label}:** Not clearly mentioned")

    return bullets
