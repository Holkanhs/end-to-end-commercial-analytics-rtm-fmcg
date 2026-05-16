WITH sales_data AS (
    SELECT * FROM {{ ref('stg_sales_data') }}
),

-- we make sure that the raw data calculations are correct

Preview_data_calculations AS (
SELECT
ROUND((cost_price * NULLIF(units,0)),2) AS cost_preview_calc,
cost,
ROUND((selling_price * units),2) AS revenue_preview_calc,
revenue,
ROUND((revenue - cost),2) AS margin_preview_calc,
margin,
ROUND((margin / revenue),4) AS margin_pct_preview_calc, 
margin_pct
FROM sales_data
),

-- now that we make sure everything is fine, we continue calculating the perfomance

performance_calc AS (
    SELECT
        invoice_id,
        invoice_date,
        city,
        channel,
        store_format,
        brand,
        category,
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
        Payment_mode,
        CASE 
        WHEN UPPER(customer_gender) = 'O' THEN 'M'
        WHEN UPPER(customer_gender) IN ('M', 'F') THEN UPPER(customer_gender)
        ELSE 'N/A'
        END AS customer_gender,
        -- Loyalty status 1 = member, 0 = non member
        CASE WHEN loyalty_flag = '1' THEN 'member'
        ELSE 'non-member'
        END AS loyalty_status,
        -- KPI: AVG Ticket 
        ROUND((revenue / units), 2) AS avg_ticket_price,
        -- Rent segmentation
        CASE 
            WHEN margin_pct >= 0.20 THEN 'high profit'
            WHEN margin_pct >= 0.10 THEN 'medium profit'
            ELSE 'low profit'
        END AS profit_segment
    FROM sales_data
)

SELECT *
FROM performance_calc