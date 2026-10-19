# These are the keywords we are looking for in the text.
# We include English and Danish words as per your contract.
PATTERNS = {
    "data_collection": [
        "email", "e-mail", "location", "address", "phone", "ip address", 
        "navn", "adresse", "telefonnummer", "placering"
    ],
    "third_party_sharing": [
        "share", "sell", "partners", "advertisers", "third party",
        "dele", "videregive", "tredjepart", "partnere"
    ],
    "tracking": [
        "cookie", "pixel", "tracking", "beacon", "sporing"
    ],
    "user_rights": [
        "access", "delete", "erase", "correct", "withdraw", "opt out",
        "indsigt", "slette", "rettelse", "tilbagekalde"
    ],
}

def extract_findings(sentences: list[str]) -> dict[str, list[str]]:
    """
    Goes through every sentence and checks if it contains 
    any of our privacy keywords.
    """
    findings = {category: [] for category in PATTERNS}
    
    for sentence in sentences:
        lowered_sentence = sentence.lower()
        
        for category, keywords in PATTERNS.items():
            # If any keyword from this category is in the sentence, save the sentence
            if any(word in lowered_sentence for word in keywords):
                findings[category].append(sentence)
                
    return findings
