
from pathlib import Path
import pandas as pd

file_path = Path("data") / "training_data.csv"
df = pd.read_csv(file_path)

print("--- Training Data Validation ---")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Check repeated traveler-destination pairs
pair_columns = ["traveler_id", "destination_id"]

pair_counts = df.groupby(pair_columns).size()
duplicate_pairs = pair_counts[pair_counts > 1]

print("\nRepeated traveler-destination pairs:", len(duplicate_pairs))

# Check pairs with conflicting labels
label_counts = (
    df.groupby(pair_columns)["accepted"]
    .nunique()
)

conflicting_pairs = label_counts[label_counts > 1]

print("Pairs with conflicting labels:", len(conflicting_pairs))

# Check missing values in questionnaire features
feature_columns = [
    "form_a", "form_b", "form_c", "form_f", "form_g",
    "form_h", "form_i", "form_j", "form_k",
    "form_r", "form_rr"
]

print("\nMissing values in questionnaire features:")
print(df[feature_columns].isna().sum())

print("\nMissing-value percentages:")
print((df[feature_columns].isna().mean() * 100).round(2))

print("\nValidation completed.")
