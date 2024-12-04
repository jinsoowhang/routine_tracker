import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
rhythm_df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""⏱️Activity Tracker""")

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

# User Input
last_activity_prompt = st.text_input("Write the last activity 👇")

# Filter data by user input
filter_by_user_prompt = rhythm_df[rhythm_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

# Sort by date in descending order
columns_to_display = ['days_since_rhythm_date', 'rhythm_date', 'weekday', 'activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']

sorted_prompt = filter_by_user_prompt.sort_values(by='rhythm_date', ascending=False)[columns_to_display].drop_duplicates()

# Display the dataframe
st.dataframe(sorted_prompt, use_container_width=True)