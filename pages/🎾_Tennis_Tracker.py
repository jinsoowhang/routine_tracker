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

# Perform query
query_1 = """
SELECT 
    matches.gym_date AS match_date,
    results.player_name,
    results.score,
    results.result,
    matches.teammate,
    matches.opponents,
    matches.match_type,
    results.is_teammate,
    results.match_id
FROM fct__tennis_results results
JOIN fct__tennis_matches matches
    ON results.match_id = matches.match_id;
"""

query_2 = """
SELECT distinct
    matches.gym_date AS match_date,
    results.result,
    matches.score,
    matches.teammate,
    matches.opponents,
    matches.match_type,
    matches.match_id
FROM fct__tennis_matches matches
LEFT JOIN fct__tennis_results results
        ON results.match_id = matches.match_id;
"""

tennis_results_df = conn.query(query_1, ttl="10m")

tennis_match_results_df = conn.query(query_2, ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🎾Tennis Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

tennis_results_df['match_date'] = pd.to_datetime(tennis_results_df['match_date'])
tennis_match_results_df['match_date'] = pd.to_datetime(tennis_match_results_df['match_date'])

# Calculate the default start and end dates
default_end_date = dt.today()
default_start_date = default_end_date - timedelta(days=365)

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
date_filtered_tennis_results_df = tennis_results_df[
    (tennis_results_df['match_date'] >= pd.to_datetime(start_dt)) &
    (tennis_results_df['match_date'] <= pd.to_datetime(end_dt))
]

date_filtered_tennis_match_results_df = tennis_match_results_df[
    (tennis_match_results_df['match_date'] >= pd.to_datetime(start_dt)) &
    (tennis_match_results_df['match_date'] <= pd.to_datetime(end_dt))
]

###################################
####### Tennis Recent Form ########
###################################

st.title("""🎾Tennis Recent Form""")

st.divider()

st.dataframe(date_filtered_tennis_match_results_df)

####################################
####### Tennis Head to Head ########
####################################

tennis_head2head_df = date_filtered_tennis_results_df.copy()

st.title("""🎾Tennis Head2Head""")

st.divider()

# Define the columns and corresponding filter names
filter_columns = {
    "Player Name": "player_name"
    ,"Is Teammate": "is_teammate"
}

# Create the filters dynamically
filters = {}
with st.container():
    cols = st.columns(len(filter_columns))  # Create the necessary number of columns
    for i, (label, column) in enumerate(filter_columns.items()):
        with cols[i]:
            filters[column] = st.selectbox(
                label,
                options=["All"] + tennis_head2head_df[column].unique().tolist(),
                index=0
           )

# Apply filters dynamically
filtered_df = tennis_head2head_df.copy()
for column, selected_value in filters.items():
    if selected_value != "All":
        filtered_df = filtered_df[filtered_df[column] == selected_value]

st.dataframe(filtered_df, use_container_width=True, hide_index=True)

##################################
####### Tennis W/L Record ########
##################################

st.title("""🎾Tennis W/L Record""")

st.divider()

# Create two columns for filter
col1, col2, col3, col4 = st.columns(4)

# Column 1: Overall Activity KPIs and Average Score by Day
with col1:
    tennis_match_type = st.radio(
    "Select match type",
    ['doubles', 'singles'],
    index=0,
    )
# Column 2: Average Score by Week
with col2:
    tennis_player_role = st.radio(
        "Select player role",
        ['opponent', 'teammate'],
        index=0,
    )

# Column 3 & 4 are empty and it is used for spacing purposes
with col3:
    pass
with col4:
    pass

# Filter by match type
match_type_df = tennis_head2head_df[tennis_head2head_df['match_type'] == tennis_match_type]

# Filter by player role
if tennis_player_role == 'teammate':
    opponent_doubles_stats = match_type_df[match_type_df['is_teammate'] == 1]
elif tennis_player_role == 'opponent':
    opponent_doubles_stats = match_type_df[match_type_df['is_teammate'] == 0]
else: 
    opponent_doubles_stats = match_type_df[match_type_df['is_teammate'] == 0]

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
st.dataframe(player_stats, use_container_width=True, hide_index=True)
