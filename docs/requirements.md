# Requirements & Specifications

## 1. Functional Requirements

### 1.1 Ingestion
- **Text Input:** Ingest pasted privacy policy text with minimum length validation ($\ge 50$ characters).
- **URL Scraping:** Download web pages via HTTP/HTTPS, extract clean textual content, strip boilerplate HTML (nav, header, footer, scripts), and handle network errors/timeouts.
- **Safety Limits:** Truncate incoming raw text at 200,000 characters to prevent memory exhaustion.

### 1.2 Language Detection
- Identify whether the policy is written in **English** (`en`) or **Danish** (`da`).
- Support language-aware keyword matching to avoid cross-lingual false positives.

### 1.3 Disclosure Extraction
Identify disclosures across seven key privacy domains:
1. **Data Collection:** Email, phone, location, name, IP address, etc.
2. **Processing Purpose:** Personalization, improvement, analytics, service delivery.
3. **Third-Party Sharing:** Advertisers, analytics partners, data brokers.
4. **Tracking & Cookies:** Beacons, tracking pixels, cookies, profiling.
5. **Data Retention:** Storage duration and criteria for retention.
6. **Security Safeguards:** Encryption, access control, protective measures.
7. **User Rights:** Access, correction, deletion, consent withdrawal, objection.

### 1.4 Risk Scoring
- Assign numeric weights to privacy-intrusive vs. protective practices.
- Compute an aggregate score and map it to `Low` ($\le 3$), `Medium` ($4$ to $7$), or `High` ($\ge 8$).

### 1.5 Summarization
- Output high-level bullet points summarizing findings for each category.

---

## 2. Technical Stack
- **Language:** Python 3.10+
- **NLP / Parsing:** Standard regex (`re`), `BeautifulSoup4`, `trafilatura`, `langdetect`
- **Testing:** Unit test suite covering extractor, pipeline, and risk scorer
- **UI:** Streamlit web interface (`app.py`)

