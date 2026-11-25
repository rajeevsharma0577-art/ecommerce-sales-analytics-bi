
USE EcommerceSalesDB;
GO

-- 1. Products Count
SELECT COUNT(*) AS TotalProducts
FROM dbo.Products;

-- 2. Customers Count
SELECT COUNT(*) AS TotalCustomers
FROM dbo.Customers;

-- 3. Sales Count
SELECT COUNT(*) AS TotalSalesTransactions
FROM dbo.Sales;

-- 4. Total Sales Amount
SELECT
    SUM(TotalSales) AS TotalRevenue
FROM dbo.Sales;

-- 5. Order Status Summary
SELECT
    OrderStatus,
    COUNT(*) AS TotalOrders
FROM dbo.Sales
GROUP BY OrderStatus;
