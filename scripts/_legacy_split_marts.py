import duckdb, os

SRC = 'bi_Analytics/rtm_final_powerbi.csv'
OUT = 'bi_Analytics'

con = duckdb.connect()

exports = {

    # dim_customers — surrogate key + 3 attributes, deduplicated
    'dim_customers': f"""
        SELECT DISTINCT
            customers_key,
            customer_age,
            customer_gender,
            loyalty_status
        FROM read_csv_auto('{SRC}')
        ORDER BY customers_key
    """,

    # dim_locations — surrogate key + 3 attributes, deduplicated
    'dim_locations': f"""
        SELECT DISTINCT
            location_key,
            city,
            channel,
            store_format
        FROM read_csv_auto('{SRC}')
        ORDER BY location_key
    """,

    # dim_products — surrogate key + 2 attributes, deduplicated
    'dim_products': f"""
        SELECT DISTINCT
            product_key,
            brand,
            category
        FROM read_csv_auto('{SRC}')
        ORDER BY product_key
    """,

    # fct_sales — exact columns from fct_sales.sql, all rows (no dedup)
    'fct_sales': f"""
        SELECT
            customers_key,
            product_key,
            location_key,
            invoice_id,
            invoice_date,
            units,
            revenue,
            cost,
            margin,
            margin_pct,
            stock_on_hand,
            avg_ticket_price,
            profit_segment
        FROM read_csv_auto('{SRC}')
    """,
}

for name, query in exports.items():
    path = f"{OUT}/{name}.csv"
    con.execute(f"COPY ({query}) TO '{path}' (FORMAT CSV, HEADER true)")
    rows = con.sql(f"SELECT COUNT(*) FROM read_csv_auto('{path}')").fetchone()[0]
    print(f"{name}.csv  ->  {rows:,} rows  ->  {path}")

con.close()
