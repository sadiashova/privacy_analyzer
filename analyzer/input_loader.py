import requests
import trafilatura

MAX_CHARS = 200_000

def load_from_text(text: str) -> str:
    """Accept pasted text and clean it a little."""
    text = (text or "").strip()
    if len(text) < 50:
        raise ValueError("Please paste at least a few paragraphs of policy text.")
    return text[:MAX_CHARS]

def load_from_url(url: str) -> str:
    """Download a web page and extract the main text."""
    url = (url or "").strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "PrivacyAnalyzerBot/1.0"}
    )
    response.raise_for_status()

    text = trafilatura.extract(response.text) or ""
    if not text:
        raise ValueError("Could not extract text from this page.")

    return text[:MAX_CHARS]
