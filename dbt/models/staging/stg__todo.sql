{{ config(materialized='table') }}

WITH source AS (
    SELECT 
        "ID" as todo_id, 
        "Date" as creation_date, 
        "Category" as category, 
        "Description" as description, 
        "Status" as status, 
        "Priority" as priority, 
        "Completion Date" as completion_date, 
        "Notes" as notes
    FROM {{ source('staging', 'raw__todo') }}
    WHERE "Date" IS NOT NULL
)

SELECT 
    todo_id,
    creation_date,
    category,
    description,
    status,
    priority,
    completion_date,
    notes
FROM source