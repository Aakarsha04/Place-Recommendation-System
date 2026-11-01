
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
INPUT_FILE = DATA_DIR / "training_data.csv"
OUTPUT_FILE = DATA_DIR / "clean_training_data.csv"

df = pd.read_csv(INPUT_FILE)

pair_columns = ["traveler_id", "destination_id"]

print("--- Cleaning Training Data ---")
print("Original rows:", len(df))

# Find pairs that have both accepted and rejected labels
label_counts = df.groupby(pair_columns)["accepted"].nunique()
conflicting_pairs = (
    label_counts[label_counts > 1]
    .reset_index()[pair_columns]
)
print("Conflicting pairs found:", len(conflicting_pairs))

# Remove all records belonging to conflicting pairs
df = df.merge(
    conflicting_pairs.assign(conflict=True),
    on=pair_columns,
    how="left"
)

df = df[df["conflict"].isna()].drop(columns="conflict")
print("Rows after removing conflicts:", len(df))

# Keep one record per traveler-destination pair
df = df.drop_duplicates(subset=pair_columns, keep="first")
print("Rows after removing duplicate pairs:", len(df))

# Drop questionnaire columns with very high missingness
df = df.drop(columns=["form_r", "form_rr"])

# Preserve missing responses explicitly for later encoding
feature_columns = [
    "form_a", "form_b", "form_c", "form_f", "form_g",
    "form_h", "form_i", "form_j", "form_k"
]
df[feature_columns] = df[feature_columns].fillna("missing")

df.to_csv(OUTPUT_FILE, index=False)

print("\nClean dataset saved to:", OUTPUT_FILE)
print("Final rows:", len(df))
print("\nLabel counts:")
print(df["accepted"].value_counts().sort_index())
print("\nRemaining missing values in questionnaire features:")
print(df[feature_columns].isna().sum())
