# pages/tennis_tracker.py

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt, timedelta

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_tennis_tracker(start_date, end_date, date_prefix=""):

    ###########################
    ####### Title Page ########
    ###########################

    st.title("""🎾 Tennis Tracker""")
    st.divider()

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

    tennis_results_df['match_date'] = pd.to_datetime(tennis_results_df['match_date'])
    tennis_match_results_df['match_date'] = pd.to_datetime(tennis_match_results_df['match_date'])

    # Filter data based on the shared start_date and end_date
    date_filtered_tennis_results_df = tennis_results_df[
        (tennis_results_df['match_date'] >= pd.to_datetime(start_date)) &
        (tennis_results_df['match_date'] <= pd.to_datetime(end_date))
    ]

    date_filtered_tennis_match_results_df = tennis_match_results_df[
        (tennis_match_results_df['match_date'] >= pd.to_datetime(start_date)) &
        (tennis_match_results_df['match_date'] <= pd.to_datetime(end_date))
    ]

    st.markdown("## 🎾 Tennis Recent Form")
    st.dataframe(date_filtered_tennis_match_results_df)

    st.markdown("## 🎾 Head2Head")

    filter_columns = {
        "Player Name": "player_name",
        "Is Teammate": "is_teammate"
    }

    filters = {}
    cols = st.columns(len(filter_columns))
    for i, (label, column) in enumerate(filter_columns.items()):
        with cols[i]:
            filters[column] = st.selectbox(
                label,
                options=["All"] + date_filtered_tennis_results_df[column].dropna().unique().tolist(),
                index=0,
                key=f"{date_prefix}{column}"
            )

    filtered_df = date_filtered_tennis_results_df.copy()
    for column, selected_value in filters.items():
        if selected_value != "All":
            filtered_df = filtered_df[filtered_df[column] == selected_value]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.markdown("## 🎾 W/L Record")

    col1, col2, _, _ = st.columns(4)

    with col1:
        tennis_match_type = st.radio(
            "Match type", ['doubles', 'singles'],
            index=0,
            key=f"{date_prefix}match_type"
        )
    with col2:
        tennis_player_role = st.radio(
            "Player role", ['opponent', 'teammate'],
            index=0,
            key=f"{date_prefix}player_role"
        )

    match_type_df = filtered_df[filtered_df['match_type'] == tennis_match_type]

    if tennis_player_role == 'teammate':
        opponent_stats = match_type_df[match_type_df['is_teammate'] == 1]
    else:
        opponent_stats = match_type_df[match_type_df['is_teammate'] == 0]

    if opponent_stats.empty:
        st.info("No data available for selected filters.")
        return

    player_stats = opponent_stats.groupby('player_name')['result'].value_counts().unstack(fill_value=0)
    player_stats.columns = ['number_of_losses', 'number_of_wins']
    player_stats['win_loss_difference'] = player_stats['number_of_wins'] - player_stats['number_of_losses']
    player_stats['win_rate (%)'] = (
        player_stats['number_of_wins'] / 
        (player_stats['number_of_wins'] + player_stats['number_of_losses'])
    ) * 100
    player_stats = player_stats.reset_index()

    st.dataframe(player_stats, use_container_width=True, hide_index=True)
