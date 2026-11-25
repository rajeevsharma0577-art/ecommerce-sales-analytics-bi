
import pandas as pd
from pathlib import Path

# 1. Project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. File paths
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_clean.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv"

print("Starting Product Data Cleaning...")

# 3. Read CSV
df = pd.read_csv(INPUT_FILE)

print("\nRecords Before Cleaning:", len(df))

# 4. Handle missing brand values
df["brand"] = df["brand"].fillna("Unknown")

# 5. Remove duplicate Product IDs
df = df.drop_duplicates(subset=["id"])

# 6. Correct data types
df["id"] = df["id"].astype("int64")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["stock"] = pd.to_numeric(df["stock"], errors="coerce")

# 7. Check missing values again
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# 8. Save cleaned data
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\nRecords After Cleaning:", len(df))
print("Missing Brands:", (df["brand"] == "Unknown").sum())

print("\nDATA CLEANING COMPLETED!")
print("Saved File:", OUTPUT_FILE)
