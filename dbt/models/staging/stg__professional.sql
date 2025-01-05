{{ config(materialized='table') }}

WITH source AS (
    SELECT 
        "Status" AS application_status,
        "Phase" AS application_phase,
        "Year" AS application_year,
        "Date Applied" AS application_month_day,
        "Company" AS company_name,
        "Job Title" AS job_title,
        "Location" AS job_location,
        "Link" AS application_link 
    FROM {{ source('staging', 'raw__professional') }}
),

combined_dates AS (
    SELECT
        -- Generate a unique application_id based on application_link
        CASE 
            WHEN application_link = '' OR application_link IS NULL THEN
                CONCAT('unknown_', ROW_NUMBER() OVER ())
            ELSE
                MD5(application_link)
        END AS application_id,
        application_status,
        TRIM(SPLIT_PART(application_phase, ':', 1)) AS application_phase,
	    TRIM(SPLIT_PART(application_phase, ':', 2)) AS application_phase_desc,
        TO_DATE(CONCAT(application_year, '-', application_month_day), 'YYYY-MM/DD') AS application_date,
        TRIM(company_name) AS company_name,
        TRIM(job_title) AS job_title,
        TRIM(job_location) AS job_location,
        application_link
    FROM source
),

results AS (
    SELECT 
        application_id,
        application_status,
        application_phase,
        application_phase_desc,
        application_date,
        company_name,
        job_title,
        job_location,
        application_link
    FROM combined_dates
)

SELECT *
FROM results
