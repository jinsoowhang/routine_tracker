{{ config(materialized='table') }}

WITH source AS (
    SELECT *
    FROM {{ source('staging', 'raw_gym') }}
)

SELECT *
FROM source