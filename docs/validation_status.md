# Validation status

Status updated on 20 November 2026. A successful source reconciliation is distinct from successful live-system interaction testing.

## Completed

- Recomputed canonical counts and Gross Sales from `sales_clean.csv`.
- Reconciled monthly/country revenue, invoice and unit summaries, customer revenue/orders, product ranking and monthly growth.
- Recomputed monthly customer activity: November 2011 has 1,664 active, 323 first-observed and 1,341 returning customers.
- Re-read the raw Excel workbook and reproduced eligible row count and revenue. Confirmed both large positive/negative invoice pairs.
- Recorded source SHA-256 hashes and checks in `reports/evidence.json`.
- Reviewed the saved PBIX report-definition source references. This does not establish semantic-model relationships or filter behaviour.
- Exported all three pages natively from Power BI and visually reviewed the PDF/PNG previews, including GBP labels and chronological customer trends.

## Deferred / not certified

- Country slicer sequence UK → Germany → clear selection was interrupted at the user's request. No passing interaction result is claimed.
- Cross-page filters and semantic-model relationships have not been certified. Product/customer summary tables do not contain Country keys.
- SQL overall KPIs were reported as checked by the project owner. The new schema/import/view scripts have not been executed against the owner's live database during this packaging work.
- Fresh installation from PyPI and full notebook rerun have not been performed; installed analysis versions are recorded separately in `requirements-core.txt`.

## Known presentation issues to review

- Fixed and saved: Monthly Active Customers now sorts by YearMonth ascending, December 2010 through December 2011.
- Fixed and saved: Gross Sales, AOV, Customer Gross Sales and the product Revenue column use GBP formatting. The overview was visually checked after the change; numerical measures were not edited.
- Top-products data is a global Top 10 extract. It cannot produce a correct country-specific Top 10 without rebuilding the calculation from detailed sales.
- Customer Trends uses a global month aggregate. New/returning customers by Country require a defined first-purchase scope and calculation from detailed identified transactions.

## Definitions that must remain visible

Gross Sales excludes cancelled and non-positive lines but does not subtract later reversals. Exact duplicate sales rows remain in the baseline. Identified customer analysis excludes missing IDs. December 2011 is partial. New customers are first observed in the available window; returning-customer share is not cohort retention.
