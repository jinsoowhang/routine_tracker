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

##############################
####### Data Cleaning ########
##############################

# Convert to datetime
daily_activity_scores_df['adj_rhythm_date'] = pd.to_datetime(daily_activity_scores_df['adj_rhythm_date'], format='%Y%m%d')

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


##########################
####### Variables ########
##########################

# Group by adj_year_week_num to get weekly scores
weekly_activity_scores_df = daily_activity_scores_df.groupby('adj_year_week_num')['total_daily_score'].mean()

# Today vs One week ago scores
today_date = dt.today().date()
one_week_ago_date = today_date - timedelta(days=7)
today_score = daily_activity_scores_df[daily_activity_scores_df['adj_rhythm_date'].dt.date == today_date]['total_daily_score'].iloc[0]
one_week_ago_score = daily_activity_scores_df[daily_activity_scores_df['adj_rhythm_date'].dt.date == one_week_ago_date]['total_daily_score'].iloc[0]

# This week vs Last week score
this_week_num = today_date.strftime("%Y-W%U")  # Format as YYYY-Wxx
last_week_num = (today_date - timedelta(weeks=1)).strftime("%Y-W%U")  # Previous week in YYYY-Wxx format
this_week_score = weekly_activity_scores_df.loc[this_week_num] if this_week_num in weekly_activity_scores_df.index else None
last_week_score = weekly_activity_scores_df.loc[last_week_num] if last_week_num in weekly_activity_scores_df.index else None
# Round the scores to 1 decimal place
this_week_score_rounded = round(this_week_score, 1) if this_week_score is not None else None
last_week_score_rounded = round(last_week_score, 1) if last_week_score is not None else None

###############################
####### Activity Score ########
###############################

st.markdown("## Activity Score")

# Today vs One week ago scores
if today_score > one_week_ago_score:
    st.markdown(
        f"Today's score is <b style='color:yellow; font-size:35px;'>{today_score}</b> and "
        f"last week's score was <b style='color:orange; font-size:35px;'>{one_week_ago_score}"
        f" <b style='color:green; font-size:25px;'>(🔼{round(today_score-one_week_ago_score, 1)})</b>",
        unsafe_allow_html=True
    )
elif today_score < one_week_ago_score:
    st.markdown(
        f"Today's score is <b style='color:yellow; font-size:35px;'>{today_score}</b> and "
        f"last week's score was <b style='color:orange; font-size:35px;'>{one_week_ago_score}"
        f" <b style='color:red; font-size:25px;'>(🔻{round(today_score-one_week_ago_score, 1)})</b>",
        unsafe_allow_html=True
    )
else: 
    pass

# This week vs Last week score with conditional display
if this_week_score_rounded is not None and last_week_score_rounded is not None:
    if this_week_score_rounded > last_week_score_rounded:
        st.markdown(
            f"This week's score is <b style='color:yellow; font-size:35px;'>{this_week_score_rounded}</b> and "
            f"last week's score was <b style='color:orange; font-size:35px;'>{last_week_score_rounded}"
            f" <b style='color:green; font-size:25px;'>(🔼{round(this_week_score_rounded-last_week_score_rounded, 1)})</b>",
            unsafe_allow_html=True
        )
    elif this_week_score_rounded < last_week_score_rounded:
        st.markdown(
            f"This week's score is <b style='color:yellow; font-size:35px;'>{this_week_score_rounded}</b> and "
            f"last week's score was <b style='color:orange; font-size:35px;'>{last_week_score_rounded}"
            f" <b style='color:red; font-size:25px;'>(🔻{round(this_week_score_rounded-last_week_score_rounded, 1)})</b>",
            unsafe_allow_html=True
        )
    else:
        pass
else:
    st.markdown("One or both of the weekly scores are not available.")

st.divider()

# Line Chart for daily score over time
line_chart = alt.Chart(daily_activity_scores_df).mark_line().encode(
    x = alt.X('adj_rhythm_date'),
    y = alt.Y('total_daily_score', scale=alt.Scale(domain=[0, 120]), title='Total Daily Score'),
    tooltip=['adj_rhythm_date:T', 'adj_weekday:N', 'adj_year_week_num:N', 'total_daily_score:Q']  # Add adj_year_week_num to the tooltip
)

# Text labels
labels = alt.Chart(daily_activity_scores_df).mark_text(align='left', dx=-10, dy=-10, fontSize=12, color='white').encode(
    x=alt.X('adj_rhythm_date:T'),
    y=alt.Y('total_daily_score:Q'),
    text=alt.Text('total_daily_score:Q', format=".1f")  # Round the score to 1 decimal place
)

# Combine the line chart and labels with a title
chart_1 = (line_chart + labels).properties(
    title="Daily Score Over Time",
    width=800,  # Optional: Adjust width
    height=400  # Optional: Adjust height
)

# Display the chart in Streamlit
st.altair_chart(chart_1, use_container_width=True)
st.divider()

######################################
####### Weekly Scores by Day ########
######################################

# Heatmap to represent the scores
heatmap = alt.Chart(daily_activity_scores_df).mark_rect().encode(
    x=alt.X(
        'adj_weekday:N',
        title='Weekday',
        sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']  # Explicit order
    ),
    y=alt.Y('adj_year_week_num:N', title='Year-Week'),
    color=alt.Color('total_daily_score:Q', scale=alt.Scale(scheme='redyellowgreen'), title='Daily Score'),
    tooltip=['adj_year_week_num:N', 'adj_weekday:N', 'total_daily_score:Q']  # Tooltip for details
)

# Text labels for each grid cell
text = alt.Chart(daily_activity_scores_df).mark_text(align='center', baseline='middle', fontSize=12, color='white').encode(
    x=alt.X(
        'adj_weekday:N',
        sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']  # Explicit order
    ),
    y=alt.Y('adj_year_week_num:N'),
    text=alt.Text('total_daily_score:Q', format=".0f")  # Format to display whole numbers
)

# Combine the heatmap and text labels
grid_chart = (heatmap + text).properties(
    title="Weekly Scores by Day",
    width=800,  # Adjust width for better readability
    height=400   # Adjust height for better readability
)

# Display the chart in Streamlit
st.altair_chart(grid_chart, use_container_width=True)

######################################
####### Overall Activity KPIs ########
######################################

st.markdown("## Overall Activity KPIs")

# Create two columns
col1, col2 = st.columns(2)

# Column 1: Overall Activity KPIs and Average Score by Day
with col1:
    st.markdown("##### Average score by day")
    result = (
        daily_activity_scores_df.groupby(['adj_weekday', 'adj_day_num'])['total_daily_score']
        .mean()
        .reset_index()  # Convert the Series to a DataFrame
        .sort_values(by='adj_day_num').reset_index()  # Sort by 'adj_day_num'
    )
    st.dataframe(result[['adj_weekday', 'total_daily_score']])

# Column 2: Average Score by Week
with col2:
    st.markdown("##### Average score by week")
    st.dataframe(weekly_activity_scores_df)

# Divider below the columns
st.divider()