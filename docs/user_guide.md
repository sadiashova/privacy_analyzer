# User Guide

This guide explains how to install, configure, and use the Privacy Policy Analyzer.

---

## 1. Setup

### Installation
Clone or navigate to the repository directory and install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 2. Using the Python API

You can import and run `analyze_policy` directly in your Python code:

```python
from analyzer.pipeline import analyze_policy

# Option A: Analyze from pasted text
policy_text = """
We collect your email address and location to provide our service.
We share data with our advertising partners.
You can delete your information at any time.
"""
result = analyze_policy(text=policy_text)

# Option B: Analyze directly from a URL
# result = analyze_policy(url="https://example.com/privacy-policy")

# Inspect the outputs:
print("Detected Language:", result["language"])
print("Risk Score:", result["risk"]["score"])
print("Risk Level:", result["risk"]["level"])

print("\nRisk Factors:")
for points, reason in result["risk"]["factors"]:
    print(f"  {points} -> {reason}")

print("\nSummary:")
for bullet in result["summary"]:
    print(f"  {bullet}")
```

---

## 3. Running the Streamlit Web App

To launch the web interface:

```bash
streamlit run app.py
```

1. Open your browser at `http://localhost:8501`.
2. Choose either **Paste Text** or **Enter URL**.
3. Click **Analyze Text** or **Analyze URL**.
4. View the interactive dashboard with risk score metrics, risk factors breakdown, language detection, and category summaries.

---

## 4. Running Tests & Benchmarks

### Run Unit Tests
```bash
pytest
```

### Run Benchmark Prediction Check
```bash
python check_data.py
```

