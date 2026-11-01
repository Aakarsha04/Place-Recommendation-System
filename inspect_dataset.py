
from pathlib import Path
import pandas as pd

# 1. Define the file paths
project_folder = Path(__file__).parent
data_folder = project_folder / "data"

csv_path = data_folder / "Stravl_Travel_Preference_Data.csv"
mapping_path = data_folder / "destination_ids.txt"

# 2. Verify that both files exist
print("Checking dataset files...")

if not csv_path.exists():
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

if not mapping_path.exists():
    raise FileNotFoundError(f"Mapping file not found: {mapping_path}")

print("Both files were found successfully!")

# 3. Load the dataset
df = pd.read_csv(csv_path)

# 4. Display the dataset dimensions
print("\n--- Dataset Size ---")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# 5. Display the actual column names
print("\n--- Column Names ---")
print(df.columns.tolist())

# 6. Display the first five records
print("\n--- First Five Records ---")
print(df.head().to_string())

# 7. Check data types
print("\n--- Data Types ---")
print(df.dtypes.to_string())

# 8. Check missing values
print("\n--- Missing Values Per Column ---")
print(df.isnull().sum().to_string())

# 9. Check completely duplicated rows
print("\n--- Duplicate Records ---")
print("Number of duplicate rows:", df.duplicated().sum())

# 10. Inspect the destination mapping file
print("\n--- Destination Mapping Preview ---")
with open(mapping_path, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file):
        if line_number == 15:
            break
        print(line.rstrip("\n"))

print("\nDataset inspection completed.")


# Inspect the unique values in the questionnaire columns

questionnaire_columns = [
    "form_a", "form_b", "form_c",
    "form_f", "form_g", "form_h",
    "form_i", "form_j", "form_k"
]

for column in questionnaire_columns:
    print(f"\n--- {column} ---")
    print("Unique responses:")
    print(df[column].dropna().value_counts().head(10))


import ast

print("\n--- Swipe Data Inspection ---")

for column in ["yes_swipes", "no_swipes", "maybe_swipes"]:
    print(f"\n{column}:")
    print("First 3 values:")

    for value in df[column].head(3):
        print(value)

    def get_list_length(value):
        try:
            parsed = ast.literal_eval(value) if isinstance(value, str) else value
            return len(parsed) if isinstance(parsed, list) else 0
        except (ValueError, SyntaxError, TypeError):
            return 0

    lengths = df[column].apply(get_list_length)
    print("Average destinations per traveler:", round(lengths.mean(), 2))
    print("Maximum destinations for one traveler:", lengths.max())

    
from pathlib import Path

mapping_path = Path("data") / "destination_ids.txt"

with open(mapping_path, "r", encoding="utf-8") as file:
    destinations = file.read().splitlines()

print("\n--- Destination Mapping Inspection ---")
print("Total destination entries:", len(destinations))

print("\nFirst 5 entries:")
for index, destination in enumerate(destinations[:5]):
    print(index, "->", destination)

print("\nCheck destination ID 837:")
if len(destinations) > 837:
    print("Index 837:", destinations[837])
if len(destinations) >= 837:
    print("Index 836:", destinations[836])


import ast

print("\n--- Destination ID Validation ---")

for column in ["yes_swipes", "no_swipes", "maybe_swipes"]:
    all_ids = set()

    for value in df[column].dropna():
        try:
            parsed = ast.literal_eval(value) if isinstance(value, str) else value
            if isinstance(parsed, list):
                all_ids.update(
                    item for item in parsed
                    if isinstance(item, int)
                )
        except (ValueError, SyntaxError, TypeError):
            continue

    invalid_ids = sorted(
        item for item in all_ids
        if item < 0 or item >= len(destinations)
    )

    print(f"\n{column}:")
    print("Unique destination IDs:", len(all_ids))
    print("Invalid IDs:", len(invalid_ids))
    print("First 10 invalid IDs:", invalid_ids[:10])


