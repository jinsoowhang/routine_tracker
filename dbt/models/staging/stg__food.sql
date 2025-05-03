-- models/staging/stg__food.sql
WITH source AS (
    SELECT 
        TO_DATE(rhythm_date::TEXT, 'YYYYMMDD') AS rhythm_date,
        attribute_1 as food_activity,
        attribute_2 as meal_of_day,
        CASE 
            WHEN notes ~ 'food:\s*"([^"]+)"' 
            THEN REGEXP_REPLACE(notes, '.*food:\s*"([^"]+)".*', '\1', 'i')
            ELSE notes
        END AS food,
        CASE 
            WHEN notes ~ 'restaurant:\s*"([^"]+)"' 
            THEN REGEXP_REPLACE(notes, '.*restaurant:\s*"([^"]+)".*', '\1', 'i')
            ELSE places
        END AS restaurant
    FROM {{ ref('stg__rhythm') }}  -- Reference the staging model
    WHERE attribute_1 in ('eat', 'cook')
      AND notes is not null
)

SELECT
    rhythm_date,
    food_activity,
    meal_of_day,
    food,
    restaurant
FROM source