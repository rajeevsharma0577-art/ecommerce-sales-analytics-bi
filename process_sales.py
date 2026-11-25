
import pandas as pd
from pathlib import Path

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. Input and output paths
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "sales_transactions_simulated.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "sales_processed.csv"

print("Starting Sales Data Processing...")

# 3. Load raw sales data
df = pd.read_csv(INPUT_FILE)

print("\nRecords Before Processing:", len(df))

# 4. Convert order_date into datetime
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

# 5. Convert numeric columns
numeric_columns = [
    "quantity",
    "unit_price",
    "discount_percentage",
    "gross_amount",
    "discount_amount",
    "total_sales"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# 6. Remove duplicate order IDs
df = df.drop_duplicates(subset=["order_id"])

# 7. Sort records by order date
df = df.sort_values("order_date")

# 8. Reset index
df = df.reset_index(drop=True)

# 9. Save processed data
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# 10. Processing summary
print("\nPROCESSING COMPLETED!")
print("--------------------------------")

print("Total Records:", len(df))
print("Missing Dates:", df["order_date"].isnull().sum())
print("Total Sales:", round(df["total_sales"].sum(), 2))

print("\nColumn Data Types:")
print(df.dtypes)

print("\nProcessed File Saved:")
print(OUTPUT_FILE)

print("\nDATA SOURCE: SIMULATED")
