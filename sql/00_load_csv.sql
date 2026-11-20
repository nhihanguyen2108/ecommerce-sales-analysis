-- Run after 00_create_schema.sql. Edit @CsvPath for your SQL Server host.
-- SQL Server's service account needs read access to this file.
-- Only loads an EMPTY target; an existing dataset is never deleted or appended to.
USE EcommerceSales;
GO
SET NOCOUNT ON;
SET XACT_ABORT ON;
DECLARE @CsvPath NVARCHAR(4000) = N'D:\Projects\ecommerce-sales-analysis\data\processed\sales_sql_import.csv';
IF OBJECT_ID(N'dbo.sales_clean', N'U') IS NULL
    THROW 51000, 'Create dbo.sales_clean with 00_create_schema.sql first.', 1;
BEGIN TRY
    BEGIN TRANSACTION;
    IF EXISTS (SELECT 1 FROM dbo.sales_clean WITH (TABLOCKX, HOLDLOCK))
        THROW 51001, 'Target is not empty. Import stopped to prevent duplicate loads.', 1;
    DECLARE @Bulk NVARCHAR(MAX) =
        N'BULK INSERT dbo.sales_clean FROM ''' + REPLACE(@CsvPath, '''', '''''') +
        N''' WITH (FORMAT = ''CSV'', FIRSTROW = 2, FIELDQUOTE = ''"'',
            CODEPAGE = ''65001'', ROWTERMINATOR = ''0x0a'', KEEPNULLS,
            CHECK_CONSTRAINTS, TABLOCK, MAXERRORS = 0);';
    EXEC sys.sp_executesql @Bulk;
    IF (SELECT COUNT_BIG(*) FROM dbo.sales_clean) <> 530104
        THROW 51002, 'Unexpected row count; this loader expects the canonical project CSV.', 1;
    IF (SELECT SUM(Revenue) FROM dbo.sales_clean) <> CAST(10666684.5440 AS DECIMAL(19,4))
        THROW 51003, 'Gross sales do not reconcile to the project baseline.', 1;
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;
GO
