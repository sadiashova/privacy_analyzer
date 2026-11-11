from analyzer.extractor import classify_sentence, extract_findings, is_negated


def test_classify_english_collection():
    res = classify_sentence("We collect your email address.", language="en")
    assert res["collection"] == 1
    assert res["sharing"] == 0


def test_word_boundary_delete_not_sharing():
    # "delete" should not match Danish "dele"
    res = classify_sentence("You can delete your account anytime.", language="en")
    assert res["sharing"] == 0
    assert res["rights"] == 1


def test_word_boundary_deletion_rights():
    # "deletion" should match rights, not sharing
    res = classify_sentence("You may request deletion of your information.", language="en")
    assert res["sharing"] == 0
    assert res["rights"] == 1


def test_classify_danish_sentence():
    res = classify_sentence("Vi opbevarer dine personoplysninger i fem år.", language="da")
    assert res["retention"] == 1
    assert res["sharing"] == 0


def test_negation_detection():
    sentence = "We do not collect or sell your personal information."
    assert is_negated(sentence, "collection") is True
    assert is_negated(sentence, "sharing") is True

    res = classify_sentence(sentence, language="en")
    assert res["collection"] == 0
    assert res["sharing"] == 0


def test_extract_findings():
    sentences = [
        "We collect your email and address.",
        "We share data with advertising partners.",
        "You can request deletion of your personal data.",
    ]
    findings = extract_findings(sentences, language="en")
    assert len(findings["collection"]) == 1
    assert len(findings["sharing"]) == 1
    assert len(findings["rights"]) == 1
    assert len(findings["retention"]) == 0

