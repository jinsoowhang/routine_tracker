{{ config(materialized='table') }}

WITH source AS (

    SELECT 
        "Date" AS date,
        "Supplier" AS supplier,
        "Category" AS category,
        "Card Owner" AS card_owner,
        "Bank Name" AS bank_name,
        "Type" AS transaction_type,
        "Amount" AS amount,
        "Memo" AS memo
    FROM {{ source('staging', 'raw__finance') }}

),

results AS (

    SELECT 
        CAST(TO_CHAR(TO_DATE(date, 'YYYY-MM-DD'), 'YYYYMMDD') AS INTEGER) AS transaction_date,
        supplier,
        category,
        card_owner,
        bank_name,
        transaction_type,
        amount,
        memo
    FROM source

)

SELECT *
FROM results