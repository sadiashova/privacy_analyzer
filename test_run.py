from analyzer.pipeline import analyze_policy

# Example: a short privacy policy text
sample_text = """
We collect your email and location to improve our service.
We share your data with our advertising partners.
You can access or delete your data at any time.
We use cookies to track your activity.
"""

result = analyze_policy(text=sample_text)

print("=== Language ===")
print(result["language"])

print("\n=== Risk ===")
print(f"Score: {result['risk']['score']}")
print(f"Level: {result['risk']['level']}")
for (points, reason) in result["risk"]["factors"]:
    print(f"{points} {reason}")

print("\n=== Summary ===")
for line in result["summary"]:
    print(line)
