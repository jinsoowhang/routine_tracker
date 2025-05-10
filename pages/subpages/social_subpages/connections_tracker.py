import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime as dt

def render_connections_tracker(shared_start_date, shared_end_date):
    # Initialize connection.
    conn = st.connection("postgresql", type="sql")

    # Perform query.
    rhythm_df = conn.query("""SELECT *
                              FROM dim__social_categories"""
                            , ttl="10m")

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
    columns_to_concatenate = ['attribute_1', 'attribute_2', 'places', 'people', 'individuals', 'social_type']
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

    ################################
    ####### High Level KPIs ########
    ################################

    st.markdown("### High Level KPIs")

    col1, col2 = st.columns(2)

    with col1:
        unique_people = social_df['individuals'].unique()
        unique_count = len(unique_people)
        st.metric(label="Distinct People Count", value=unique_count)

    with col2:
        people_counts = social_df[['individuals']].value_counts()
        if not people_counts.empty:
            most_frequent_person = people_counts.idxmax()[0]  # Access the value within the tuple
            most_frequent_count = people_counts.max()
            st.metric(label="Most Frequent Person", value=f'{most_frequent_person} ({(most_frequent_count / 4).round()} hours)')
        else:
            st.metric(label="Most Frequent Person", value="N/A")

    st.divider()

    ################################
    ####### Social Table ###########
    ################################

    st.markdown("### Social Table")

    # Filter relevant columns
    interactions_df = social_df[['individuals', 'social_type']].copy()

    # Count the number of interactions by individuals and social type
    people_counts = interactions_df.groupby(['individuals', 'social_type']).size().reset_index(name='Count')

    # Calculate the total number of interactions
    total_interactions = people_counts['Count'].sum()

    # Prepare the DataFrame for the social table with 'individuals', 'social_type', 'Count', 'Hours', and 'Proportion'
    social_table_df = people_counts.copy()
    social_table_df['Hours'] = (social_table_df['Count'] / 4).round(2)
    social_table_df['Proportion'] = (social_table_df['Count'] / total_interactions).round(2)

    # Display the updated social table
    st.dataframe(social_table_df[['individuals', 'social_type', 'Hours', 'Proportion']].sort_values(by='Hours', ascending=False), use_container_width=True)

