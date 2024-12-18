import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

# Initialize connection
conn = st.connection("postgresql", type="sql")

# Perform query.
daily_activity_scores_df = conn.query('SELECT * FROM fct__daily_activity_scores;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🌱Habit Tracker""")

st.divider()

##########################
####### Variables ########
##########################

# Convert to date
today_date = dt.today().date()
one_week_ago_date = today_date - timedelta(days=7)
daily_activity_scores_df['adj_rhythm_date'] = pd.to_datetime(daily_activity_scores_df['adj_rhythm_date'], format='%Y%m%d')

today_score = daily_activity_scores_df[daily_activity_scores_df['adj_rhythm_date'].dt.date == today_date]['total_daily_score'].iloc[0]
one_week_ago_score = daily_activity_scores_df[daily_activity_scores_df['adj_rhythm_date'].dt.date == one_week_ago_date]['total_daily_score'].iloc[0]

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
daily_activity_scores_df = daily_activity_scores_df[
    (daily_activity_scores_df['adj_rhythm_date'] >= pd.to_datetime(start_dt)) &
    (daily_activity_scores_df['adj_rhythm_date'] <= pd.to_datetime(end_dt))
]

###############################
####### Activity Score ########
###############################

st.markdown("## Activity Score")

st.write(f"Today's score:          {today_score}")
st.write(f"One week ago score:          {one_week_ago_score}")

chart_1 = alt.Chart(daily_activity_scores_df).mark_line().encode(
    x = alt.X('adj_rhythm_date'),
    y = alt.Y('total_daily_score', scale=alt.Scale(domain=[0, 120]))
)

# Display the chart in Streamlit
st.altair_chart(chart_1, use_container_width=True)

st.divider()

######################################
####### Overall Activity KPIs ########
######################################

st.markdown("## Overall Activity KPIs")

st.markdown("##### Average score by day")

result = (
    daily_activity_scores_df.groupby(['adj_weekday', 'adj_day_num'])['total_daily_score']
    .mean()
    .reset_index()  # Convert the Series to a DataFrame
    .sort_values(by='adj_day_num').reset_index()  # Sort by 'adj_day_num'
)

st.write(result[['adj_weekday', 'total_daily_score']])

st.divider()

#########################
####### Appendix ########
#########################

# dfu_weekly['rating'] = dfu_weekly['rating']/7

# # Get the current year and week number
# current_date = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
# current_year = current_date.isocalendar().year
# this_week = f"{current_year}-W{current_date.isocalendar().week:02d}"  # Ensure two-digit week number

# # Formula for weekly ranking
# weekly_ranking = dfu_weekly.copy()
# weekly_ranking['week_ranking'] = weekly_ranking['rating'].rank(ascending=False)

# # Print this week's Score
# try:
#     current_week_data = weekly_ranking.loc[this_week]

#     week_score = round(float(current_week_data['rating']), 1)
#     week_rank = int(current_week_data['week_ranking'])
#     total_weeks = int(weekly_ranking['week_ranking'].max())

#     # Calculate percentile
#     percentile = (1 - (week_rank / total_weeks)) * 100

#     st.write(f"Week {this_week} score:          {week_score}")
#     st.write(f"Week {this_week} all-time Rank:  {week_rank} out of {total_weeks}")
#     st.write(f"Week {this_week} Percentile:     {percentile:.2f}%")

# except KeyError:
#     st.write(f"No data available for Week {this_week}.")

# st.divider()