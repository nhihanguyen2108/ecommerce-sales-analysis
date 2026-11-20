# E-commerce Sales Analysis

## Business Insights & Recommendations

**Period:** 1 December 2010 - 9 December 2011. **Currency:** GBP.

**Purpose:** identify sales patterns, market concentration and customer opportunities in the UCI Online Retail dataset. These are historical observations and proposed actions, not evidence that an intervention has already improved performance.

## Executive summary

The eligible sales dataset contains **530,104 transaction lines**, **19,960 invoices**, **4,338 identified customers**, **5,588,376 units** and **£10,666,684.54 Gross Sales**. Average invoice value is **£534.40**. Gross Sales counts positive, priced, non-cancelled lines and does not deduct later returns or cancellations.

Three priorities emerge: prepare capacity for the observed autumn peak, manage concentration in the UK and large customer accounts, and reconcile returns before using product rankings for purchasing decisions. Customer activity provides a reason to investigate repeat purchasing, but the dataset does not establish the causes of growth or a causal retention effect.

## 1. Sales peak in November, with limited evidence of repeatable seasonality

**Observation.** November 2011 generated **£1,509,496.33**, the highest monthly Gross Sales, **30.69%** above October. Sales rose from August through November. December 2011 records **£638,792.68**, but only through 9 December.

**Business meaning.** The observed autumn increase is relevant to staffing, inventory and fulfilment planning. A single annual cycle is insufficient to establish recurring seasonality. The apparent **57.68%** November-to-December decline is a full-month versus partial-month comparison and cannot establish a business downturn.

**Recommendation.** Review stock availability and order-processing capacity ahead of similar trading periods. Validate demand assumptions with additional years, campaign records and stockout information before committing inventory. Compare December using equivalent elapsed trading days.

**Measure to monitor:** daily Gross Sales, orders, units, stockout rate and fulfilment time; the last two require additional operational data.

**Evidence:** `data/processed/monthly_sales.csv`, `monthly_growth.csv`; SQL queries 01 and 05.

## 2. Sales depend heavily on the UK; overseas totals can conceal account concentration

**Observation.** The UK contributes **£9,025,222.08**, or **84.61%** of Gross Sales. Netherlands contributes **£285,446.34** from **94 invoices and 9 identified customers**; EIRE contributes **£283,453.96** from **288 invoices and 3 identified customers**. Germany contributes **£228,867.14** from **457 invoices and 94 identified customers**.

**Business meaning.** The portfolio is concentrated in the UK. Overseas sales are meaningful, but the very small identified customer populations in Netherlands and EIRE do not demonstrate broad market demand. Country rankings alone should not determine expansion budgets.

**Recommendation.** Protect service quality in the UK while comparing account concentration, returns and contribution margin across overseas markets. Pilot expansion only after assessing logistics, acquisition costs and repeat demand. Margin and acquisition costs are absent from this dataset.

**Measure to monitor:** country share of sales, identified accounts per country, top-account concentration and contribution margin when cost data becomes available.

**Evidence:** `data/processed/country_sales.csv`; SQL query 03; recalculated country controls in `reports/evidence.json`.

## 3. Product rankings need a returns check before inventory decisions

**Observation.** After excluding `DOT`, `POST` and `M` from the product ranking, **REGENCY CAKESTAND 3 TIER** leads at **£174,484.74**. **PAPER CRAFT , LITTLE BIRDIE** follows at **£168,469.60**. The raw workbook contains an 80,995-unit sale for the latter and an equal cancellation on the same day. A 74,215-unit sale of **MEDIUM CERAMIC TOP STORAGE JAR**, worth **£77,183.60**, also has an equal same-day cancellation.

**Business meaning.** These two large sales contribute **£245,653.20** to Gross Sales despite offsetting cancellations in the raw data. The product ranking therefore measures recorded positive sales activity, not realized net demand. The two observed pairs are examples; they are not a complete return reconciliation.

**Recommendation.** Add a documented sale-return matching process and publish Gross Sales alongside a separately defined net measure. Validate outstanding demand before increasing inventory for products dominated by exceptional transactions.

**Measure to monitor:** gross and return-adjusted product value, reversal rate, order concentration and units per invoice.

**Evidence:** `data/processed/top_10_products.csv`, notebook 02; raw invoice pairs `581483/C581484` and `541431/C541433`, reproduced in `reports/evidence.json`. Product aggregation uses the exact StockCode + Description pair, so description variants can split a code. Excluding three codes is not a complete classification of every non-merchandise code.

## 4. Large accounts matter, but gross-value rankings can overstate account value

**Observation.** Customer **14646** contributes **£280,206.02** across **73 invoices**; customer **18102** contributes **£259,657.30** across **60 invoices**. The top 10 identified customers contribute **£1,538,276.65**, or **17.26% of identified-customer Gross Sales** and **14.42% of all Gross Sales**. The denominators are **£8,911,407.90** and **£10,666,684.54**, respectively.

**Business meaning.** A small set of accounts represents a material share of sales. However, the top 10 includes customers **16446** and **12346**, associated with the large cancellations described above. Gross spend alone is insufficient for identifying profitable or loyal accounts.

**Recommendation.** Review the largest accounts individually and combine return-adjusted spend, invoice frequency, recency and margin before allocating account-management benefits. Treat exceptional buyers separately from consistent repeat purchasers.

**Measure to monitor:** return-adjusted account sales, recency, repeat invoice count and account concentration. No churn or RFM model has been implemented in this project.

**Evidence:** `data/processed/customer_sales.csv`; SQL query 04; `reports/evidence.json`.

## 5. Returning customers account for most observed November activity

**Observation.** November has **1,664 active identified customers**: **323 new** and **1,341 returning**. Returning customers account for **80.59%** of that month's active identified customers.

**Business meaning.** Previously observed buyers are a substantial part of November's customer base. This percentage is an activity composition measure, **not a cohort retention rate**. A new customer is first observed in this dataset; purchases before December 2010 are unknown. Consequently, all customers observed in December 2010 are classified as new within the available window.

**Recommendation.** Build acquisition-month cohorts and compare subsequent purchasing using complete observation windows. Test a targeted reactivation or repeat-purchase offer with a comparison group; evaluate incremental margin rather than assuming the offer causes retention.

**Measure to monitor:** cohort repeat-purchase rate, time to next purchase, orders per identified customer and incremental campaign margin. Customer records without an ID cannot be assigned to these cohorts.

**Evidence:** `reports/monthly_customer_activity.csv`; SQL query 07 and `dbo.vw_monthly_customer_activity`.

## 6. Identity coverage and duplicates affect the interpretation

**Observation.** **132,220** eligible lines have no CustomerID and account for **£1,755,276.64**, or approximately **16.46%** of Gross Sales. The eligible dataset retains **5,226 exact duplicate rows**. Removing the repeated copies in a sensitivity calculation would reduce Gross Sales by **£24,573.74** (about **0.23%**), to **£10,642,110.80**.

**Business meaning.** Customer analysis covers only identified purchases, while overall sales include anonymous purchases. Exact duplicates cannot be conclusively classified as ingestion errors without a source line identifier. Retaining them preserves the established project baseline; it does not certify their business validity.

**Recommendation.** Improve customer identification where appropriate and capture a stable source transaction-line key. Agree a deduplication policy before changing the baseline. Publish the sensitivity alongside the current totals instead of silently removing records.

**Measure to monitor:** identified share of sales, missing IDs, duplicate rate and reconciliation differences between systems.

**Evidence:** `reports/evidence.json`; notebook 01. No source data or existing KPI baseline was changed to produce this report.

## Proposed action order

| Priority | Action | Suggested owner | Success measure |
|---|---|---|---|
| 1 | Define returns and duplicate handling | Analytics + finance | Reconciled gross and net measures, explained differences |
| 2 | Review high-value products and accounts | Merchandising + account management | Confirmed demand and return-adjusted account value |
| 3 | Review seasonal capacity and overseas opportunities | Operations + commercial team | Service levels and margin, with comparable time windows |
| 4 | Evaluate repeat-purchase interventions | CRM + analytics | Incremental repeat purchases and margin against a comparison group |

These are proposed responsibilities and measures, not completed initiatives or measured benefits.

## Scope, methodology and validation

The cleaned population excludes invoice codes beginning with `C`, non-positive quantities, non-positive prices, invalid dates and missing/empty invoice numbers. Missing CustomerID is retained for sales analysis and excluded for customer analysis. Revenue is Quantity × UnitPrice. AOV is total Gross Sales / distinct invoices, not the mean of customer or monthly AOVs. Duplicates remain in the baseline. Top-product analysis excludes `DOT`, `POST`, `M`; headline sales still include them.

`python scripts/build_evidence.py --include-raw` reproduced the baseline from the raw workbook, reconciled saved summaries and confirmed the two large reversal pairs. Source hashes and individual checks are in `reports/evidence.json`. This verification covers files and calculations; it does not certify live SQL Server refreshes or Power BI slicer interactions. Dashboard interaction testing remains deferred. See `docs/validation_status.md` for the precise status.

Source: Chen, D. (2015), [Online Retail, UCI Machine Learning Repository](https://doi.org/10.24432/C5BW33), CC BY 4.0. All monetary figures are GBP; calculations retain source precision and round totals for display. Dataset period and currency are documented by [UCI](https://archive.ics.uci.edu/dataset/352/online+retail). No cost, margin, campaign or pre-observation customer history is available.
