-- Read-only reconciliation. Run after importing, or on an existing project database.
USE EcommerceSales;
GO
SELECT COUNT_BIG(*) AS SalesRows,
       COUNT(DISTINCT InvoiceNo) AS TotalOrders,
       COUNT(DISTINCT CustomerID) AS IdentifiedCustomers,
       SUM(CAST(Quantity AS BIGINT)) AS UnitsSold,
       CAST(SUM(Revenue) AS DECIMAL(19,2)) AS GrossSalesGBP,
       CAST(SUM(Revenue) / NULLIF(COUNT(DISTINCT InvoiceNo),0) AS DECIMAL(19,2)) AS AOV_GBP,
       MIN(InvoiceDate) AS FirstInvoice, MAX(InvoiceDate) AS LastInvoice
FROM dbo.sales_clean;
-- Expected: 530104 | 19960 | 4338 | 5588376 | 10666684.54 | 534.40

SELECT Country, COUNT(DISTINCT InvoiceNo) AS Orders,
       COUNT(DISTINCT CustomerID) AS Customers, SUM(CAST(Quantity AS BIGINT)) AS UnitsSold,
       CAST(SUM(Revenue) AS DECIMAL(19,2)) AS GrossSalesGBP,
       CAST(SUM(Revenue)/NULLIF(COUNT(DISTINCT InvoiceNo),0) AS DECIMAL(19,2)) AS AOV_GBP
FROM dbo.sales_clean
WHERE Country IN (N'United Kingdom',N'Germany')
GROUP BY Country;
-- UK: 18019 | 3920 | 4662390 | 9025222.08 | 500.87
-- Germany: 457 | 94 | 119261 | 228867.14 | 500.80

SELECT YearMonth, ActiveCustomers, NewCustomers, ReturningCustomers,
       CAST(100.0*ReturningCustomers/NULLIF(ActiveCustomers,0) AS DECIMAL(10,2)) AS ReturningSharePct
FROM dbo.vw_monthly_customer_activity ORDER BY YearMonth;
-- November 2011: 1664 | 323 | 1341 | 80.59
-- This share is NOT a cohort retention rate.
GO
