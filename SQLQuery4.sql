SELECT TOP 10
    LogID,
    PipelineName,
    ExecutionStatus,
    RecordsProcessed,
    ExecutionDate
FROM dbo.Pipeline_Log
ORDER BY LogID DESC;

SELECT
    MIN(OrderDate) AS First_Order_Date,
    MAX(OrderDate) AS Last_Order_Date,
    COUNT(DISTINCT CAST(OrderDate AS DATE)) AS Unique_Dates,
    COUNT(DISTINCT YEAR(OrderDate)) AS Unique_Years
FROM dbo.Sales;

SELECT TOP 10 *
FROM dbo.Pipeline_Log
ORDER BY LogID DESC;

SELECT TOP 5 *
FROM dbo.Pipeline_Log
ORDER BY LogID DESC;

SELECT TOP 10
    LogID,
    PipelineName,
    ExecutionStatus,
    RecordsProcessed,
    ExecutionDate
FROM dbo.Pipeline_Log
ORDER BY LogID DESC;