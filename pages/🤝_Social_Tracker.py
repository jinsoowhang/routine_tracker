import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
rhythm_df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🤝Social Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

# Convert to date
rhythm_df['rhythm_date'] = pd.to_datetime(rhythm_df['rhythm_date'], format='%Y%m%d')

# Create a new columns to show days since rhythm_date
rhythm_df['days_since_rhythm_date'] = -(pd.Timestamp.today() - rhythm_df['rhythm_date']).dt.days

# Create a new column to concatenate all relevant columns
columns_to_concatenate = ['activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']

rhythm_df['concatenated_values'] = rhythm_df[columns_to_concatenate].astype(str).apply(
    lambda row: ' | '.join(row.values), axis=1
)

########################
####### Filters ########
########################

default_end_date = dt.today()
default_start_date = default_end_date - timedelta(days=30)

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
rhythm_df = rhythm_df[
    (rhythm_df['rhythm_date'] >= pd.to_datetime(start_dt)) &
    (rhythm_df['rhythm_date'] <= pd.to_datetime(end_dt))
]

# Create a copy of the dataframe
social_df = rhythm_df.copy()

# Data Cleaning

# Step 1: Drop null values
non_null_people = social_df['people'].dropna()

# Step 2: Split names by comma and flatten into a single list
all_people = non_null_people.str.split(',').explode().str.strip()

################################
####### High Level KPIs ########
################################

# High Level KPIs
st.markdown("### High Level KPIs")

# Columns for KPIs
col1, col2 = st.columns(2)

with col1:
    unique_people = all_people.unique()
    unique_count = len(unique_people)
    st.metric(label="Distinct People Count", value=unique_count)

with col2:
    people_counts = all_people.value_counts()
    most_frequent_person = people_counts.idxmax()
    most_frequent_count = people_counts.max()
    st.metric(label="Most Frequent Person", value=f'{most_frequent_person} ({(most_frequent_count/4).round()} hours)')

st.divider()

################################
####### Social Table ###########
################################

st.markdown("### Social Table")

# Calculate total interactions
total_interactions = people_counts.sum()

# Create a new DataFrame for display
social_table_df = people_counts.reset_index()
social_table_df.columns = ['Person', 'Count']

# Add proportion column
social_table_df['Proportion'] = (social_table_df['Count'] / total_interactions).round(2)

# Display table
st.dataframe(social_table_df, use_container_width=True)