WITH raw AS (
	SELECT 
		TO_DATE(rhythm_date::TEXT, 'YYYYMMDD') AS rhythm_date,
		(REGEXP_MATCHES(notes, 'mood:\s*([\d.]+)'))[1]::NUMERIC AS mood_score,
		(REGEXP_MATCHES(notes, 'sleep_score:\s*([\d.]+)'))[1]::NUMERIC AS sleep_score,
		(REGEXP_MATCHES(notes, 'weight:\s*([\d.]+)'))[1]::NUMERIC AS body_weight,
		CASE 
		    WHEN notes ~ 'highlight:\s*".+?"' 
		    THEN REGEXP_REPLACE(notes, '.*highlight:\s*"(.*?)".*', '\1', 'i') 
		END AS highlight,
		CASE 
		    WHEN notes ~ 'lowlight:\s*".+?"' 
		    THEN REGEXP_REPLACE(notes, '.*lowlight:\s*"(.*?)".*', '\1', 'i') 
		END AS lowlight
	FROM {{ ref('stg__rhythm') }}  -- Reference the staging model
),

results AS (
	SELECT 
		rhythm_date,
		mood_score,
		sleep_score,
		body_weight,
		highlight,
		lowlight
	FROM raw
)

SELECT *
FROM results