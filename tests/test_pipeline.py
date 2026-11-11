from analyzer.pipeline import analyze_policy


def test_analyze_policy_full_flow():
    sample_text = (
        "We collect your email address and location to provide our service. "
        "We share your data with trusted advertising partners. "
        "We use cookies and tracking beacons to monitor usage. "
        "You can access, correct, or delete your information at any time."
    )
    result = analyze_policy(text=sample_text)

    assert "language" in result
    assert result["language"] == "en"
    assert "risk" in result
    assert result["risk"]["score"] > 0
    assert "level" in result["risk"]
    assert "summary" in result
    assert len(result["summary"]) > 0
    assert "findings" in result
    assert len(result["findings"]["collection"]) > 0
    assert len(result["findings"]["sharing"]) > 0
    assert len(result["findings"]["rights"]) > 0


def test_analyze_policy_short_text_raises_error():
    try:
        analyze_policy(text="Too short")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Please paste at least a few paragraphs" in str(e)
