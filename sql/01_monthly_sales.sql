
-- QUERY 01: MONTHLY SALES ANALYSIS

USE EcommerceSales;
GO

SELECT
    YearMonth,

    -- Tổng doanh thu theo tháng
    CAST(
        SUM(Revenue) AS DECIMAL(18,2)
    ) AS GrossSales,

    -- Số hóa đơn duy nhất
    COUNT(DISTINCT InvoiceNo) AS Orders,

    -- Tổng số lượng bán
    SUM(Quantity) AS UnitsSold,

    -- Giá trị trung bình mỗi hóa đơn
    CAST(
        SUM(Revenue) /
        NULLIF(COUNT(DISTINCT InvoiceNo), 0)
        AS DECIMAL(18,2)
    ) AS AOV

FROM dbo.sales_clean

GROUP BY YearMonth

ORDER BY YearMonth;
GO
