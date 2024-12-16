WITH raw AS (
    SELECT 
        TO_DATE(rhythm_date::TEXT, 'YYYYMMDD') AS weigh_in_date,
        (REGEXP_MATCHES(notes, 'weight:\s*([\d.]+)'))[1]::NUMERIC AS body_weight
    FROM {{ ref('stg__rhythm') }}  -- Reference the staging model
    WHERE LOWER(notes) LIKE '%weight:%'
),

results AS (
	SELECT 
        weigh_in_date,
		body_weight
	FROM raw
)

SELECT *
FROM results