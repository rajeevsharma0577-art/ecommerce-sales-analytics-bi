CREATE TABLE Pipeline_Log (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    PipelineName VARCHAR(100),
    ExecutionStatus VARCHAR(30),
    RecordsProcessed INT,
    ExecutionDate DATETIME DEFAULT GETDATE()
);



USE EcommerceSalesDB;
GO

-- 1. Sales table columns and data types
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME IN ('Sales', 'Customers', 'Products')
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- 2. Primary keys and foreign keys
SELECT
    OBJECT_NAME(parent_object_id) AS TableName,
    name AS ConstraintName,
    type_desc AS ConstraintType
FROM sys.objects
WHERE type IN ('PK', 'F', 'UQ')
  AND parent_object_id IN (
      OBJECT_ID('dbo.Sales'),
      OBJECT_ID('dbo.Customers'),
      OBJECT_ID('dbo.Products')
  )
ORDER BY TableName, ConstraintType;



USE EcommerceSalesDB;
GO

-- Complete Sales table structure
SELECT
    c.column_id,
    c.name AS ColumnName,
    TYPE_NAME(c.user_type_id) AS DataType,
    c.max_length,
    c.precision,
    c.scale,
    c.is_nullable,
    c.is_identity
FROM sys.columns c
WHERE c.object_id = OBJECT_ID('dbo.Sales')
ORDER BY c.column_id;

-- Primary key column
SELECT
    c.name AS PrimaryKeyColumn
FROM sys.indexes i
JOIN sys.index_columns ic
    ON i.object_id = ic.object_id
    AND i.index_id = ic.index_id
JOIN sys.columns c
    ON ic.object_id = c.object_id
    AND ic.column_id = c.column_id
WHERE i.object_id = OBJECT_ID('dbo.Sales')
AND i.is_primary_key = 1;



USE EcommerceSalesDB;
GO

-- Remaining Sales columns
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Sales'
  AND ORDINAL_POSITION > 12
ORDER BY ORDINAL_POSITION;

-- Customer IDs for valid foreign keys
SELECT TOP 10
    CustomerID
FROM dbo.Customers
ORDER BY CustomerID;

-- Product IDs for valid foreign keys
SELECT TOP 10
    ProductID,
    ProductName,
    Price,
    Category
FROM dbo.Products
ORDER BY ProductID;



USE EcommerceSalesDB;
GO

SELECT TOP 10
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
FROM dbo.Sales
ORDER BY OrderDate DESC;




USE EcommerceSalesDB;
GO

-- Verify latest generated orders
SELECT TOP 10
    OrderID,
    OrderDate,
    CustomerID,
    ProductName,
    Quantity,
    TotalSales,
    OrderStatus,
    DataSource
FROM dbo.Sales
ORDER BY OrderDate DESC;

-- Verify total records and revenue
SELECT
    COUNT(*) AS TotalOrders,
    SUM(TotalSales) AS TotalRevenue,
    SUM(Quantity) AS TotalQuantity
FROM dbo.Sales;
