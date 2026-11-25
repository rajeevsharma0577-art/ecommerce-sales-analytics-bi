
import pandas as pd
from pathlib import Path

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. Input and output paths
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "customers_simulated.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "customers_processed.csv"

print("Starting Customer Data Processing...")

# 3. Read raw customer data
df = pd.read_csv(INPUT_FILE)

print("\nRecords Before Processing:", len(df))

# 4. Remove duplicate customer IDs
df = df.drop_duplicates(subset=["customer_id"])

# 5. Clean text columns
text_columns = [
    "customer_name",
    "email",
    "city",
    "state",
    "country",
    "customer_type",
    "data_source"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# 6. Standardize customer type
df["customer_type"] = df["customer_type"].str.title()

# 7. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 8. Save processed customer data
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# 9. Display summary
print("\nCUSTOMER PROCESSING COMPLETED!")
print("--------------------------------")

print("Total Customers:", len(df))
print("Unique Customer IDs:", df["customer_id"].nunique())

print("\nCustomer Type Summary:")
print(df["customer_type"].value_counts())

print("\nProcessed File Saved:")
print(OUTPUT_FILE)

print("\nDATA SOURCE: SIMULATED")
