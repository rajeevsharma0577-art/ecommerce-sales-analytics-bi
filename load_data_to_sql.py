
import pandas as pd
import pyodbc
from pathlib import Path
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 1. Project location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2. SQL Server configuration
SERVER = r"localhost\SQLEXPRESS"
DATABASE = "EcommerceSalesDB"

# 3. Database connection
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

# 4. SQLAlchemy engine
encoded_connection = quote_plus(connection_string)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={encoded_connection}"
)

# 5. CSV file paths
datasets = {
    "Products": PROJECT_ROOT / "data" / "processed" / "products_cleaned.csv",
    "Customers": PROJECT_ROOT / "data" / "processed" / "customers_processed.csv",
    "Sales": PROJECT_ROOT / "data" / "processed" / "sales_processed.csv"
}

# 6. Load datasets into SQL Server
try:
    with engine.begin() as connection:

        for table_name, file_path in datasets.items():

            print(f"\nLoading {table_name}...")

            df = pd.read_csv(file_path)

            # Rename columns to match SQL tables
            if table_name == "Products":
                df = df.rename(columns={
                    "id": "ProductID",
                    "title": "ProductName",
                    "category": "Category",
                    "price": "Price",
                    "discountPercentage": "DiscountPercentage",
                    "rating": "Rating",
                    "stock": "Stock",
                    "brand": "Brand",
                    "sku": "SKU",
                    "availabilityStatus": "AvailabilityStatus"
                })

            elif table_name == "Customers":
                df = df.rename(columns={
                    "customer_id": "CustomerID",
                    "customer_name": "CustomerName",
                    "email": "Email",
                    "city": "City",
                    "state": "State",
                    "country": "Country",
                    "customer_type": "CustomerType",
                    "data_source": "DataSource"
                })

            elif table_name == "Sales":
                df = df.rename(columns={
                    "order_id": "OrderID",
                    "order_date": "OrderDate",
                    "customer_id": "CustomerID",
                    "product_id": "ProductID",
                    "product_name": "ProductName",
                    "category": "Category",
                    "quantity": "Quantity",
                    "unit_price": "UnitPrice",
                    "discount_percentage": "DiscountPercentage",
                    "gross_amount": "GrossAmount",
                    "discount_amount": "DiscountAmount",
                    "total_sales": "TotalSales",
                    "payment_method": "PaymentMethod",
                    "order_status": "OrderStatus",
                    "data_source": "DataSource"
                })

                df["OrderDate"] = pd.to_datetime(
                    df["OrderDate"]
                )

            # Load data
            df.to_sql(
                name=table_name,
                con=connection,
                schema="dbo",
                if_exists="append",
                index=False,
                chunksize=500
            )

            print(f"{table_name} Loaded: {len(df)} records")

    print("\nALL DATASETS LOADED SUCCESSFULLY!")
    # Log successful ETL execution
    with engine.begin() as connection:

        result = connection.execute(text("""
            SELECT
                (SELECT COUNT(*) FROM dbo.Products) +
                (SELECT COUNT(*) FROM dbo.Customers) +
                (SELECT COUNT(*) FROM dbo.Sales)
        """))

        total_records = result.scalar()

        connection.execute(text("""
            INSERT INTO dbo.Pipeline_Log
            (PipelineName, ExecutionStatus, RecordsProcessed)
            VALUES
            ('Ecommerce ETL', 'COMPLETED', :records)
        """), {"records": total_records})

    print("ETL Pipeline Log Saved Successfully!")

except Exception as error:
    print("\nDATA LOADING FAILED!")
    print("Error:", error)

finally:
    engine.dispose()
