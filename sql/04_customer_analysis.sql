
-- QUERY 04: TOP 10 CUSTOMERS BY GROSS SALES

USE EcommerceSales;
GO

SELECT TOP 10
    CustomerID,

    -- Tổng doanh thu từng khách hàng
    CAST(
        SUM(Revenue) AS DECIMAL(18,2)
    ) AS GrossSales,

    -- Số hóa đơn duy nhất
    COUNT(DISTINCT InvoiceNo) AS Orders,

    -- Tổng số lượng sản phẩm đã mua
    SUM(Quantity) AS UnitsSold,

    -- Lần mua gần nhất
    MAX(InvoiceDate) AS LastPurchase,

    -- Giá trị trung bình mỗi hóa đơn
    CAST(
        SUM(Revenue) /
        NULLIF(COUNT(DISTINCT InvoiceNo), 0)
        AS DECIMAL(18,2)
    ) AS AOV

FROM dbo.sales_clean

-- Chỉ phân tích khách hàng có mã
WHERE CustomerID IS NOT NULL

GROUP BY CustomerID

ORDER BY GrossSales DESC, CustomerID;
GO
