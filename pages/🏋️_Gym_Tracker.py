import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt
from datetime import timedelta

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM fct__all_dates_activity;', ttl="10m")

gym_exercises_df = conn.query('SELECT * FROM fct__gym_exercises;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🏋️Gym Tracker""")

st.divider()

st.markdown("## Activity Counts")

##############################
####### Data Cleaning ########
##############################

df['calendar_date'] = pd.to_datetime(df['calendar_date'])

########################
####### Filters ########
########################

# Calculate the default start and end dates
default_end_date = dt.today()
default_start_date = default_end_date - timedelta(days=30)

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
df = df[
    (df['calendar_date'] >= pd.to_datetime(start_dt)) &
    (df['calendar_date'] <= pd.to_datetime(end_dt))
]

####################################################
####### Stacked Bar Chart: Activity by week ########
####################################################

# Activity type filter columns
list_of_activity_type = [col for col in df.type_of_activity.unique().tolist()]

activity_filter = st.multiselect('Select Activity', options=list_of_activity_type, default=list_of_activity_type)

activity_by_week_df = df[df['type_of_activity'].isin(activity_filter)]

# Create the Altair chart
chart = alt.Chart(activity_by_week_df).mark_bar().encode(
    x=alt.X('week_start_date:T', title='Week Start Date', axis=alt.Axis(format='%b %d %y')),  # Format as "Jan 2024"
    y=alt.Y('had_activity:Q', title='Had Activity'),
    color=alt.Color('type_of_activity:N', title='Type of Activity')
).properties(
    width=800,
    height=400,
    title='Stacked Bar Chart of Weekly Activities'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)

#############################################
####### Bar Chart: Count by Activity ########
#############################################

# Aggregate the count of activities
activity_count_df = df.groupby('type_of_activity')['had_activity'].sum().reset_index()
activity_count_df.columns = ['Activity', 'Count']

# Create a horizontal bar chart using Altair
chart_2 = alt.Chart(activity_count_df).mark_bar().encode(
    x='Count:Q',
    y=alt.Y('Activity:N', sort='-x'),
    color='Activity:N'
).properties(
    width=600,
    height=400,
    title='Bar Chart by Activity Type'
)

# Display the chart in Streamlit
st.altair_chart(chart_2, use_container_width=True)

st.divider()

########################################
####### Weight Lifting Progress ########
########################################

st.markdown("## Weight Lifting")

# User chooses gym exercise type
gym_exercise_type_selection = st.pills(
    "Gym Exercise Type",
    options=gym_exercises_df['gym_exercise_type'].str.strip().unique(),
    selection_mode="single"
)

# Filter data based on gym date and exercise type
gym_exercise_date_filter = (gym_exercises_df['gym_date'] >= start_dt) & (gym_exercises_df['gym_date'] <= end_dt)
gym_exercise_type_filter = (gym_exercises_df['gym_exercise_type'].str.strip() == gym_exercise_type_selection)

# Apply filters to the dataframe
gym_exercises_filtered = gym_exercises_df[gym_exercise_date_filter & gym_exercise_type_filter]

# Create the Altair chart
chart_3 = alt.Chart(gym_exercises_filtered).mark_bar().encode(
    x=alt.X('gym_date:T', title='Gym Date', axis=alt.Axis(format='%b %d %y')),  # Format as "Apr 25 2022"
    y=alt.Y('sum(gym_exercise_repetitions):Q', title='Total Reps'),  # Sum of reps
    color=alt.Color('gym_exercise_weight:N', title='Gym Exercise Type', legend=alt.Legend(title="Gym Exercise Type")),
    tooltip=['gym_date:T', 'gym_exercise_weight:N', alt.Tooltip('sum(gym_exercise_repetitions):Q', title='Total Reps')]
).properties(
    width=800,
    height=400,
    title='Sum of Weekly Weight Lifting Reps'
)

# Display the chart in Streamlit
st.altair_chart(chart_3, use_container_width=True)
