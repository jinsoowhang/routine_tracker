{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ source('staging', 'raw__rhythm') }}
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['date', 'hour']) }} AS activity_id,
    weekday,
    day_num,
    date,
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