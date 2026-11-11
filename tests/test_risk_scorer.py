from analyzer.risk_scorer import score_policy


def empty_findings():
    return {
        "third_party_sharing": [],
        "tracking": [],
        "user_rights": [],
    }


def test_low_risk_with_user_rights():
    findings = empty_findings()
    findings["user_rights"] = [
        "You may request deletion of your data."
    ]

    result = score_policy(
        findings,
        "You may request deletion of your data."
    )

    assert result["score"] == -1
    assert result["level"] == "Low"
    assert len(result["factors"]) == 1


def test_high_risk_with_three_risk_categories():
    findings = empty_findings()
    findings["third_party_sharing"] = [
        "We share data with analytics providers."
    ]
    findings["tracking"] = [
        "We use cookies."
    ]

    result = score_policy(
        findings,
        "We collect your email, phone, and location. We use cookies."
    )

    assert result["score"] == 8
    assert result["level"] == "High"
    assert len(result["factors"]) == 3


def test_high_risk_with_many_personal_data_types():
    findings = empty_findings()
    findings["third_party_sharing"] = [
        "We share data with third parties."
    ]
    findings["tracking"] = [
        "We use tracking pixels."
    ]

    result = score_policy(
        findings,
        "We collect email, location, address, phone, and IP address."
    )

    assert result["score"] == 8
    assert result["level"] == "High"
    assert len(result["factors"]) == 3
def test_no_findings_returns_low_risk():
    findings = empty_findings()

    result = score_policy(findings, "This is a simple privacy policy.")

    assert result["score"] == 0
    assert result["level"] == "Low"
    assert result["factors"] == []
def test_medium_risk():
    findings = empty_findings()
    findings["third_party_sharing"] = [
        "We may share data with third parties."
    ]
    findings["tracking"] = [
        "We use cookies."
    ]
    findings["user_rights"] = [
        "You may request deletion of your data."
    ]

    result = score_policy(
        findings,
        "We use cookies, and you may request deletion of your data."
    )

    assert result["score"] == 4
    assert result["level"] == "Medium"
    assert len(result["factors"]) == 3


def test_standard_7_categories():
    findings = {
        "collection": ["We collect email and location."],
        "purpose": ["To improve services."],
        "sharing": ["We share data with partners."],
        "tracking": ["We track cookies."],
        "retention": [],
        "security": [],
        "rights": ["You can delete your data."],
    }
    result = score_policy(
        findings,
        "We collect your email, address, and phone number. We share with partners. We track cookies. You can delete.",
    )
    # +3 (sharing) + 3 (3 data types) + 2 (tracking) - 1 (rights) = 7 (Medium)
    assert result["score"] == 7
    assert result["level"] == "Medium"
    assert len(result["factors"]) == 4
