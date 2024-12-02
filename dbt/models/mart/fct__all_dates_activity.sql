WITH all_dates AS (
    SELECT 
        date_day,
        day_of_week_name_short,
        week_start_date,
        week_of_year,
        month_name_short,
        quarter_start_date
    FROM {{ ref('dim__dates') }}
),

activity_data AS (
    -- Select the necessary columns from the raw activity data
    SELECT 
        TO_DATE(CAST(gym_date AS TEXT), 'YYYYMMDD') AS date_of_activity,
        attribute_6 AS type_of_activity
    FROM {{ ref('stg__gym') }}
),

activity_by_date AS (
    -- Join the date spine with the activity data
    SELECT 
        CAST(all_dates.date_day AS DATE) AS calendar_date,
        all_dates.day_of_week_name_short,
        all_dates.week_start_date,
        all_dates.week_of_year,
        all_dates.month_name_short,
        all_dates.quarter_start_date,
        CASE 
            WHEN date_of_activity IS NOT NULL THEN 1
            ELSE 0
        END AS had_activity,
        type_of_activity
    FROM all_dates 
    LEFT JOIN activity_data
            ON all_dates.date_day = activity_data.date_of_activity
)

-- Final selection of columns
SELECT DISTINCT
    calendar_date,
    day_of_week_name_short,
    week_start_date,
    week_of_year,
    month_name_short,
    quarter_start_date,
    had_activity,
    type_of_activity
FROM activity_by_date
ORDER BY calendar_date
