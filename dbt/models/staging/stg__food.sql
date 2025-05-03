-- models/staging/stg__food.sql
WITH source AS (
    SELECT 
        TO_DATE(rhythm_date::TEXT, 'YYYYMMDD') AS rhythm_date,
        CASE 
            WHEN notes ~ 'food:\s*"([^"]+)"' 
            THEN REGEXP_REPLACE(notes, '.*food:\s*"([^"]+)".*', '\1', 'i')
            ELSE NULL
        END AS food,
        CASE 
            WHEN notes ~ 'restaurant:\s*"([^"]+)"' 
            THEN REGEXP_REPLACE(notes, '.*restaurant:\s*"([^"]+)".*', '\1', 'i')
            ELSE NULL
        END AS restaurant
    FROM {{ ref('stg__rhythm') }}  -- Reference the staging model
)

SELECT
    rhythm_date,
    food,
    restaurant
FROM source