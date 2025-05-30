WITH raw AS (
    SELECT 
        TO_DATE(gym_date::TEXT, 'YYYYMMDD') AS gym_date,
        TRIM(attribute_1) AS gym_exercise_type,
        TRIM(attribute_2) AS gym_exercise_weight,
        attribute_3 AS gym_exercise_repetitions
    FROM {{ ref('stg__gym') }}  -- Reference the staging model
    WHERE attribute_6 = 'gym'
),

results AS (
	SELECT 
        gym_date,
		gym_exercise_type,
		gym_exercise_weight,
        gym_exercise_repetitions
	FROM raw
)

SELECT *
FROM results