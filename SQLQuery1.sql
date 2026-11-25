
USE EcommerceSalesDB;
GO

-- 1. PRODUCTS TABLE
IF OBJECT_ID('dbo.Products', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Products
    (
        ProductID INT PRIMARY KEY,
        ProductName NVARCHAR(500) NOT NULL,
        Category NVARCHAR(100),
        Price DECIMAL(12,2),
        DiscountPercentage DECIMAL(8,2),
        Rating DECIMAL(4,2),
        Stock INT,
        Brand NVARCHAR(200),
        SKU NVARCHAR(100),
        AvailabilityStatus NVARCHAR(100)
    );
END;
GO

-- 2. CUSTOMERS TABLE
IF OBJECT_ID('dbo.Customers', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Customers
    (
        CustomerID VARCHAR(20) PRIMARY KEY,
        CustomerName NVARCHAR(200),
        Email VARCHAR(255),
        City NVARCHAR(150),
        State NVARCHAR(150),
        Country NVARCHAR(100),
        CustomerType VARCHAR(50),
        DataSource VARCHAR(50)
    );
END;
GO

-- 3. SALES TABLE
IF OBJECT_ID('dbo.Sales', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Sales
    (
        OrderID VARCHAR(30) PRIMARY KEY,
        OrderDate DATETIME2,
        CustomerID VARCHAR(20) NOT NULL,
        ProductID INT NOT NULL,
        ProductName NVARCHAR(500),
        Category NVARCHAR(100),
        Quantity INT NOT NULL,
        UnitPrice DECIMAL(12,2),
        DiscountPercentage DECIMAL(8,2),
        GrossAmount DECIMAL(14,2),
        DiscountAmount DECIMAL(14,2),
        TotalSales DECIMAL(14,2),
        PaymentMethod VARCHAR(100),
        OrderStatus VARCHAR(50),
        DataSource VARCHAR(50),

        CONSTRAINT FK_Sales_Customers
        FOREIGN KEY (CustomerID)
        REFERENCES dbo.Customers(CustomerID),

        CONSTRAINT FK_Sales_Products
        FOREIGN KEY (ProductID)
        REFERENCES dbo.Products(ProductID),

        CONSTRAINT CHK_Sales_Quantity
        CHECK (Quantity > 0)
    );
END;
GO

PRINT 'ALL THREE TABLES CREATED SUCCESSFULLY!';
GO
