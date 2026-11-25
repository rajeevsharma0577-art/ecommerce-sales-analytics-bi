
import pandas as pd
from pathlib import Path

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. File locations
SALES_FILE = PROJECT_ROOT / "data" / "raw" / "sales_transactions_simulated.csv"
PRODUCT_FILE = PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv"
CUSTOMER_FILE = PROJECT_ROOT / "data" / "raw" / "customers_simulated.csv"

# 3. Load datasets
sales = pd.read_csv(SALES_FILE)
products = pd.read_csv(PRODUCT_FILE)
customers = pd.read_csv(CUSTOMER_FILE)

print("====================================")
print("SALES DATA QUALITY REPORT")
print("====================================")

# 4. Total records
print("\nTotal Sales Records:", len(sales))

# 5. Duplicate Order IDs
duplicates = sales["order_id"].duplicated().sum()
print("Duplicate Order IDs:", duplicates)

# 6. Missing values
missing = sales.isnull().sum().sum()
print("Total Missing Values:", missing)

# 7. Invalid quantity
invalid_quantity = (sales["quantity"] <= 0).sum()
print("Invalid Quantity:", invalid_quantity)

# 8. Invalid sales amount
invalid_sales = (sales["total_sales"] < 0).sum()
print("Invalid Sales Amount:", invalid_sales)

# 9. Sales calculation verification
expected_sales = (
    sales["gross_amount"] - sales["discount_amount"]
)

incorrect_calculations = (
    (sales["total_sales"] - expected_sales).abs() > 0.02
).sum()

print("Incorrect Sales Calculations:", incorrect_calculations)

# 10. Foreign key validation
invalid_products = (~sales["product_id"].isin(products["id"])).sum()
invalid_customers = (~sales["customer_id"].isin(customers["customer_id"])).sum()

print("Invalid Product References:", invalid_products)
print("Invalid Customer References:", invalid_customers)

# 11. Order status summary
print("\nOrder Status Summary:")
print(sales["order_status"].value_counts())

# 12. Total revenue
print("\nTotal Simulated Revenue:")
print(round(sales["total_sales"].sum(), 2))

# 13. Final validation
if all([
    duplicates == 0,
    missing == 0,
    invalid_quantity == 0,
    invalid_sales == 0,
    incorrect_calculations == 0,
    invalid_products == 0,
    invalid_customers == 0
]):
    print("\nDATA QUALITY STATUS: PASSED")
else:
    print("\nDATA QUALITY STATUS: ISSUES FOUND")

print("\nDATA SOURCE: SIMULATED")
print("====================================")
