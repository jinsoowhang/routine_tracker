import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime as dt

def render_connections_tracker(shared_start_date, shared_end_date):
    # Initialize connection.
    conn = st.connection("postgresql", type="sql")

    # Perform query.
    rhythm_df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("""👥Connections Tracker""")
    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    # Convert to date
    rhythm_df['rhythm_date'] = pd.to_datetime(rhythm_df['rhythm_date'], format='%Y%m%d')

    # Create a new column to show days since rhythm_date
    rhythm_df['days_since_rhythm_date'] = -(pd.Timestamp.today() - rhythm_df['rhythm_date']).dt.days

    # Create a new column to concatenate all relevant columns
    columns_to_concatenate = ['activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']
    rhythm_df['concatenated_values'] = rhythm_df[columns_to_concatenate].astype(str).apply(
        lambda row: ' | '.join(row.values), axis=1
    )

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame using shared date range
    rhythm_df = rhythm_df[
        (rhythm_df['rhythm_date'] >= pd.to_datetime(shared_start_date)) &
        (rhythm_df['rhythm_date'] <= pd.to_datetime(shared_end_date))
    ]

    # Create a copy of the dataframe
    social_df = rhythm_df.copy()

    # Step 1: Drop null values
    non_null_people = social_df['people'].dropna()

    # Step 2: Split names by comma and flatten into a single list
    all_people = non_null_people.str.split(',').explode().str.strip()

    ################################
    ####### High Level KPIs ########
    ################################

    st.markdown("### High Level KPIs")

    col1, col2 = st.columns(2)

    with col1:
        unique_people = all_people.unique()
        unique_count = len(unique_people)
        st.metric(label="Distinct People Count", value=unique_count)

    with col2:
        people_counts = all_people.value_counts()
        if not people_counts.empty:
            most_frequent_person = people_counts.idxmax()
            most_frequent_count = people_counts.max()
            st.metric(label="Most Frequent Person", value=f'{most_frequent_person} ({(most_frequent_count/4).round()} hours)')
        else:
            st.metric(label="Most Frequent Person", value="N/A")

    st.divider()

    ################################
    ####### Social Table ###########
    ################################

    st.markdown("### Social Table")

    if not all_people.empty:
        total_interactions = people_counts.sum()
        social_table_df = people_counts.reset_index()
        social_table_df.columns = ['Person', 'Count']
        social_table_df['Hours'] = (social_table_df['Count'] / 4).round(2)
        social_table_df['Proportion'] = (social_table_df['Count'] / total_interactions).round(2)
        st.dataframe(social_table_df[['Person', 'Hours', 'Proportion']], use_container_width=True)
    else:
        st.info("No social interactions found in the selected date range.")
