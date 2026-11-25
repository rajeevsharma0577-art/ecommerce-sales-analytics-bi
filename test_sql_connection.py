
import pyodbc

# 1. SQL Server connection details
SERVER = r"localhost\SQLEXPRESS"
DATABASE = "EcommerceSalesDB"

# 2. Check installed ODBC drivers
drivers = pyodbc.drivers()

print("Available SQL Server Drivers:")
print(drivers)

# 3. Select installed SQL Server driver
available_drivers = [
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
    "SQL Server"
]

driver = next(
    (d for d in available_drivers if d in drivers),
    None
)

if driver is None:
    raise Exception(
        "SQL Server ODBC Driver not found. "
        "Please install Microsoft ODBC Driver 17 or 18."
    )

# 4. Build connection string
connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

# 5. Connect to SQL Server
try:
    connection = pyodbc.connect(
        connection_string,
        timeout=10
    )

    print("\nSQL SERVER CONNECTION SUCCESSFUL!")

    # 6. Verify database connection
    cursor = connection.cursor()

    cursor.execute("SELECT DB_NAME(), @@SERVERNAME")

    result = cursor.fetchone()

    print("Database Name:", result[0])
    print("Server Name:", result[1])

    cursor.close()
    connection.close()

    print("\nConnection Closed Successfully!")

except pyodbc.Error as error:
    print("\nSQL SERVER CONNECTION FAILED!")
    print(error)
