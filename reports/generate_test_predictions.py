from pathlib import Path

import pandas as pd

from analyzer.extractor import classify_sentence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LABELS_FILE = PROJECT_ROOT / "data" / "labels.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "test_prediction.csv"

categories = [
    "collection",
    "purpose",
    "sharing",
    "tracking",
    "retention",
    "security",
    "rights",
]

labels_df = pd.read_csv(LABELS_FILE)

required_columns = ["sentence", *categories]
missing_columns = [
    column for column in required_columns
    if column not in labels_df.columns
]

if missing_columns:
    raise ValueError(
        "Missing columns in labels.csv: " + ", ".join(missing_columns)
    )

if labels_df.empty:
    raise ValueError("labels.csv contains no labelled sentences.")

rows = []

for _, source_row in labels_df.iterrows():
    lang = str(source_row["language"]) if "language" in source_row else None
    predictions = classify_sentence(str(source_row["sentence"]), language=lang)

    output_row = {}

    for category in categories:
        true_value = int(source_row[category])
        predicted_value = int(predictions[category])

        output_row[f"{category}_true"] = true_value
        output_row[f"{category}_pred"] = predicted_value

    rows.append(output_row)

predictions_df = pd.DataFrame(rows)
predictions_df.to_csv(OUTPUT_FILE, index=False)

print(f"Created: {OUTPUT_FILE}")
print(f"Evaluated sentences: {len(predictions_df)}")
print(predictions_df.to_string(index=False))
