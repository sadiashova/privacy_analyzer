# Privacy Policy Analyzer

A lightweight NLP tool designed to analyze privacy policies (in English and Danish), classify disclosures across 7 key privacy categories, estimate privacy risk, and generate structured summaries.

## Features

- **Multi-Input Support:** Paste raw policy text or fetch directly from a web URL.
- **Bilingual NLP Extraction:** Supports both English (`en`) and Danish (`da`) policy texts with regex word-boundary pattern matching.
- **7 Privacy Categories:**
  1. `collection` - Personal data types collected (email, location, phone, etc.)
  2. `purpose` - Purposes of data processing (analytics, service improvement)
  3. `sharing` - Disclosures to third parties, partners, or advertisers
  4. `tracking` - Tracking technologies (cookies, beacons, profiling, pixels)
  5. `retention` - Data storage and retention duration
  6. `security` - Safeguards, encryption, and protection measures
  7. `rights` - User rights (access, deletion, correction, opt-out)
- **Risk Scoring Engine:** Evaluates policy risk score and assigns a risk tier (`Low`, `Medium`, `High`) based on weighted disclosure factors.
- **Interactive Web App:** Streamlit-powered dashboard for interactive analysis.

## Project Structure

```
privacy_analyzer/
├── analyzer/
│   ├── input_loader.py    # Text loader and URL scraper (trafilatura / BeautifulSoup)
│   ├── language.py        # Language detector (langdetect with heuristic fallback)
│   ├── preprocess.py      # Text cleaning and sentence tokenization
│   ├── extractor.py       # Rule-based NLP classifier and findings extractor
│   ├── risk_scorer.py     # Privacy risk scoring logic
│   ├── summariser.py      # Bullet-point policy summarization
│   └── pipeline.py        # End-to-end analysis orchestration
├── data/
│   └── labels.csv         # Benchmark labeled dataset
├── reports/               # Performance evaluation and metrics scripts
├── tests/                 # Unit test suite
├── app.py                 # Streamlit web application
├── demo.py                # Demonstration script
└── requirements.txt       # Project dependencies
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
python demo.py
```

### 3. Launch the Web Interface
```bash
streamlit run app.py
```

### 4. Run Unit Tests
```bash
pytest
```
Or run with Python directly:
```bash
python -c "from tests import test_risk_scorer, test_extractor, test_pipeline"
```

