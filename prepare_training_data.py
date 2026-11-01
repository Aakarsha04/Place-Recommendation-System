
import ast
from pathlib import Path

import pandas as pd

# File paths
DATA_DIR = Path("data")
INPUT_FILE = DATA_DIR / "Stravl_Travel_Preference_Data.csv"
MAPPING_FILE = DATA_DIR / "destination_ids.txt"
OUTPUT_FILE = DATA_DIR / "training_data.csv"

# Load the original data and destination names
df = pd.read_csv(INPUT_FILE)

with open(MAPPING_FILE, "r", encoding="utf-8") as file:
    destinations = file.read().splitlines()


def parse_list(value):
    """Convert a stored list string into a Python list."""
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    try:
        result = ast.literal_eval(value)
        return result if isinstance(result, list) else []
    except (ValueError, SyntaxError, TypeError):
        return []


# Questionnaire fields used as traveler features
feature_columns = [
    "form_a", "form_b", "form_c", "form_f", "form_g",
    "form_h", "form_i", "form_j", "form_k",
    "form_r", "form_rr"
]

records = []

for _, row in df.iterrows():
    traveler_id = row["id"]

    for swipe_column, label in [
        ("yes_swipes", 1),
        ("no_swipes", 0),
    ]:
        destination_ids = parse_list(row[swipe_column])

        for destination_id in destination_ids:
            if not isinstance(destination_id, int):
                continue

            if not 0 <= destination_id < len(destinations):
                continue

            record = {
                "traveler_id": traveler_id,
                "destination_id": destination_id,
                "destination": destinations[destination_id],
                "accepted": label,
            }

            for column in feature_columns:
                record[column] = row[column]

            records.append(record)

# Save a separate training dataset
training_df = pd.DataFrame(records)
training_df.to_csv(OUTPUT_FILE, index=False)

print("Training data preparation completed.")
print("Output file:", OUTPUT_FILE)
print("Total training examples:", len(training_df))
print("\nLabel counts:")
print(training_df["accepted"].value_counts().sort_index())
print("\nFirst 5 rows:")
print(training_df.head())
