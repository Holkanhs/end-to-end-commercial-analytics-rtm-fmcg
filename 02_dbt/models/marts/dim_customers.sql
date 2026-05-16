WITH customers AS (
    SELECT * FROM {{ ref ('int_route_performance') }} 
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_age','customer_gender','loyalty_status']) }} AS customers_key,
    customer_age,
    customer_gender,
    loyalty_status
    FROM {{ ref('int_route_performance') }}
    GROUP BY 1, 2, 3, 4