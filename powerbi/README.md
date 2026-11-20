# Power BI report

Open `ecommerce_sales_dashboard.pbix` in Power BI Desktop. This is an imported-data report; viewing uses the saved model, while refresh requires access to the configured sources.

## Source mapping

| Page | Visual | Source |
|---|---|---|
| Sales Overview | KPIs, monthly trend, countries, Country slicer | `sales_clean` |
| Product & Customer | Top products | Global `top_10_products` CSV |
| Product & Customer | Top customers | `sales_clean` and Customer Gross Sales measure |
| Customer Trends | Both monthly charts | `vw_monthly_customer_activity (2)` in the model |

The `(2)` suffix is the Power BI query/table name. The SQL object is `dbo.vw_monthly_customer_activity`, supplied in `sql/09_create_views.sql`. A second similarly named imported table is present; it has not been removed during packaging.

## Refresh on another computer

1. Rebuild the processed CSVs using both notebooks.
2. Prepare SQL Server using `sql/README.md`.
3. In Power BI, update the SQL Server connection and database, then the CSV file locations in Data source settings / Power Query Source steps. Authenticate using your own account.
4. Preserve the table and field names used by visuals. Refresh and reconcile to `reports/evidence.json`.

## Interpretation and current limits

All monetary amounts are GBP. Gross Sales does not deduct subsequent returns. December 2011 is incomplete. The first observed customer month is not necessarily the true acquisition month.

The monthly active-customer chart was corrected to YearMonth ascending. Currency formats for Gross Sales, AOV, Customer Gross Sales and product Revenue were changed to GBP and saved. Formulas and source data were not changed.

Country testing and cross-page interaction verification remain deferred at the project owner's request. A Country slicer cannot reconstruct country detail in the global product/monthly customer aggregates. Full interaction requires rebuilding those visuals from transactions with a defined customer first-purchase scope. No arbitrary many-to-many relationship was added.

For the precise validation boundary, see [validation status](../docs/validation_status.md).

## Exported pages

Exported directly from Power BI Desktop on 20 November 2026, then rendered to PNG for repository previews. These are the actual report pages, not recreated charts. Country is All in the exported overview. Layout/currency/time ordering were visually reviewed; this is not a slicer certification.

- [All three pages (PDF)](ecommerce_sales_dashboard.pdf)
- [01 - Sales Overview](screenshots/01_sales_overview.png)
- [02 - Product & Customer](screenshots/02_product_customer.png)
- [03 - Customer Trends](screenshots/03_customer_trends.png)
