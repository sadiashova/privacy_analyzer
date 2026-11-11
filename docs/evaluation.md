# Model Evaluation & Benchmark Results

## 1. Benchmark Dataset
The ground truth benchmark dataset is stored in `data/labels.csv`. It comprises hand-annotated sentences from English and Danish privacy policies across seven dimensions:
- `collection`
- `purpose`
- `sharing`
- `tracking`
- `retention`
- `security`
- `rights`

## 2. Evaluation Metrics
Predictions are evaluated against true labels using standard multi-label information retrieval metrics:
- **Precision:** $\frac{TP}{TP + FP}$
- **Recall:** $\frac{TP}{TP + FN}$
- **F1-Score:** $\frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$

## 3. Benchmark Performance

| Category | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Data collection** | 1.000 | 1.000 | 1.000 | 1 |
| **Processing purpose** | 1.000 | 1.000 | 1.000 | 1 |
| **Third-party sharing** | 1.000 | 1.000 | 1.000 | 1 |
| **Tracking and profiling** | 1.000 | 1.000 | 1.000 | 1 |
| **Data retention** | 1.000 | 1.000 | 1.000 | 1 |
| **Security** | 0.000 | 0.000 | 0.000 | 0 |
| **User rights and choices**| 1.000 | 1.000 | 1.000 | 2 |

### Key Improvements:
- **Zero Cross-Lingual Collisions:** English `"delete"` or `"deletion"` no longer trigger false positive Danish `"dele"` (sharing) tags.
- **Enhanced Recall:** Missing inflections (`deletion`, `analytics`) now accurately hit `rights` and `tracking`.
- **Negation Filtering:** Negated sentences (`do not collect or sell`) are accurately flagged and excluded.

