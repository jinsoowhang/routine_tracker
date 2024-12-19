import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt
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

##############################
####### Data Cleaning ########
##############################

# Convert to datetime
rhythm_df['rhythm_date'] = pd.to_datetime(rhythm_df['rhythm_date'], format='%Y%m%d')

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

##############################################
####### Last Occurrence of Activity X ########
##############################################

st.title('Last Occurrence of Activity X')

# User Input
last_activity_prompt = st.text_input("Write the activity you want to track in lowercase 👇")

# Filter data by user input
filter_by_user_prompt = rhythm_df[rhythm_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

# Display the amount of time spent in this activity
activity_hours_spent = int(len(filter_by_user_prompt)/4)
activity_days_spent = int(activity_hours_spent/24)
activity_proportion_spent = round(len(filter_by_user_prompt) / len(rhythm_df) * 100, 1)

if last_activity_prompt == '':
    st.write('There is no input from user. Please write the activity in text box ☝️')
else: 
    st.write(f'All time {'"'+str(last_activity_prompt)+'"'} duration: {activity_hours_spent} hours or {activity_days_spent} days, accounts for {activity_proportion_spent}% of total activities')

# Sort by date in descending order
columns_to_display = ['days_since_rhythm_date', 'rhythm_date', 'weekday', 'activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']

sorted_prompt = filter_by_user_prompt.sort_values(by='rhythm_date', ascending=False)[columns_to_display]

# Display the dataframe
st.dataframe(sorted_prompt, use_container_width=True)

# Example data (replace with your actual DataFrame)
# rhythm_date and attribute_1 should exist in your dataframe
stacked_bar_chart = alt.Chart(sorted_prompt).mark_bar().encode(
    x=alt.X('rhythm_date:T', title='Rhythm Date'),
    y=alt.Y('count()', title='Count of Activities'),
    color=alt.Color('attribute_1:N', title='Activity Type'),  # Stacks by activity type
    tooltip=['rhythm_date:T', 'attribute_1:N', 'count()']  # Add tooltips
).properties(
    title='Activity Distribution by Date',
    width=800,
    height=400
)

# Display the chart in Streamlit
st.altair_chart(stacked_bar_chart, use_container_width=True)

####################################
####### Activity Proportion ########
####################################

st.title("""High Level Activities""")

activity_hierarchy = st.selectbox(
    "Select activity hierarchy",
    ['attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places']
)

# Calculate proportions and total hours/days
activity_proportion_df = rhythm_df[['activity_id', activity_hierarchy]].groupby(activity_hierarchy).size().reset_index(name='count')

# Add total hours and days
activity_proportion_df['total_hours'] = round(activity_proportion_df['count'] / 4)
activity_proportion_df['total_days'] = round(activity_proportion_df['total_hours'] / 24)
activity_proportion_df['proportion (%)'] = round(activity_proportion_df['count'] / activity_proportion_df['count'].sum() * 100, 1)

# Reorder columns
activity_proportion_df = activity_proportion_df[[activity_hierarchy, 'total_hours', 'total_days', 'proportion (%)']]

# Display in Streamlit
st.write(activity_proportion_df)
    
st.divider()