WITH source_data AS
 (SELECT * FROM {{ source("raw_data", "sales_data_raw") }}),

-- looking for nulls data (we detected only nulls in customer_age)

count_nulls AS (
SELECT 
COUNT(*) AS total_rows,
SUM(CASE WHEN invoice_id IS NULL THEN 1 ELSE 0 END ) AS null_invoice_id,
SUM(CASE WHEN invoice_date IS NULL THEN 1 ELSE 0 END ) AS null_invoice_date,
SUM(CASE WHEN city IS NULL THEN 1 ELSE 0 END ) AS null_city,
SUM(CASE WHEN store_format IS NULL THEN 1 ELSE 0 END ) AS null_store_format,
SUM(CASE WHEN category IS NULL THEN 1 ELSE 0 END ) AS null_category,
SUM(CASE WHEN brand IS NULL THEN 1 ELSE 0 END ) AS null_brand,
SUM(CASE WHEN channel IS NULL THEN 1 ELSE 0 END ) AS null_channel,
SUM(CASE WHEN payment_mode IS NULL THEN 1 ELSE 0 END ) AS null_payment_mode,
SUM(CASE WHEN units IS NULL THEN 1 ELSE 0 END ) AS null_units,
SUM(CASE WHEN cost_price IS NULL THEN 1 ELSE 0 END ) AS null_cost_price,
SUM(CASE WHEN selling_price IS NULL THEN 1 ELSE 0 END ) AS null_selling_price,
SUM(CASE WHEN revenue IS NULL THEN 1 ELSE 0 END ) AS null_revenue,
SUM(CASE WHEN margin IS NULL THEN 1 ELSE 0 END ) AS null_margin,
SUM(CASE WHEN margin_pct IS NULL THEN 1 ELSE 0 END ) AS null_margin_pct,
SUM(CASE WHEN stock_on_hand IS NULL THEN 1 ELSE 0 END ) AS null_stock_on_hand,
SUM(CASE WHEN reorder_level IS NULL THEN 1 ELSE 0 END ) AS null_reorder_level,
SUM(CASE WHEN lead_time_days IS NULL THEN 1 ELSE 0 END ) AS null_lead_time_days,
SUM(CASE WHEN customer_age IS NULL THEN 1 ELSE 0 END ) AS null_customer_age,
SUM(CASE WHEN customer_gender IS NULL THEN 1 ELSE 0 END ) AS null_customer_gender,
SUM(CASE WHEN loyalty_flag IS NULL THEN 1 ELSE 0 END ) AS null_loyalty_flag
FROM source_data
),

-- cleaning data
cleaning_data_source AS(
SELECT 
invoice_id,
CAST(invoice_date AS DATE) AS invoice_date,
city,
store_format,
category,
brand,
channel,
payment_mode,
units,
ROUND(cost_price,2) AS cost_price,
ROUND(selling_price,2) AS selling_price,
ROUND(revenue,2) AS revenue,
ROUND(cost,2) AS cost,
ROUND(margin,2) AS margin,
ROUND(margin_pct,4) AS margin_pct,
stock_on_hand,
reorder_level,
lead_time_days,
COALESCE(customer_age, 0) AS customer_age,
customer_gender,
loyalty_flag
FROM source_data
)

SELECT *
FROM source_data