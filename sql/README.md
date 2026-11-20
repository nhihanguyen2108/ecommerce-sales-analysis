# SQL Server workflow

Use SQL Server 2017 or newer and SSMS. Scripts use T-SQL (`GO`, `TOP`, `COUNT(DISTINCT ...)`, CTEs and window functions). They do not run unchanged in PostgreSQL.

## Fresh setup

1. Run both notebooks in order to generate `data/processed/sales_sql_import.csv`.
2. Run `00_create_schema.sql`. It creates `EcommerceSales` and `dbo.sales_clean` only if missing.
3. Open `00_load_csv.sql` and edit `@CsvPath`. The path is on the SQL Server host, which can differ from the computer running SSMS. The SQL Server service account must be able to read the file.
4. Run the loader once. It requires an empty target, imports UTF-8 quoted CSV, preserves missing CustomerID as NULL, checks row/revenue totals and rolls back on failure. It does not clear an existing table.
5. Run `09_create_views.sql`, then `10_validate_kpis.sql`.
6. Run the eight analysis queries as needed.

For an existing populated database, skip the schema/load steps and inspect the schema before using the new view definition. `09_create_views.sql` uses `CREATE OR ALTER VIEW`, so it replaces an existing view with the documented project logic. New scripts have been reviewed locally; live execution is a separate validation step, not claimed here.

The import column order matches the 14 exported columns exactly. Identifiers are NVARCHAR, CustomerID is nullable INT, date is DATETIME2(0), and UnitPrice/Revenue are DECIMAL(19,4). NVARCHAR(30)/NVARCHAR(255) preserve the widths assumed by the existing binary product grouping. Do not use InvoiceNo as a primary key: an invoice has several lines. Avoid joins that multiply transaction rows.

## Query index

| Script | Question / output |
|---|---|
| 01_monthly_sales | Revenue, invoices, units and AOV by month |
| 02_top_products | Top 10 exact StockCode + Description groups; excludes DOT/POST/M |
| 03_sales_by_country | Gross sales and activity by country |
| 04_customer_analysis | Top 10 identified customers |
| 05_monthly_growth | Month-over-month sales growth using LAG |
| 06_sales_by_year | Partial-year totals; not a like-for-like YoY comparison |
| 07_monthly_customer_activity | Active, first-observed and returning customers |
| 08_product_sales_contribution | Top-product shares; denominator excludes DOT/POST/M |
| 09_create_views | Reusable global monthly customer-activity view |
| 10_validate_kpis | Overall/country controls and monthly customer shares |

The monthly view has one row per YearMonth and no Country key. Joining it to transactions by month does not create valid country-level customer counts. New means first purchase *observed in this dataset*. Returning share is not a cohort retention rate. Distinct customers and invoices must be recalculated at the required grain, not blindly summed across groups.

Bulk import syntax reference: [Microsoft Learn - BULK INSERT](https://learn.microsoft.com/en-us/sql/t-sql/statements/bulk-insert-transact-sql). File quoting matters because product descriptions can contain commas.
