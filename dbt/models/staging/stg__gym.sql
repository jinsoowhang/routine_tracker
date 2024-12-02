{{ config(materialized='table') }}

WITH source AS (

    SELECT 
        "Day" AS day,
        "Day_num" AS day_num,
        "Date" AS date,
        "Hour" AS hour,
        "Activity" AS activity,
        "Attribute1" AS attribute_1,
        "Attribute2" AS attribute_2,
        "Attribute3" AS attribute_3,
        "Attribute4" AS attribute_4,
        "Attribute5" AS attribute_5,
        "Attribute6" AS attribute_6,
        "Notes" AS notes
    FROM {{ source('staging', 'raw__gym') }}

),

results AS (
    SELECT 
        {{ dbt_utils.generate_surrogate_key(['date', 'hour', 'activity', 'attribute_2', 'attribute_3', 'attribute_4', 'attribute_5', 'attribute_6']) }} AS activity_id,
        day,
        day_num,
        CAST(TO_CHAR(TO_DATE(date, 'MM/DD/YYYY'), 'YYYYMMDD') AS INTEGER) AS gym_date,
        hour,
        activity,
        attribute_1,
        attribute_2,
        attribute_3,
        attribute_4,
        attribute_5,
        attribute_6,
        notes
    FROM source
)

SELECT *
FROM results