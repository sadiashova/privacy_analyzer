import re

def clean_text(text: str) -> str:
    """Removes extra spaces and messy formatting."""
    # This turns multiple spaces/newlines into a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_sentences(text: str) -> list[str]:
    """Splits one big block of text into a list of individual sentences."""
    # Splits after a period, question mark, or exclamation point
    sentences = re.split(r"(?<=[.!?])\s+", clean_text(text))
    # Keep only sentences that aren't tiny
    return [s for s in sentences if len(s) > 10]
