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

st.title("""📈Gym Routine""")

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

############################################
####### Bar Chart: Activity by week ########
############################################

activity_by_week_df = df[['week_start_date', 'had_activity']].groupby('week_start_date').sum('had_activity')

st.bar_chart(activity_by_week_df)

st.divider()

####################################
####### Tennis Head to Head ########
####################################

st.title("""🎾Tennis Head2Head""")

st.divider()

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

