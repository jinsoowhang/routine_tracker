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
tennis_results_df = conn.query('SELECT * FROM fct__tennis_results;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🎾Tennis Tracker""")

st.divider()

####################################
####### Tennis Head to Head ########
####################################

st.title("""🎾Tennis Head2Head""")

st.divider()

tennis_match_type = st.radio(
    "Select player role",
    ['teammate', 'opponent'],
    index=None,
)

if tennis_match_type == 'teammate':
    opponent_doubles_stats = tennis_results_df[tennis_results_df['is_teammate'] == 1]
elif tennis_match_type == 'opponent':
    opponent_doubles_stats = tennis_results_df[tennis_results_df['is_teammate'] == 0]
else: 
    opponent_doubles_stats = tennis_results_df[tennis_results_df['is_teammate'] == 0]

# Group by player_name and count wins and losses
player_stats = opponent_doubles_stats.groupby('player_name')['result'].value_counts().unstack(fill_value=0)

# Rename columns to number_of_wins and number_of_losses
player_stats.columns = ['number_of_losses', 'number_of_wins']  # Assuming result is 'loss' and 'win'

# Calculate the win_loss_difference
player_stats['win_loss_difference'] = player_stats['number_of_wins'] - player_stats['number_of_losses']

# Calculate win rate and format as percentage
player_stats['win_rate (%)'] = (
    player_stats['number_of_wins'] / 
    (player_stats['number_of_wins'] + player_stats['number_of_losses'])
) * 100

# Reset index for better readability
player_stats = player_stats.reset_index()

# Show the dataframe
st.dataframe(player_stats, use_container_width=True)
