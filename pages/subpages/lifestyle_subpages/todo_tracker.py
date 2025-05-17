import streamlit as st
import pandas as pd
from datetime import datetime as dt

# Initialize connection
conn = st.connection("postgresql", type="sql")

def render_todo_tracker(start_dt, end_dt):
    # Perform query
    todo_df = conn.query("""
        SELECT 
            todo_id,
            creation_date,
            category,
            description,
            status,
            priority,
            completion_date,
            notes
        FROM stg__todo
        ORDER BY creation_date;
    """, ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("📋 TODO Tracker")

    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    # Convert creation_date to datetime
    todo_df['creation_date'] = pd.to_datetime(todo_df['creation_date'], format='mixed')

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame to include only the selected date range
    todo_df = todo_df[
        (todo_df['creation_date'] >= pd.to_datetime(start_dt)) & 
        (todo_df['creation_date'] <= pd.to_datetime(end_dt))
    ]

    ######################
    ####### TODOs ########
    ######################

    st.markdown('## TODO Table')

    st.dataframe(todo_df)