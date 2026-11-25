
import pandas as pd
from pathlib import Path

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. Read processed CSV
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("===================================")
print("PRODUCT DATA QUALITY REPORT")
print("===================================")

# 3. Total records
print("\nTotal Records:", len(df))

# 4. Missing values check
print("\nMissing Values:")
print(df.isnull().sum())

# 5. Duplicate Product ID check
duplicate_ids = df["id"].duplicated().sum()
print("\nDuplicate Product IDs:", duplicate_ids)

# 6. Invalid price check
invalid_prices = (df["price"] <= 0).sum()
print("Invalid Prices:", invalid_prices)

# 7. Invalid stock check
invalid_stock = (df["stock"] < 0).sum()
print("Invalid Stock:", invalid_stock)

# 8. Data types
print("\nColumn Data Types:")
print(df.dtypes)

# 9. Overall validation status
if (
    df.isnull().sum().sum() == 0
    and duplicate_ids == 0
    and invalid_prices == 0
    and invalid_stock == 0
):
    print("\nDATA QUALITY STATUS: PASSED")
else:
    print("\nDATA QUALITY STATUS: ISSUES FOUND")

print("\n===================================")
