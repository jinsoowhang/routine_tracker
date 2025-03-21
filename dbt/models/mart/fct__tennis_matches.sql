WITH raw AS (
	SELECT 
        activity_id AS match_id,
		TO_DATE(CAST(gym_date AS TEXT), 'YYYYMMDD') AS gym_date,
		attribute_2 AS score,
		attribute_3 AS teammate,
		attribute_4 AS opponents,
		TRIM(SPLIT_PART(attribute_4, ',', 1)) AS opponent_1,
		TRIM(NULLIF(SPLIT_PART(attribute_4, ',', 2), '')) AS opponent_2,
		notes
	FROM {{ ref('stg__gym') }}  -- Reference the staging model
	WHERE attribute_6 = 'tennis'
),

match_type_cte AS (
	SELECT 
        match_id,
		gym_date,
		CASE 
			WHEN teammate IS NULL AND score IS NULL THEN 'other_tennis_activity'
			WHEN teammate IS NULL AND opponent_1 IS NOT NULL THEN 'singles' 
			WHEN teammate IS NOT NULL and opponent_2 IS NOT NULL THEN 'doubles'
		ELSE NULL END AS match_type,
		score,
		teammate,
		opponents,
		notes
	FROM raw
),

results AS (
	SELECT 
        match_id,
		gym_date,
		match_type,
		score,
		teammate,
		opponents,
		notes
	FROM match_type_cte
)

SELECT *
FROM results