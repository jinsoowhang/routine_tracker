import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query("""
    SELECT 
        rhythm_date,
        sleep_score
    FROM public.fct__other_rhythm_tracking
    WHERE sleep_score IS NOT NULL;
""", ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""💤 Sleep Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

df['rhythm_date'] = pd.to_datetime(df['rhythm_date'])

########################
####### Filters ########
########################

# Calculate the default start and end dates
default_end_date = dt.today()
default_start_date = default_end_date - timedelta(days=365)

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
df = df[
    (df['rhythm_date'] >= pd.to_datetime(start_dt)) &
    (df['rhythm_date'] <= pd.to_datetime(end_dt))
]

##############################
####### Sleep Tracker ########
##############################

st.markdown("## Sleep Score Over Time")

chart_1 = alt.Chart(df).mark_line().encode(
    x = alt.X('rhythm_date'),
    y = alt.Y('sleep_score')  # Let Altair handle the scale automatically
)

# Display the chart in Streamlit
st.altair_chart(chart_1, use_container_width=True)