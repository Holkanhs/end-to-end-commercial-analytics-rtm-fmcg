WITH sales_performance AS (
    SELECT * FROM {{ ref ('int_route_performance') }} 
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_age','customer_gender','loyalty_status']) }} AS customers_key,
    {{ dbt_utils.generate_surrogate_key(['brand', 'category']) }} AS product_key,
    {{ dbt_utils.generate_surrogate_key(['city', 'channel', 'store_format']) }} AS location_key,
    invoice_id,
    invoice_date,
    units,
    revenue,
    cost,
    margin,
    margin_pct,
    avg_ticket_price,
    profit_segment,
    payment_mode
    FROM sales_performance