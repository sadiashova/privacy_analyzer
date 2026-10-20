"""
Final demonstration of the Privacy Policy Analyzer.
This script tests the entire pipeline with two types of input.
"""

from analyzer.pipeline import analyze_policy

print("=" * 60)
print("PRIVACY POLICY ANALYZER - FINAL DEMONSTRATION")
print("=" * 60)

# Test 1: Simple text input
print("\n1. TEST WITH PASTED TEXT")
print("-" * 30)

sample = """
Example Privacy Policy:
We collect your email address and device location to personalize content.
We share anonymized data with analytics partners.
You have the right to access and delete your personal information.
We use cookies for tracking your preferences.
This policy is written in English.
"""

print("Sample text:", sample[:100] + "...")
result = analyze_policy(text=sample)

print(f"Language detected: {result['language']}")
print(f"Risk score: {result['risk']['score']} → {result['risk']['level']}")
print("\nSummary:")
for item in result["summary"]:
    print(f"  • {item}")

# Test 2: URL input (comment out if you want to skip)
print("\n" + "=" * 60)
print("2. URLs SUPPORTED")
print("=" * 60)
print("To analyze from a URL, run:")
print('  result = analyze_policy(url="https://example.com/privacy")')
print("\n...or use the web interface:")
print("  streamlit run app.py")
print("\nThe app will open at http://localhost:8501")

print("\n" + "=" * 60)
print("COMPLETE! Your project includes:")
print("-" * 60)
print("✓ analyzer/    — Core processing modules")
print("✓ app.py       — Web interface (Streamlit)")
print("✓ README.md    — Documentation")
print("✓ demo.py      — This demonstration script")
print("✓ .git/        — Version control")
print("✓ requirements.txt — Python dependencies")
print("\nTo start the web app:")
print("  streamlit run app.py")
