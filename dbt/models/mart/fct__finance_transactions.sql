WITH source AS (
    SELECT 
        TO_DATE(transaction_date::TEXT, 'YYYYMMDD') AS transaction_date,
        finance.supplier,
        supplier.parent_supplier,
        supplier.spend_category,
        finance.bank_spend_category,
        card_owner,
        bank_name,
        transaction_type,
        amount,
        memo
    FROM {{ ref('stg__finance') }} finance
    LEFT JOIN {{ ref('dim__supplier') }} supplier
        ON finance.supplier = supplier.supplier
),

results AS (
    SELECT
        transaction_date,
        supplier,
        parent_supplier,
        spend_category,
        bank_spend_category,
        card_owner,
        bank_name,
        transaction_type,
        amount,
        memo
    FROM source 
)

SELECT *
FROM results