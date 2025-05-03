import streamlit as st
import pandas as pd
from datetime import datetime as dt

# Initialize connection
conn = st.connection("postgresql", type="sql")

def render_journal_tracker(start_dt, end_dt):
    # Perform query
    journal_df = conn.query("""
        SELECT 
            rhythm_date,
            highlight,
            lowlight,
            dream,
            lesson
        FROM stg__journal;
    """, ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("📓 Journal Tracker")

    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    # Convert journal_date to datetime
    journal_df['rhythm_date'] = pd.to_datetime(journal_df['rhythm_date'], format='%Y%m%d')

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame to include only the selected date range
    journal_df = journal_df[
        (journal_df['rhythm_date'] >= pd.to_datetime(start_dt)) & 
        (journal_df['rhythm_date'] <= pd.to_datetime(end_dt))
    ]

    ##############################
    ####### Track Journal ########
    ##############################

    st.markdown('## Track Journal Entries')

    # User Input
    journal_entry_prompt = st.text_input("Write your journal entry")

    # Create a new column to concatenate all relevant columns
    columns_to_concatenate = journal_df.columns

    journal_df['concatenated_values'] = journal_df[columns_to_concatenate].astype(str).apply(
        lambda row: ' | '.join(row.values), axis=1
    )

    # Filter data by user input
    filter_by_entry = journal_df[journal_df['concatenated_values'].str.lower().str.contains(journal_entry_prompt, na=False)]

    # Display the filtered journal entries
    st.write(f"Found {len(filter_by_entry)} journal entries matching your input")

    ###############################
    ####### Journal Table ########
    ###############################

    st.markdown('## Journal Table')

    # Display the filtered journal entries
    st.dataframe(filter_by_entry, use_container_width=True, hide_index=True)

    st.divider()
