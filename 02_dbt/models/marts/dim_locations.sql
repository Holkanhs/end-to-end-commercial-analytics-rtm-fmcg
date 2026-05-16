WITH location_channels AS (
    SELECT * FROM {{ ref ('int_route_performance') }} 
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['city', 'channel', 'store_format']) }} AS location_key,
    COALESCE(city, 'Desconocido') AS city,
    COALESCE(channel, 'No Definido') AS channel,
    COALESCE(store_format, 'General') AS store_format
FROM {{ ref('int_route_performance') }}
GROUP BY 1, 2, 3, 4