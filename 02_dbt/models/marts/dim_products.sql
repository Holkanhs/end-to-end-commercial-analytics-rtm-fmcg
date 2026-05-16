-- dim_products: brand × category dimension with rolled-up SKU attributes.
--
-- Grain: one row per (brand, category) — 64 rows for 8 brands × 8 categories.
--
-- The 5 numeric attributes (cost_price, selling_price, stock_on_hand,
-- reorder_level, lead_time_days) are AVERAGED across all invoice lines in
-- the brand/category since the raw data carries them per line, not per SKU.
-- This is a deliberate rollup so the dim preserves a proper many-to-one
-- relationship to fct_sales rather than degenerating to fact grain.

WITH category_products AS (
    SELECT * FROM {{ ref('int_route_performance') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['brand', 'category']) }} AS product_key,
    COALESCE(brand,    'Unknown') AS brand,
    COALESCE(category, 'Other')   AS category,
    ROUND(AVG(cost_price),     2) AS cost_price,
    ROUND(AVG(selling_price),  2) AS selling_price,
    ROUND(AVG(stock_on_hand),  0) AS stock_on_hand,
    ROUND(AVG(reorder_level),  0) AS reorder_level,
    ROUND(AVG(lead_time_days), 1) AS lead_time_days
FROM {{ ref('int_route_performance') }}
GROUP BY 1, 2, 3
