
-- QUERY 05: MONTH-OVER-MONTH SALES GROWTH

USE EcommerceSales;
GO

WITH MonthlySales AS (
    -- 1. Tính doanh thu theo tháng
    SELECT
        YearMonth,
        SUM(Revenue) AS GrossSales
    FROM dbo.sales_clean
    GROUP BY YearMonth
),

MonthlyComparison AS (
    -- 2. Lấy doanh thu tháng trước
    SELECT
        YearMonth,
        GrossSales,

        LAG(GrossSales) OVER (
            ORDER BY YearMonth
        ) AS PreviousRevenue

    FROM MonthlySales
)

-- 3. Tính tăng trưởng theo tháng
SELECT
    YearMonth,

    CAST(
        GrossSales AS DECIMAL(18,2)
    ) AS GrossSales,

    CAST(
        PreviousRevenue AS DECIMAL(18,2)
    ) AS PreviousRevenue,

    CAST(
        GrossSales - PreviousRevenue
        AS DECIMAL(18,2)
    ) AS RevenueChange,

    CAST(
        (GrossSales - PreviousRevenue) * 100.0
        / NULLIF(PreviousRevenue, 0)
        AS DECIMAL(18,2)
    ) AS MoM_Growth_Pct

FROM MonthlyComparison

ORDER BY YearMonth;
GO
