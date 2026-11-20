
-- QUERY 02: TOP 10 PRODUCTS BY GROSS SALES
-- Group exact StockCode and Description values

USE EcommerceSales;
GO

WITH ProductGroups AS (
    SELECT
        MIN(StockCode) AS StockCode,
        MIN(Description) AS Description,
        CAST(SUM(Revenue) AS DECIMAL(18,2)) AS GrossSales,
        SUM(Quantity) AS UnitsSold

    FROM dbo.sales_clean

    WHERE StockCode NOT IN ('DOT', 'POST', 'M')

    GROUP BY
        CONVERT(VARBINARY(60), StockCode),
        CONVERT(VARBINARY(510), Description)
)

SELECT TOP 10
    StockCode,
    Description,
    GrossSales,
    UnitsSold

FROM ProductGroups

ORDER BY
    GrossSales DESC,
    StockCode,
    Description;
GO
