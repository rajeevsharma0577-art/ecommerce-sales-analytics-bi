
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import pyodbc

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"

# SQL Server connection
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=EcommerceSalesDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

PIPELINE_STEPS = [
    "fetch_products.py",
    "process_products.py",
    "upsert_products.py"
]


def save_pipeline_log(status, records_processed, start_time):

    try:
        connection = pyodbc.connect(CONNECTION_STRING)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO dbo.Pipeline_Log
            (PipelineName, ExecutionStatus, RecordsProcessed)
            VALUES (?, ?, ?)
        """, "Ecommerce Product ETL", status, records_processed)

        connection.commit()
        cursor.close()
        connection.close()

        print(f"SQL Pipeline Log Saved: {status}")

    except Exception as error:
        print("Pipeline Log Error:", error)


def get_product_count():

    connection = pyodbc.connect(CONNECTION_STRING)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM dbo.Products")
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count


def run_pipeline():

    start_time = datetime.now()

    print("=" * 55)
    print(" E-COMMERCE PRODUCT ETL PIPELINE STARTED")
    print("=" * 55)

    try:

        for script in PIPELINE_STEPS:

            script_path = SCRIPTS_DIR / script

            print(f"\nRunning: {script}")
            print("-" * 55)

            subprocess.run(
                [sys.executable, str(script_path)],
                check=True
            )

            print(f"\nSUCCESS: {script}")

        records_processed = get_product_count()

        save_pipeline_log(
            "COMPLETED",
            records_processed,
            start_time
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 55)
        print(" PRODUCT ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"Products in SQL: {records_processed}")
        print(f"Total Duration: {duration:.2f} seconds")
        print("=" * 55)

    except Exception as error:

        print("\nPIPELINE FAILED!")
        print("Error:", error)

        save_pipeline_log("FAILED", 0, start_time)

        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
