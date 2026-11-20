-- Global monthly aggregate used by Power BI. Country is not a key in this view.
-- FirstMonth means first observed purchase within this dataset.
USE EcommerceSales;
GO
CREATE OR ALTER VIEW dbo.vw_monthly_customer_activity
AS
WITH IdentifiedSales AS (
    -- 1. Chỉ lấy giao dịch có mã khách hàng
    SELECT
        YearMonth,
        CustomerID,
        InvoiceNo,
        Revenue
    FROM dbo.sales_clean
    WHERE CustomerID IS NOT NULL
),

FirstPurchase AS (
    -- 2. Xác định tháng đầu tiên xuất hiện
    -- của từng khách hàng trong dữ liệu
    SELECT
        CustomerID,
        MIN(YearMonth) AS FirstMonth
    FROM IdentifiedSales
    GROUP BY CustomerID
),

MonthlyCustomerList AS (
    -- 3. Mỗi khách hàng chỉ xuất hiện
    -- một lần trong mỗi tháng
    SELECT DISTINCT
        YearMonth,
        CustomerID
    FROM IdentifiedSales
),

MonthlyCustomerCounts AS (
    -- 4. Phân loại khách hàng mới và quay lại
    SELECT
        m.YearMonth,

        COUNT(*) AS ActiveCustomers,

        SUM(
            CASE
                WHEN m.YearMonth = f.FirstMonth
                THEN 1 ELSE 0
            END
        ) AS NewCustomers,

        SUM(
            CASE
                WHEN m.YearMonth > f.FirstMonth
                THEN 1 ELSE 0
            END
        ) AS ReturningCustomers

    FROM MonthlyCustomerList m

    INNER JOIN FirstPurchase f
        ON m.CustomerID = f.CustomerID

    GROUP BY m.YearMonth
),

MonthlyTransactions AS (
    -- 5. Tính đơn hàng và doanh thu
    -- của khách hàng có mã
    SELECT
        YearMonth,

        COUNT(DISTINCT InvoiceNo)
            AS IdentifiedOrders,

        CAST(
            SUM(Revenue) AS DECIMAL(18,2)
        ) AS IdentifiedGrossSales

    FROM IdentifiedSales

    GROUP BY YearMonth
)

-- 6. Kết hợp kết quả
SELECT
    c.YearMonth,
    c.ActiveCustomers,
    c.NewCustomers,
    c.ReturningCustomers,
    t.IdentifiedOrders,
    t.IdentifiedGrossSales

FROM MonthlyCustomerCounts c

INNER JOIN MonthlyTransactions t
    ON c.YearMonth = t.YearMonth;
GO
