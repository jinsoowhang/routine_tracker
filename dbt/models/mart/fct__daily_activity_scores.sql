WITH weekly_scores AS (
    SELECT 
        EXTRACT(YEAR FROM adj_rhythm_date) AS year,
        adj_weekday,
        avg(total_daily_score) AS average_daily_score
    FROM public.fct__daily_activity_scores
    GROUP BY year, adj_weekday
),

highest_score AS (
    SELECT 
        year,
        MAX(average_daily_score) AS max_weekday_score
    FROM weekly_scores
    GROUP BY year
),

raw AS (
    SELECT 
        TO_DATE(adj_rhythm_date::TEXT, 'YYYYMMDD') AS adj_rhythm_date,
        CONCAT(year_number, '-W', LPAD(week_of_year::TEXT, 2, '0')) AS adj_year_week_num,
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
            WHEN attribute_1 = 'dating' THEN 2.5
            WHEN attribute_1 = 'study' THEN 2.5
            WHEN attribute_1 = 'side_hustle' THEN 2.3
            WHEN attribute_1 = 'read' THEN 2.2
            WHEN attribute_1 = 'work' THEN 2.0
            WHEN attribute_1 = 'exercise' THEN 1.9
            WHEN attribute_1 = 'learn' THEN 1.9
            WHEN attribute_1 = 'church' THEN 1.5
            WHEN attribute_1 = 'productive' THEN 1.2 
            WHEN attribute_1 = 'meet' THEN 1.0
            WHEN attribute_1 = 'call' THEN 1.0
            WHEN attribute_1 = 'cook' THEN 1.0
            WHEN attribute_1 = 'walk' THEN 1.0
            WHEN attribute_1 = 'grocery' THEN 1.0
            WHEN attribute_1 = 'clean' THEN 1.0
            WHEN attribute_1 = 'no tracking' then 0.70
            WHEN attribute_1 = 'eat' THEN 0.65
            WHEN attribute_1 = 'shopping' THEN 0.65 
            WHEN attribute_1 = 'hygiene' THEN 0.65
            WHEN attribute_1 = 'hangout' THEN 0.65
            WHEN attribute_1 = 'prepare' THEN 0.65
            WHEN attribute_1 = 'sick' THEN 0.65
            WHEN attribute_1 = 'travel' THEN 0.65
            WHEN attribute_1 = 'vacation' THEN 0.65
            WHEN attribute_1 = 'wake_up' THEN 0.65
            WHEN attribute_1 = 'commute' THEN 0.65
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
        CASE 
            WHEN SUM(activity_score) > 110 THEN 110
            ELSE SUM(activity_score)
        END AS total_daily_score
    FROM activity_score_cte
    GROUP BY adj_rhythm_date, adj_year_week_num, adj_weekday, adj_day_num
    ORDER BY adj_rhythm_date
),

adjusted_scores AS (
    SELECT
        adj_rhythm_date,
        adj_year_week_num,
        adj_weekday,
        adj_day_num,
        total_daily_score,
        year,  -- Add year to the result
        max_weekday_score,  -- Join the dynamic max score for that year
        -- Define the weekday adjustment based on the year-specific max score
        CASE 
            WHEN adj_weekday = 'Thursday' THEN total_daily_score
            WHEN adj_weekday = 'Tuesday' THEN total_daily_score + (max_weekday_score - 78.19) * 0.5  -- Example adjustment formula
            WHEN adj_weekday = 'Saturday' THEN total_daily_score + (max_weekday_score - 64.00) * 0.5
            WHEN adj_weekday = 'Wednesday' THEN total_daily_score + (max_weekday_score - 75.36) * 0.5
            WHEN adj_weekday = 'Friday' THEN total_daily_score + (max_weekday_score - 66.40) * 0.5
            WHEN adj_weekday = 'Sunday' THEN total_daily_score + (max_weekday_score - 62.60) * 0.5
            WHEN adj_weekday = 'Monday' THEN total_daily_score + (max_weekday_score - 71.75) * 0.5
            ELSE total_daily_score
        END AS adjusted_score
    FROM agg_score_cte
    JOIN highest_score
        ON EXTRACT(YEAR FROM adj_rhythm_date) = highest_score.year  -- Join to match the year
)

SELECT 
    adj_rhythm_date,
    adj_year_week_num,
    adj_weekday,
    adj_day_num,
    total_daily_score,
    ROUND(adjusted_score, 2) as adjusted_score
FROM adjusted_scores



---------------------------------------------------------------------------
-- If volumes get reset, then rerun the model below to initialize the table
---------------------------------------------------------------------------

-- with raw as (
-- 	SELECT 
-- 	    TO_DATE(adj_rhythm_date::TEXT, 'YYYYMMDD') AS adj_rhythm_date,
-- 	    CONCAT(year_number, '-W', LPAD(week_of_year::TEXT, 2, '0')) AS adj_year_week_num,
-- 	    adj_weekday,
-- 	    adj_day_num,
-- 	    attribute_1    
--     FROM {{ ref('stg__rhythm') }} rhythm -- Reference the staging model
--     JOIN {{ ref('dim__dates') }} dates
-- 	  ON TO_DATE(rhythm.adj_rhythm_date::TEXT, 'YYYYMMDD') = dates.date_day
-- 	WHERE adj_rhythm_date >= 20220101
-- ),

-- activity_score_cte AS (
--     SELECT
--         adj_rhythm_date,
--         adj_year_week_num,
--         adj_weekday,
--         adj_day_num,
--         attribute_1,
--         CASE 
--             WHEN attribute_1 = 'love' THEN 3.0
--             WHEN attribute_1 = 'study' THEN 2.6
--             WHEN attribute_1 = 'side_hustle' THEN 2.4
--             WHEN attribute_1 = 'read' THEN 2.2
--             WHEN attribute_1 = 'work' THEN 2.0
--             WHEN attribute_1 = 'exercise' THEN 1.9
--             WHEN attribute_1 = 'learn' THEN 1.9
--             WHEN attribute_1 = 'church' THEN 1.5
--             WHEN attribute_1 = 'productive' THEN 1.2 
--             WHEN attribute_1 = 'meet' THEN 1.0
--             WHEN attribute_1 = 'call' THEN 1.0
--             WHEN attribute_1 = 'cook' THEN 1.0
--             WHEN attribute_1 = 'walk' THEN 1.0
--             WHEN attribute_1 = 'grocery' THEN 1.0
--             WHEN attribute_1 = 'clean' THEN 1.0
--             WHEN attribute_1 = 'eat' THEN 0.65
--             WHEN attribute_1 = 'shopping' THEN 0.65 
--             WHEN attribute_1 = 'hygiene' THEN 0.65
--             WHEN attribute_1 = 'hangout' THEN 0.65
--             WHEN attribute_1 = 'prepare' THEN 0.65
--             WHEN attribute_1 = 'sick' THEN 0.65
--             WHEN attribute_1 = 'travel' THEN 0.65
--             WHEN attribute_1 = 'vacation' THEN 0.65
--             WHEN attribute_1 = 'wake_up' THEN 0.65
--             WHEN attribute_1 = 'commute' THEN 0.65
--             WHEN attribute_1 = 'leisure' THEN 0
--             WHEN attribute_1 = 'sleep' THEN 0
--         ELSE NULL END AS activity_score
--     FROM raw
-- ),

-- agg_score_cte AS (
--     SELECT 
--         adj_rhythm_date,
--         adj_year_week_num,
--         adj_weekday,
--         adj_day_num,
--         CASE 
--             WHEN SUM(activity_score) > 110 THEN 110
--             ELSE SUM(activity_score)
--         END AS total_daily_score
--     FROM activity_score_cte
--     GROUP BY adj_rhythm_date, adj_year_week_num, adj_weekday, adj_day_num
--     ORDER BY adj_rhythm_date
-- )

-- select * from agg_score_cte

