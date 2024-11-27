WITH raw AS (
	SELECT 
		activity_id as match_id,
		attribute_3 AS teammate,
		TRIM(SPLIT_PART(attribute_4, ',', 1)) AS opponent_1,
		TRIM(NULLIF(SPLIT_PART(attribute_4, ',', 2), '')) AS opponent_2,
		attribute_2 AS score
	FROM {{ ref('stg__gym') }}
	WHERE attribute_6 = 'tennis'
),

result_cte AS (
	SELECT
		match_id,
		teammate AS player_name,
		score,
		CASE 
			WHEN substring(score, 1, 1) > SUBSTRING(score, 3, 1) THEN 'Win' 
			WHEN substring(score, 1, 1) < SUBSTRING(score, 3, 1) THEN 'Loss' 
		ELSE NULL END AS result,
		TRUE AS is_teammate
	FROM raw
	WHERE teammate IS NOT NULL
	
	UNION 
	
	SELECT
		match_id,
		opponent_1 AS player_name,
		score,
		CASE 
			WHEN substring(score, 1, 1) < SUBSTRING(score, 3, 1) THEN 'Loss' 
			WHEN substring(score, 1, 1) > SUBSTRING(score, 3, 1) THEN 'Win' 
		ELSE NULL END AS result,
		FALSE AS is_teammate
	FROM raw
	
	UNION 
	
	SELECT
		match_id,
		opponent_2 AS player_name,
		score,
		CASE 
			WHEN substring(score, 1, 1) < SUBSTRING(score, 3, 1) THEN 'Loss' 
			WHEN substring(score, 1, 1) > SUBSTRING(score, 3, 1) THEN 'Win' 
		ELSE NULL END AS result,
		FALSE AS is_teammate
	FROM raw
),

results AS (
	SELECT
		match_id,
		player_name,
		score,
		result,
		is_teammate
	FROM result_cte
)

SELECT *
FROM results