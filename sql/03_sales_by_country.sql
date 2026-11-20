
-- QUERY 03: SALES BY COUNTRY

USE EcommerceSales;
GO

SELECT
    Country,

    -- Tổng doanh thu theo quốc gia
    CAST(
        SUM(Revenue) AS DECIMAL(18,2)
    ) AS GrossSales,

    -- Số hóa đơn duy nhất
    COUNT(DISTINCT InvoiceNo) AS Orders,

    -- Số khách hàng xác định được
    COUNT(DISTINCT CustomerID) AS Customers,

    -- Tổng số lượng bán
    SUM(Quantity) AS UnitsSold

FROM dbo.sales_clean

-- Nhóm dữ liệu theo quốc gia
GROUP BY Country

-- Sắp xếp doanh thu từ cao xuống thấp
ORDER BY GrossSales DESC, Country;
GO
