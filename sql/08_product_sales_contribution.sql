
-- QUERY 08: PRODUCT SALES CONTRIBUTION

USE EcommerceSales;
GO

-- 1. Tổng hợp doanh thu theo từng sản phẩm
WITH ProductSales AS (
    SELECT
        MIN(StockCode) AS StockCode,
        MIN(Description) AS Description,
        SUM(Revenue) AS GrossSales,
        SUM(Quantity) AS UnitsSold

    FROM dbo.sales_clean

    -- Loại các mã phí và điều chỉnh đã xác định
    WHERE CONVERT(VARBINARY(60), StockCode) NOT IN (
    CONVERT(VARBINARY(60), N'DOT'),
    CONVERT(VARBINARY(60), N'POST'),
    CONVERT(VARBINARY(60), N'M')
)

    -- Nhóm chính xác như Query 2
    GROUP BY
        CONVERT(VARBINARY(60), StockCode),
        CONVERT(VARBINARY(510), Description)
),

-- 2. Xếp hạng và tính tổng doanh thu
RankedProducts AS (
    SELECT
        StockCode,
        Description,
        GrossSales,
        UnitsSold,

        ROW_NUMBER() OVER (
            ORDER BY GrossSales DESC,
                     StockCode, Description
        ) AS ProductRank,

        SUM(GrossSales) OVER ()
            AS TotalProductGrossSales

    FROM ProductSales
)

-- 3. Tính tỷ trọng doanh thu
SELECT
    ProductRank,
    StockCode,
    Description,

    CAST(
        GrossSales AS DECIMAL(18,2)
    ) AS GrossSales,

    UnitsSold,

    CAST(
        TotalProductGrossSales AS DECIMAL(18,2)
    ) AS TotalProductGrossSales,

    CAST(
        GrossSales * 100.0 /
        NULLIF(TotalProductGrossSales, 0)
        AS DECIMAL(10,2)
    ) AS RevenueSharePct,

    CAST(
        SUM(GrossSales) OVER (
            ORDER BY ProductRank
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) * 100.0 /
        NULLIF(TotalProductGrossSales, 0)
        AS DECIMAL(10,2)
    ) AS CumulativeSharePct

FROM RankedProducts

WHERE ProductRank <= 10

ORDER BY ProductRank;
GO
