"""Recompute report evidence and reconcile saved outputs without modifying inputs.

Run from any directory: python scripts/build_evidence.py [--include-raw]
Writes reports/evidence.json and reports/monthly_customer_activity.csv.
Raises an error if the canonical data or saved summaries do not reconcile.
"""
from pathlib import Path
import argparse
import hashlib
import json
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-raw', action='store_true', help='Also verify the original Excel workbook and large reversals.')
    args = parser.parse_args()
    source = ROOT / 'data/processed/sales_clean.csv'
    sales = pd.read_csv(source, dtype={'InvoiceNo': 'string', 'StockCode': 'string'}, parse_dates=['InvoiceDate'])
    gross = float(sales.Revenue.sum())
    orders = int(sales.InvoiceNo.nunique())
    assert len(sales) == 530104, 'Unexpected cleaned row count'
    assert orders == 19960 and sales.CustomerID.nunique() == 4338
    assert sales.Quantity.sum() == 5588376
    assert abs(gross - 10666684.544) < 0.000001
    assert sales.Quantity.gt(0).all() and sales.UnitPrice.gt(0).all()
    assert sales.InvoiceDate.notna().all() and sales.InvoiceNo.notna().all()
    assert not sales.InvoiceNo.str.upper().str.startswith('C').any()
    assert np.allclose(sales.Revenue, sales.Quantity * sales.UnitPrice, rtol=0, atol=1e-8)
    assert sales.YearMonth.eq(sales.InvoiceDate.dt.strftime('%Y-%m')).all()
    checks = ['Canonical KPI totals', 'Positive quantities and prices', 'Valid invoice identifiers and dates', 'Revenue = Quantity × UnitPrice', 'YearMonth matches InvoiceDate']
    for filename, key in [('monthly_sales.csv', 'YearMonth'), ('country_sales.csv', 'Country')]:
        actual = sales.groupby(key).agg(Revenue=('Revenue', 'sum'), Orders=('InvoiceNo', 'nunique'), UnitsSold=('Quantity', 'sum')).sort_index()
        saved = pd.read_csv(ROOT / 'data/processed' / filename).set_index(key).sort_index()
        assert actual.index.equals(saved.index), filename
        assert np.allclose(actual.Revenue, saved.Revenue, rtol=0, atol=1e-7), filename
        assert (actual.Orders == saved.Orders).all() and (actual.UnitsSold == saved.UnitsSold).all(), filename
        checks.append(filename + ': values reconcile')
    identified = sales.dropna(subset=['CustomerID'])
    actual_customers = identified.groupby('CustomerID').agg(Revenue=('Revenue', 'sum'), Orders=('InvoiceNo', 'nunique'), UnitsSold=('Quantity', 'sum'))
    saved_customers = pd.read_csv(ROOT / 'data/processed/customer_sales.csv').set_index('CustomerID').sort_index()
    assert actual_customers.index.equals(saved_customers.index)
    assert np.allclose(actual_customers.Revenue, saved_customers.Revenue, rtol=0, atol=1e-7)
    assert (actual_customers.Orders == saved_customers.Orders).all()
    checks.append('customer_sales.csv: revenues and orders reconcile')
    products = sales.loc[~sales.StockCode.isin(['DOT', 'POST', 'M'])].groupby(['StockCode', 'Description'], as_index=False).agg(Revenue=('Revenue', 'sum'), UnitsSold=('Quantity', 'sum')).sort_values(['Revenue', 'StockCode', 'Description'], ascending=[False, True, True])
    saved_products = pd.read_csv(ROOT / 'data/processed/top_10_products.csv', dtype={'StockCode': 'string'})
    assert products.head(10).StockCode.tolist() == saved_products.StockCode.tolist()
    assert products.head(10).Description.tolist() == saved_products.Description.tolist()
    assert np.allclose(products.head(10).Revenue, saved_products.Revenue, rtol=0, atol=1e-7)
    checks.append('top_10_products.csv: ranking and revenue reconcile')
    monthly = sales.groupby('YearMonth').Revenue.sum()
    growth = pd.read_csv(ROOT / 'data/processed/monthly_growth.csv').set_index('YearMonth')
    assert np.allclose(monthly.pct_change().iloc[1:] * 100, growth.MoM_Growth_Pct.iloc[1:], rtol=0, atol=1e-7)
    checks.append('monthly_growth.csv: percentages reconcile')
    first = identified.groupby('CustomerID').YearMonth.min()
    pairs = identified[['CustomerID', 'YearMonth']].drop_duplicates().copy()
    pairs['New'] = pairs.YearMonth.eq(pairs.CustomerID.map(first))
    activity = pairs.groupby('YearMonth').agg(ActiveCustomers=('CustomerID', 'size'), NewCustomers=('New', 'sum'))
    activity['ReturningCustomers'] = activity.ActiveCustomers - activity.NewCustomers
    activity = activity.join(identified.groupby('YearMonth').agg(IdentifiedOrders=('InvoiceNo', 'nunique'), IdentifiedGrossSales=('Revenue', 'sum')))
    assert int(activity.NewCustomers.sum()) == 4338
    assert activity.loc['2011-11', ['ActiveCustomers', 'NewCustomers', 'ReturningCustomers']].tolist() == [1664, 323, 1341]
    checks.append('Monthly customer activity: new + returning = active; first appearances reconcile')
    countries = []
    for country in ['United Kingdom', 'Germany', 'Netherlands', 'EIRE']:
        part = sales[sales.Country.eq(country)]
        revenue = float(part.Revenue.sum())
        count = int(part.InvoiceNo.nunique())
        countries.append(dict(Country=country, GrossSales=round(revenue, 2), Orders=count, Customers=int(part.CustomerID.nunique()), UnitsSold=int(part.Quantity.sum()), AOV=round(revenue/count, 2), RevenueSharePct=revenue/gross*100))
    top_customers = actual_customers.sort_values('Revenue', ascending=False).head(10)
    evidence = {
        'basis': 'Saved cleaned transaction CSV; values recalculated locally, no live SQL or Power BI filter certification',
        'source': source.relative_to(ROOT).as_posix(), 'source_sha256': digest(source),
        'period_start': str(sales.InvoiceDate.min()), 'period_end': str(sales.InvoiceDate.max()),
        'rows': len(sales), 'gross_sales_gbp': round(gross, 3), 'orders': orders,
        'identified_customers': int(sales.CustomerID.nunique()), 'units_sold': int(sales.Quantity.sum()), 'aov_gbp': gross/orders,
        'countries': countries, 'november_revenue_gbp': float(monthly.loc['2011-11']),
        'november_mom_pct': float(monthly.pct_change().loc['2011-11']*100),
        'november_returning_share_pct': 1341/1664*100,
        'identified_gross_sales_gbp': float(identified.Revenue.sum()),
        'top10_customers_gross_sales_gbp': float(top_customers.Revenue.sum()),
        'top10_customers_share_identified_pct': float(top_customers.Revenue.sum()/identified.Revenue.sum()*100),
        'top10_customers_share_all_pct': float(top_customers.Revenue.sum()/gross*100),
        'missing_customer_rows': int(sales.CustomerID.isna().sum()),
        'missing_customer_gross_sales_gbp': float(sales.loc[sales.CustomerID.isna(), 'Revenue'].sum()),
        'exact_duplicate_rows': int(sales.duplicated().sum()),
        'duplicate_revenue_sensitivity_gbp': float(sales.loc[sales.duplicated(), 'Revenue'].sum()),
        'product_only_gross_sales_gbp': float(products.Revenue.sum()), 'checks_passed': checks,
    }
    if args.include_raw:
        raw_path = ROOT / 'data/raw/Online Retail.xlsx'
        raw = pd.read_excel(raw_path, dtype={'InvoiceNo': 'string', 'StockCode': 'string'})
        inv = raw.InvoiceNo.str.strip()
        valid = raw.loc[~inv.str.upper().str.startswith('C', na=False) & raw.Quantity.gt(0) & raw.UnitPrice.gt(0) & raw.InvoiceDate.notna() & inv.notna() & inv.ne('')]
        assert len(raw) == 541909 and len(valid) == len(sales)
        assert abs(float((valid.Quantity*valid.UnitPrice).sum())-gross) < 1e-7
        large = raw[raw.StockCode.isin(['23843', '23166']) & raw.Quantity.abs().ge(70000)].copy()
        large['ValueGBP'] = large.Quantity * large.UnitPrice
        assert len(large) == 4
        assert np.allclose(large.groupby('StockCode').ValueGBP.sum(), 0, rtol=0, atol=1e-7)
        evidence['large_sales_and_reversals'] = json.loads(large[['InvoiceNo', 'StockCode', 'CustomerID', 'InvoiceDate', 'Quantity', 'UnitPrice', 'ValueGBP']].to_json(orient='records', date_format='iso'))
        evidence['raw_sha256'] = digest(raw_path)
        evidence['checks_passed'].append('Raw workbook: canonical size, eligible rows and revenue; two large sale/reversal pairs')
    out = ROOT / 'reports'
    out.mkdir(exist_ok=True)
    activity.to_csv(out / 'monthly_customer_activity.csv', float_format='%.4f')
    (out / 'evidence.json').write_text(json.dumps(evidence, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(evidence, indent=2, ensure_ascii=True))


if __name__ == '__main__':
    main()
