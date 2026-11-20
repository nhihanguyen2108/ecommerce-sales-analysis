-- Run first, on SQL Server 2017+ (CSV import support).
-- Existing tables are preserved; no DROP, TRUNCATE or data replacement.
USE master;
GO
IF DB_ID(N'EcommerceSales') IS NULL
    EXEC(N'CREATE DATABASE EcommerceSales');
GO
USE EcommerceSales;
GO
IF OBJECT_ID(N'dbo.sales_clean', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.sales_clean (
        InvoiceNo NVARCHAR(30) NOT NULL,
        StockCode NVARCHAR(30) NOT NULL,
        Description NVARCHAR(255) NULL,
        Quantity INT NOT NULL,
        InvoiceDate DATETIME2(0) NOT NULL,
        UnitPrice DECIMAL(19,4) NOT NULL,
        CustomerID INT NULL,
        Country NVARCHAR(100) NOT NULL,
        InvoiceCancelled BIT NOT NULL,
        TransactionType NVARCHAR(50) NOT NULL,
        Revenue DECIMAL(19,4) NOT NULL,
        [Year] INT NOT NULL,
        [Month] INT NOT NULL,
        YearMonth CHAR(7) NOT NULL,
        CONSTRAINT CK_sales_positive CHECK (Quantity > 0 AND UnitPrice > 0),
        CONSTRAINT CK_sales_not_cancelled CHECK (InvoiceCancelled = 0),
        CONSTRAINT CK_sales_month CHECK ([Month] BETWEEN 1 AND 12)
    );
END;
GO
-- InvoiceNo is NOT a unique key: an invoice contains multiple product lines.
-- No line identifier exists in the source; exact duplicates remain documented.
