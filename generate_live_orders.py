
import pyodbc
import random
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# SQL Server connection
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=EcommerceSalesDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def generate_orders():

    connection = pyodbc.connect(CONNECTION_STRING)
    cursor = connection.cursor()

    try:
        # Fetch existing customers
        cursor.execute("""
            SELECT CustomerID
            FROM dbo.Customers
        """)
        customers = [row[0] for row in cursor.fetchall()]

        # Fetch existing products
        cursor.execute("""
            SELECT ProductID, ProductName, Category,
                   Price, DiscountPercentage
            FROM dbo.Products
            WHERE Price IS NOT NULL
        """)
        products = cursor.fetchall()

        if not customers or not products:
            raise Exception("Customers or Products table is empty.")

        # Find highest existing numeric OrderID
        cursor.execute("""
            SELECT MAX(TRY_CONVERT(INT, SUBSTRING(OrderID, 4, 27)))
            FROM dbo.Sales
            WHERE OrderID LIKE 'ORD%'
        """)
        max_order_number = cursor.fetchone()[0] or 0

        # Generate 3 to 5 new orders
        number_of_orders = random.randint(3, 5)

        payment_methods = [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Cash on Delivery"
        ]

        order_statuses = [
            "Delivered",
            "Shipped",
            "Pending",
            "Cancelled"
        ]

        orders = []

        for i in range(number_of_orders):

            customer_id = random.choice(customers)
            product = random.choice(products)

            product_id = product.ProductID
            product_name = product.ProductName
            category = product.Category
            unit_price = money(product.Price)

            discount_percentage = money(
                product.DiscountPercentage or 0
            )

            quantity = random.randint(1, 5)

            gross_amount = money(unit_price * quantity)

            discount_amount = money(
                gross_amount * discount_percentage / Decimal("100")
            )

            total_sales = money(
                gross_amount - discount_amount
            )

            order_id = (
                f"ORD{max_order_number + i + 1:06d}"
            )

            orders.append((
                order_id,
                datetime.now(),
                customer_id,
                product_id,
                product_name,
                category,
                quantity,
                unit_price,
                discount_percentage,
                gross_amount,
                discount_amount,
                total_sales,
                random.choice(payment_methods),
                random.choice(order_statuses),
                "SYNTHETIC_LIVE"
            ))

        # Insert only new records
        cursor.executemany("""
            INSERT INTO dbo.Sales (
                OrderID,
                OrderDate,
                CustomerID,
                ProductID,
                ProductName,
                Category,
                Quantity,
                UnitPrice,
                DiscountPercentage,
                GrossAmount,
                DiscountAmount,
                TotalSales,
                PaymentMethod,
                OrderStatus,
                DataSource
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, orders)

        connection.commit()

        print("\nLIVE TRANSACTION GENERATION SUCCESSFUL!")
        print("New Orders Generated:", number_of_orders)

        for order in orders:
            print(
                f"Order: {order[0]} | "
                f"Customer: {order[2]} | "
                f"Product: {order[4]} | "
                f"Revenue: {order[11]}"
            )

        cursor.execute("SELECT COUNT(*) FROM dbo.Sales")
        total_sales_records = cursor.fetchone()[0]

        print("\nTotal SQL Sales Records:", total_sales_records)

    except Exception as error:

        connection.rollback()
        print("\nTRANSACTION GENERATION FAILED!")
        print("Error:", error)
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    generate_orders()
