WITH raw AS (
    SELECT 
        TO_DATE(adj_rhythm_date::TEXT, 'YYYYMMDD') AS adj_rhythm_date,
		CONCAT(year_number, '-W', week_of_year) AS adj_year_week_num,
        adj_weekday,
        adj_day_num,
        attribute_1	
    FROM {{ ref('stg__rhythm') }} rhythm -- Reference the staging model
	JOIN {{ ref('dim__dates') }} dates
	  ON TO_DATE(rhythm.adj_rhythm_date::TEXT, 'YYYYMMDD') = dates.date_day
	WHERE adj_rhythm_date >= 20220101
),

activity_score_cte AS (
	SELECT
		adj_rhythm_date,
		adj_year_week_num,
		adj_weekday,
		adj_day_num,
		attribute_1,
		CASE 
			WHEN attribute_1 = 'love' THEN 3.0
			WHEN attribute_1 = 'study' THEN 2.6
			WHEN attribute_1 = 'side_hustle' THEN 2.4
			WHEN attribute_1 = 'work' THEN 2.2
			WHEN attribute_1 = 'read' THEN 1.9
			WHEN attribute_1 = 'exercise' THEN 1.65
			WHEN attribute_1 = 'learn' THEN 1.65
			WHEN attribute_1 = 'church' THEN 1.5
			WHEN attribute_1 = 'productive' THEN 1.2 
			WHEN attribute_1 = 'meet' THEN 1.2
			WHEN attribute_1 = 'call' THEN 1.0
			WHEN attribute_1 = 'cook' THEN 1.0
			WHEN attribute_1 = 'walk' THEN 1.0
			WHEN attribute_1 = 'grocery' THEN 0.9
			WHEN attribute_1 = 'clean' THEN 0.65
			WHEN attribute_1 = 'walk' THEN 0.65
			WHEN attribute_1 = 'eat' THEN 0.65
			WHEN attribute_1 = 'shopping' THEN 0.65 
			WHEN attribute_1 = 'hygiene' THEN 0.65
			WHEN attribute_1 = 'hangout' THEN 0.65
			WHEN attribute_1 = 'prepare' THEN 0.65
			WHEN attribute_1 = 'sick' THEN 0.65
			WHEN attribute_1 = 'travel' THEN 0.65
			WHEN attribute_1 = 'wake_up' THEN 0.65
			WHEN attribute_1 = 'commute' THEN 0.35
			WHEN attribute_1 = 'leisure' THEN 0
			WHEN attribute_1 = 'sleep' THEN 0
		ELSE NULL END AS activity_score
	FROM raw
),

agg_score_cte AS (
	SELECT 
		adj_rhythm_date,
		adj_year_week_num,
		adj_weekday,
		adj_day_num,
		SUM(activity_score) AS total_daily_score
	FROM activity_score_cte
	GROUP BY adj_rhythm_date, adj_year_week_num, adj_weekday, adj_day_num
	ORDER BY adj_rhythm_date
),

results AS (
	SELECT 
		adj_rhythm_date,
		adj_year_week_num,
		adj_weekday,
		adj_day_num,
		total_daily_score
	FROM agg_score_cte
)

SELECT *
FROM results