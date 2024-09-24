{{ config(materialized='table') }}

WITH source AS (
    SELECT *
    FROM {{ source('staging', 'raw_rhythm') }}
)

SELECT *
FROM source