"""build_powerbi_data.py — raw CSV → 4 star-schema CSVs for Power BI.

Mirrors the dbt transformation chain (staging → intermediate → marts) using
DuckDB so reviewers without a Snowflake account can reproduce the exact files
the Power BI dashboard consumes.

Pipeline:
    01_snowflake/sample_data/sales_data_raw.csv
        ↓ staging         (typecast, round, coalesce nulls)
        ↓ intermediate    (gender fix, loyalty label, profit_segment, avg_ticket)
        ↓ marts           (surrogate keys, dim dedupe, full fact)
    03_powerbi/data/
        ├── dim_customers.csv
        ├── dim_products.csv
        ├── dim_locations.csv
        └── fct_sales.csv

Usage:
    python scripts/build_powerbi_data.py
    python scripts/build_powerbi_data.py --raw <path> --out <dir> -v
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import duckdb


# --------------------------------------------------------------------------
# SQL — kept identical to the dbt model logic to guarantee parity
# --------------------------------------------------------------------------

STAGING_SQL = """
    SELECT
        Invoice_ID                          AS invoice_id,
        CAST(Invoice_Date AS DATE)          AS invoice_date,
        City                                AS city,
        Store_Format                        AS store_format,
        Category                            AS category,
        Brand                               AS brand,
        Channel                             AS channel,
        Payment_Mode                        AS payment_mode,
        Units                               AS units,
        ROUND(Cost_Price,      2)           AS cost_price,
        ROUND(Selling_Price,   2)           AS selling_price,
        ROUND(Revenue,         2)           AS revenue,
        ROUND(Cost,            2)           AS cost,
        ROUND(Margin,          2)           AS margin,
        ROUND("Margin_%",      4)           AS margin_pct,
        Stock_On_Hand                       AS stock_on_hand,
        Reorder_Level                       AS reorder_level,
        Lead_Time_Days                      AS lead_time_days,
        COALESCE(CAST(Customer_Age AS INTEGER), 0) AS customer_age,
        Customer_Gender                     AS customer_gender,
        CAST(Loyalty_Flag AS VARCHAR)       AS loyalty_flag
    FROM read_csv_auto('{raw}')
"""

INTERMEDIATE_SQL = """
    SELECT
        invoice_id, invoice_date, city, channel, store_format,
        brand, category, payment_mode, units,
        cost_price, selling_price, revenue, cost, margin, margin_pct,
        stock_on_hand, reorder_level, lead_time_days,
        customer_age,
        CASE
            WHEN UPPER(customer_gender) = 'O'         THEN 'M'
            WHEN UPPER(customer_gender) IN ('M', 'F') THEN UPPER(customer_gender)
            ELSE 'N/A'
        END AS customer_gender,
        CASE WHEN loyalty_flag = '1' THEN 'member' ELSE 'non-member' END AS loyalty_status,
        ROUND(revenue / NULLIF(units, 0), 2) AS avg_ticket_price,
        CASE
            WHEN margin_pct >= 0.20 THEN 'high profit'
            WHEN margin_pct >= 0.10 THEN 'medium profit'
            ELSE 'low profit'
        END AS profit_segment
    FROM staging
"""

FINAL_SQL = """
    SELECT
        md5(COALESCE(CAST(customer_age AS VARCHAR), '') || '-' ||
            COALESCE(customer_gender, '') || '-' ||
            COALESCE(loyalty_status,  '')) AS customers_key,
        md5(COALESCE(brand, '')    || '-' || COALESCE(category, '')) AS product_key,
        md5(COALESCE(city, '')     || '-' ||
            COALESCE(channel, '')  || '-' ||
            COALESCE(store_format, '')) AS location_key,
        invoice_id, invoice_date, units, revenue, cost, margin, margin_pct,
        stock_on_hand, reorder_level, lead_time_days,
        avg_ticket_price, profit_segment,
        customer_age, customer_gender, loyalty_status,
        COALESCE(brand,    'Unknown')     AS brand,
        COALESCE(category, 'Other')       AS category,
        COALESCE(city,         'Desconocido') AS city,
        COALESCE(channel,      'No Definido') AS channel,
        COALESCE(store_format, 'General')     AS store_format,
        payment_mode, cost_price, selling_price
    FROM int_performance
"""

# Per-mart split queries
DIM_QUERIES = {
    "dim_customers": """
        SELECT DISTINCT customers_key, customer_age, customer_gender, loyalty_status
        FROM final ORDER BY customers_key
    """,
    # dim_products: brand × category grain with AVG rollup of per-line
    # numeric attributes. Mirrors dim_products.sql exactly.
    "dim_products": """
        SELECT
            ANY_VALUE(product_key)        AS product_key,
            brand,
            category,
            ROUND(AVG(cost_price),     2) AS cost_price,
            ROUND(AVG(selling_price),  2) AS selling_price,
            ROUND(AVG(stock_on_hand),  0) AS stock_on_hand,
            ROUND(AVG(reorder_level),  0) AS reorder_level,
            ROUND(AVG(lead_time_days), 1) AS lead_time_days
        FROM final
        GROUP BY brand, category
        ORDER BY brand, category
    """,
    "dim_locations": """
        SELECT DISTINCT location_key, city, channel, store_format
        FROM final ORDER BY location_key
    """,
}

FACT_QUERY = """
    SELECT
        customers_key, product_key, location_key,
        invoice_id, invoice_date, units, revenue, cost, margin, margin_pct,
        avg_ticket_price, profit_segment, payment_mode
    FROM final
"""


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------

def build(raw_path: Path, out_dir: Path) -> None:
    log = logging.getLogger(__name__)

    if not raw_path.exists():
        raise FileNotFoundError(f"raw CSV not found: {raw_path}")
    out_dir.mkdir(parents=True, exist_ok=True)

    log.info("opening DuckDB session")
    con = duckdb.connect()

    log.info("creating staging view")
    con.execute(f"CREATE TEMP VIEW staging AS {STAGING_SQL.format(raw=str(raw_path).replace(chr(92), '/'))}")

    log.info("creating intermediate view")
    con.execute(f"CREATE TEMP VIEW int_performance AS {INTERMEDIATE_SQL}")

    log.info("creating final view")
    con.execute(f"CREATE TEMP VIEW final AS {FINAL_SQL}")

    raw_count = con.sql("SELECT COUNT(*) FROM staging").fetchone()[0]
    log.info(f"staging row count: {raw_count:,}")

    # write dims
    for name, sql in DIM_QUERIES.items():
        out_path = out_dir / f"{name}.csv"
        con.execute(f"COPY ({sql}) TO '{out_path.as_posix()}' (FORMAT CSV, HEADER true)")
        rows = con.sql(f"SELECT COUNT(*) FROM read_csv_auto('{out_path.as_posix()}')").fetchone()[0]
        log.info(f"  → {name}.csv  ({rows:,} rows)")

    # write fact
    fact_path = out_dir / "fct_sales.csv"
    con.execute(f"COPY ({FACT_QUERY}) TO '{fact_path.as_posix()}' (FORMAT CSV, HEADER true)")
    fact_rows = con.sql(f"SELECT COUNT(*) FROM read_csv_auto('{fact_path.as_posix()}')").fetchone()[0]
    log.info(f"  → fct_sales.csv  ({fact_rows:,} rows)")

    con.close()
    log.info(f"done — 4 CSVs written to {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--raw", default="01_snowflake/sample_data/sales_data_raw.csv",
                        help="path to raw source CSV (default: %(default)s)")
    parser.add_argument("--out", default="03_powerbi/data",
                        help="output directory for the 4 star-schema CSVs (default: %(default)s)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    build(Path(args.raw), Path(args.out))


if __name__ == "__main__":
    main()
