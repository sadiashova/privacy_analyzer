from analyzer.input_loader import load_from_text, load_from_url
from analyzer.language import detect_language
from analyzer.preprocess import clean_text, split_sentences
from analyzer.extractor import extract_findings
from analyzer.risk_scorer import score_policy
from analyzer.summariser import summarise


def analyze_policy(text: str | None = None, url: str | None = None) -> dict:
    """
    Runs the full analysis.
    Give it either pasted text or a URL.
    """
    # Step 1: get the raw text
    if url:
        raw_text = load_from_url(url)
    else:
        raw_text = load_from_text(text or "")

    # Step 2: detect the language
    language = detect_language(raw_text)

    # Step 3: clean the text and split it into sentences
    cleaned = clean_text(raw_text)
    sentences = split_sentences(cleaned)

    # Step 4: find privacy keywords
    findings = extract_findings(sentences)

    # Step 5: score the risk and write the summary
    risk = score_policy(findings, cleaned)
    summary = summarise(findings)

    return {
        "language": language,
        "risk": risk,
        "summary": summary,
        "findings": findings,
    }
