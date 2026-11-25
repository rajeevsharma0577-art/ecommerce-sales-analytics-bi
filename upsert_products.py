
import pandas as pd
import pyodbc
from pathlib import Path

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. Processed CSV
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv"

# 3. SQL Server configuration
SERVER = r"localhost\SQLEXPRESS"
DATABASE = "EcommerceSalesDB"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    print("Reading processed products...")

    df = pd.read_csv(CSV_FILE)
    df = df.astype(object).where(pd.notna(df), None)

    print("CSV Products:", len(df))

    with pyodbc.connect(connection_string) as connection:
        cursor = connection.cursor()

        inserted = 0
        updated = 0

        for row in df.itertuples(index=False, name=None):

            product_id = int(row[0])

            cursor.execute("""
                UPDATE dbo.Products
                SET
                    ProductName = ?,
                    Category = ?,
                    Price = ?,
                    DiscountPercentage = ?,
                    Rating = ?,
                    Stock = ?,
                    Brand = ?,
                    SKU = ?,
                    AvailabilityStatus = ?
                WHERE ProductID = ?
            """, (
                row[1], row[2], row[3], row[4],
                row[5], row[6], row[7], row[8],
                row[9], product_id
            ))

            if cursor.rowcount > 0:
                updated += 1
            else:
                cursor.execute("""
                    INSERT INTO dbo.Products
                    (
                        ProductID,
                        ProductName,
                        Category,
                        Price,
                        DiscountPercentage,
                        Rating,
                        Stock,
                        Brand,
                        SKU,
                        AvailabilityStatus
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    product_id,
                    row[1], row[2], row[3], row[4],
                    row[5], row[6], row[7], row[8], row[9]
                ))

                inserted += 1

        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM dbo.Products")
        total_products = cursor.fetchone()[0]

        print("\nPRODUCT UPSERT SUCCESSFUL!")
        print("Updated Products:", updated)
        print("Inserted Products:", inserted)
        print("Total SQL Products:", total_products)

except Exception as error:
    print("\nPRODUCT UPSERT FAILED!")
    print("Error:", error)
