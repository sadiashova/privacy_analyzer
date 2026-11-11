from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS_FILE = PROJECT_ROOT / "data" / "test_prediction.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
TABLES_DIR = PROJECT_ROOT / "reports" / "tables"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

labels = [
    "collection",
    "purpose",
    "sharing",
    "tracking",
    "retention",
    "security",
    "rights",
]

display_names = [
    "Data collection",
    "Processing purpose",
    "Third-party sharing",
    "Tracking and profiling",
    "Data retention",
    "Security",
    "User rights and choices",
]

# Load true labels and model predictions
df = pd.read_csv(PREDICTIONS_FILE)

true_columns = [f"{label}_true" for label in labels]
predicted_columns = [f"{label}_pred" for label in labels]

missing_columns = [
    column
    for column in true_columns + predicted_columns
    if column not in df.columns
]

    if missing_columns:
        raise ValueError(
            "The following columns are missing from test_prediction.csv: "
            + ", ".join(missing_columns)
        )

y_true = df[true_columns].to_numpy()
y_pred = df[predicted_columns].to_numpy()

# Calculate category-level performance
precision, recall, f1, support = precision_recall_fscore_support(
    y_true,
    y_pred,
    average=None,
    zero_division=0,
)

results = pd.DataFrame(
    {
        "Category": display_names,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1,
        "Support": support,
    }
)

# Save the numeric table as CSV
table_file = TABLES_DIR / "category_performance.csv"
results.to_csv(table_file, index=False, float_format="%.3f")

# Create an image of the table
table_data = results.copy()
for column in ["Precision", "Recall", "F1-score"]:
    table_data[column] = table_data[column].map(lambda value: f"{value:.3f}")

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.axis("off")

table = ax.table(
    cellText=table_data.values,
    colLabels=table_data.columns,
    cellLoc="center",
    colLoc="center",
    loc="center",
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.6)

for column_index in range(len(table_data.columns)):
    table[(0, column_index)].set_facecolor("#2F5597")
    table[(0, column_index)].set_text_props(color="white", weight="bold")

plt.tight_layout()

table_image = TABLES_DIR / "category_performance_table.png"
plt.savefig(table_image, dpi=300, bbox_inches="tight")
plt.close()

# Create an F1-score bar chart
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(
    results["Category"],
    results["F1-score"],
    color="#4472C4",
)

ax.set_xlabel("F1-score")
ax.set_ylabel("Privacy category")
ax.set_title("Category-level Extraction Performance")
ax.set_xlim(0, 1)

for bar, score in zip(bars, results["F1-score"]):
    ax.text(
        min(score + 0.015, 0.96),
        bar.get_y() + bar.get_height() / 2,
        f"{score:.3f}",
        va="center",
    )

ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.invert_yaxis()
plt.tight_layout()

figure_file = FIGURES_DIR / "category_f1_scores.png"
plt.savefig(figure_file, dpi=300, bbox_inches="tight")
plt.close()

print(f"CSV table saved to: {table_file}")
print(f"Table image saved to: {table_image}")
print(f"F1-score graph saved to: {figure_file}")
