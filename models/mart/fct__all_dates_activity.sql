WITH all_dates AS (
    SELECT 
        date_day
    FROM {{ ref('dim__dates') }}
),

activity_data AS (
    -- Select the necessary columns from the raw activity data
    SELECT 
        CAST("Date" AS DATE) AS date_of_activity,
        "Activity" AS activity
    FROM {{ ref('stg__gym') }}
),

activity_by_date AS (
    -- Join the date spine with the activity data
    SELECT 
        all_dates.date_day AS calendar_date,
        CASE 
            WHEN date_of_activity IS NOT NULL THEN 'Yes'
            ELSE 'No'
        END AS had_activity,
        activity 
    FROM all_dates 
    LEFT JOIN activity_data
            ON all_dates.date_day = activity_data.date_of_activity
)

-- Final selection of columns
SELECT
    calendar_date,
    had_activity,
    activity
FROM activity_by_date
ORDER BY calendar_date
