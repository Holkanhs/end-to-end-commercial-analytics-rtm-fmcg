import duckdb
import os

RAW_CSV = r"raw_data/Mexico FMCG Retail Sales Customer Inventory (2024).csv"
OUTPUT_DIR = "bi_Analytics"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rtm_final_powerbi.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

con = duckdb.connect()

query = f"""
COPY (
    WITH staging AS (
        -- stg_sales_data: cast, round, coalesce nulls
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
        FROM read_csv_auto('{RAW_CSV}')
    ),

    int_performance AS (
        -- int_route_performance: gender fix, loyalty label, KPIs
        SELECT
            invoice_id,
            invoice_date,
            city,
            channel,
            store_format,
            brand,
            category,
            payment_mode,
            units,
            cost_price,
            selling_price,
            revenue,
            cost,
            margin,
            margin_pct,
            stock_on_hand,
            reorder_level,
            lead_time_days,
            customer_age,
            CASE
                WHEN UPPER(customer_gender) = 'O'            THEN 'M'
                WHEN UPPER(customer_gender) IN ('M', 'F')    THEN UPPER(customer_gender)
                ELSE 'N/A'
            END AS customer_gender,
            CASE WHEN loyalty_flag = '1' THEN 'member'
                 ELSE 'non-member'
            END AS loyalty_status,
            ROUND(revenue / NULLIF(units, 0), 2) AS avg_ticket_price,
            CASE
                WHEN margin_pct >= 0.20 THEN 'high profit'
                WHEN margin_pct >= 0.10 THEN 'medium profit'
                ELSE 'low profit'
            END AS profit_segment
        FROM staging
    ),

    final AS (
        -- Surrogate keys (md5 matching dbt_utils.generate_surrogate_key convention)
        -- + fully denormalised for Power BI (no joins needed in the model)
        SELECT
            md5(
                COALESCE(CAST(customer_age AS VARCHAR), '') || '-' ||
                COALESCE(customer_gender, '')               || '-' ||
                COALESCE(loyalty_status,  '')
            )                                               AS customers_key,
            md5(
                COALESCE(brand,    '') || '-' ||
                COALESCE(category, '')
            )                                               AS product_key,
            md5(
                COALESCE(city,         '') || '-' ||
                COALESCE(channel,      '') || '-' ||
                COALESCE(store_format, '')
            )                                               AS location_key,

            -- fact columns (fct_sales)
            invoice_id,
            invoice_date,
            units,
            revenue,
            cost,
            margin,
            margin_pct,
            stock_on_hand,
            reorder_level,
            lead_time_days,
            avg_ticket_price,
            profit_segment,

            -- dim_customers attributes
            customer_age,
            customer_gender,
            loyalty_status,

            -- dim_products attributes (with coalesce matching dim_products.sql)
            COALESCE(brand,    'Unknown') AS brand,
            COALESCE(category, 'Other')   AS category,

            -- dim_locations attributes (with coalesce matching dim_locations.sql)
            COALESCE(city,         'Desconocido') AS city,
            COALESCE(channel,      'No Definido') AS channel,
            COALESCE(store_format, 'General')     AS store_format,

            -- extra staging columns useful for analysis
            payment_mode,
            cost_price,
            selling_price
        FROM int_performance
    )

    SELECT * FROM final
) TO '{OUTPUT_FILE}' (FORMAT CSV, HEADER true);
"""

con.execute(query)
con.close()

row_count = duckdb.sql(f"SELECT COUNT(*) FROM read_csv_auto('{OUTPUT_FILE}')").fetchone()[0]
print(f"rtm_final_powerbi.csv generated -> {OUTPUT_FILE}")
print(f"Rows exported: {row_count:,}")
