import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM fct__all_dates_activity;', ttl="10m")
tennis_results_df = conn.query('SELECT * FROM fct__tennis_results;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🏋️Gym Schedule""")

st.divider()

##############################
####### Data Cleaning ########
##############################

df['calendar_date'] = pd.to_datetime(df['calendar_date'])

########################
####### Filters ########
########################

df['first_active_date'] = df['calendar_date']
start_dt = st.sidebar.date_input('From Date', value=df['first_active_date'].min())

df['last_active_date'] = df['calendar_date']
end_dt = st.sidebar.date_input('To Date', value=df['last_active_date'].max())

df = df[(df['calendar_date'] >= pd.to_datetime(start_dt)) & (df['calendar_date'] <= pd.to_datetime(end_dt))]

####################################################
####### Stacked Bar Chart: Activity by week ########
####################################################

# Activity type filter columns
list_of_activity_type = [col for col in df.type_of_activity.unique().tolist()]

activity_filter = st.multiselect('Select Activity', options=list_of_activity_type, default=list_of_activity_type)

activity_by_week_df = df[df['type_of_activity'].isin(activity_filter)]

# Create the Altair chart
chart = alt.Chart(activity_by_week_df).mark_bar().encode(
    x=alt.X('week_start_date:T', title='Week Start Date'),
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
    title='Activity Counts'
)

# Display the chart in Streamlit
st.altair_chart(chart_2, use_container_width=True)

####################################
####### Tennis Head to Head ########
####################################

st.title("""🎾Tennis Head2Head""")

st.divider()

tennis_match_type = st.radio(
    "Select tennis match type",
    ['singles', 'doubles'],
    index=None,
)

if tennis_match_type == 'singles':
    opponent_doubles_stats = tennis_results_df[tennis_results_df['is_teammate'] == 1]
elif tennis_match_type == 'doubles':
    opponent_doubles_stats = tennis_results_df[tennis_results_df['is_teammate'] == 0]
else: 
    opponent_doubles_stats = tennis_results_df[tennis_results_df['is_teammate'] == 0]

# Group by player_name and count wins and losses
player_stats = opponent_doubles_stats.groupby('player_name')['result'].value_counts().unstack(fill_value=0)

# Rename columns to number_of_wins and number_of_losses
player_stats.columns = ['number_of_losses', 'number_of_wins']  # Assuming result is 'loss' and 'win'

# Calculate the win_loss_difference
player_stats['win_loss_difference'] = player_stats['number_of_wins'] - player_stats['number_of_losses']

# Calculate win rate
player_stats['win_rate'] = player_stats['number_of_wins'] / (player_stats['number_of_wins'] + player_stats['number_of_losses'])

# Reset index for better readability
player_stats = player_stats.reset_index()

# Show the dataframe
st.write(player_stats)
######################
####### Table ########
######################

st.markdown(f"This is the table")

st.write(df)

