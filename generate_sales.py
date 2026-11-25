
import pandas as pd
import random
from faker import Faker
from pathlib import Path
from datetime import datetime

# Fixed seed for reproducible results
random.seed(42)
fake = Faker("en_IN")
Faker.seed(42)

# 1. Project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. Input product file
PRODUCT_FILE = PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv"

# 3. Output files
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

SALES_FILE = RAW_FOLDER / "sales_transactions_simulated.csv"
CUSTOMER_FILE = RAW_FOLDER / "customers_simulated.csv"

# 4. Load product master
products_df = pd.read_csv(PRODUCT_FILE)

print("Generating Simulated E-Commerce Data...")

# 5. Generate 500 customers
customers = []

for i in range(1, 501):
    customers.append({
        "customer_id": f"CUST{i:05d}",
        "customer_name": fake.name(),
        "email": f"customer{i}@example.com",
        "city": fake.city(),
        "state": fake.state(),
        "country": "India",
        "customer_type": random.choice(
            ["New", "Returning"]
        ),
        "data_source": "SIMULATED"
    })

customers_df = pd.DataFrame(customers)

# 6. Generate 5000 sales transactions
sales = []

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 11, 22)

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Cancelled",
    "Returned"
]

for i in range(1, 5001):

    # Select random customer
    customer = random.choice(customers)

    # Select random product
    product = products_df.sample(
        n=1,
        random_state=random.randint(1, 100000)
    ).iloc[0]

    # Transaction details
    quantity = random.randint(1, 5)
    unit_price = round(float(product["price"]), 2)
    discount = round(random.uniform(0, 20), 2)

    gross_amount = quantity * unit_price

    discount_amount = gross_amount * discount / 100

    total_sales = round(
        gross_amount - discount_amount, 2
    )

    order_date = fake.date_time_between(
        start_date=start_date,
        end_date=end_date
    )

    sales.append({
        "order_id": f"ORD{i:06d}",
        "order_date": order_date,
        "customer_id": customer["customer_id"],
        "product_id": int(product["id"]),
        "product_name": product["title"],
        "category": product["category"],
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_percentage": discount,
        "gross_amount": round(gross_amount, 2),
        "discount_amount": round(discount_amount, 2),
        "total_sales": total_sales,
        "payment_method": random.choice(payment_methods),
        "order_status": random.choice(order_statuses),
        "data_source": "SIMULATED"
    })

# 7. Convert into DataFrames
sales_df = pd.DataFrame(sales)

# 8. Save CSV files
customers_df.to_csv(
    CUSTOMER_FILE,
    index=False,
    encoding="utf-8-sig"
)

sales_df.to_csv(
    SALES_FILE,
    index=False,
    encoding="utf-8-sig"
)

# 9. Display summary
print("\nSIMULATED DATA GENERATION SUCCESSFUL!")
print("--------------------------------------")

print("Total Customers:", len(customers_df))
print("Total Transactions:", len(sales_df))

print(
    "Total Simulated Sales:",
    round(sales_df["total_sales"].sum(), 2)
)

print("\nOrder Status Summary:")
print(sales_df["order_status"].value_counts())

print("\nGenerated Files:")
print(CUSTOMER_FILE)
print(SALES_FILE)

print("\nDATA SOURCE: SIMULATED")
