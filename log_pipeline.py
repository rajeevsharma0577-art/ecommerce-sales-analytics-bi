
import pyodbc

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
    with pyodbc.connect(connection_string) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM dbo.Products) +
                (SELECT COUNT(*) FROM dbo.Customers) +
                (SELECT COUNT(*) FROM dbo.Sales)
        """)

        total_records = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO dbo.Pipeline_Log
            (PipelineName, ExecutionStatus, RecordsProcessed)
            VALUES (?, ?, ?)
        """, "Ecommerce ETL", "COMPLETED", total_records)

        connection.commit()

        print("Pipeline Log Saved Successfully!")
        print("Total Database Records:", total_records)

except Exception as error:
    print("Pipeline Logging Failed:", error)
