
import json
import pandas as pd
from pathlib import Path

# 1. Project folder location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. Input and output file paths
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "products_raw.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_clean.csv"

print("Reading Raw JSON Data...")

# 3. Load JSON data
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# 4. Extract product records
products = data["products"]

# 5. Convert JSON into Pandas DataFrame
df = pd.DataFrame(products)

print("\nDataFrame Created Successfully!")

# 6. Select required business columns
columns_to_keep = [
    "id",
    "title",
    "category",
    "price",
    "discountPercentage",
    "rating",
    "stock",
    "brand",
    "sku",
    "availabilityStatus"
]

df = df[columns_to_keep].copy()

# 7. Save as CSV
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

# 8. Display results
print("\nFirst 5 Products:")
print(df.head())

print("\nDataFrame Information:")
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())

print("\nCSV File Saved Successfully!")
print(OUTPUT_FILE)
