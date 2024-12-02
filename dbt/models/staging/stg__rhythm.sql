{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ source('staging', 'raw__rhythm') }}
),

results AS (
    SELECT 
        {{ dbt_utils.generate_surrogate_key(['date', 'hour']) }} AS activity_id,
        weekday,
        day_num,
        CAST(TO_CHAR(TO_DATE(date, 'MM/DD/YYYY'), 'YYYYMMDD') AS INTEGER) AS rhythm_date,
        hour,
        activity,
        attribute_1,
        attribute_2,
        attribute_3,
        attribute_4,
        places,
        people,
        notes,
        adj_day,
        adj_day_num,
        adj_date,
        adj_hour
    FROM source
)

SELECT *
FROM results