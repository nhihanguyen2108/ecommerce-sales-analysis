
-- QUERY 06: YEARLY SALES ANALYSIS

USE EcommerceSales;
GO

SELECT
    [Year],

    -- Tổng Gross Sales mỗi năm
    CAST(
        SUM(Revenue) AS DECIMAL(18,2)
    ) AS GrossSales,

    -- Số hóa đơn duy nhất
    COUNT(DISTINCT InvoiceNo) AS Orders,

    -- Số khách hàng xác định được
    COUNT(DISTINCT CustomerID) AS Customers,

    -- Tổng số lượng sản phẩm
    SUM(Quantity) AS UnitsSold,

    -- Giá trị trung bình mỗi hóa đơn
    CAST(
        SUM(Revenue) /
        NULLIF(COUNT(DISTINCT InvoiceNo), 0)
        AS DECIMAL(18,2)
    ) AS AOV

FROM dbo.sales_clean

GROUP BY [Year]

ORDER BY [Year];
GO
