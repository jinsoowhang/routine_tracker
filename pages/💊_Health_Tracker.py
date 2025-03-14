import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
body_weight_df = conn.query("""
    SELECT 
        rhythm_date,
        body_weight
    FROM public.fct__other_rhythm_tracking
    WHERE body_weight IS NOT NULL;
""", ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""💊 Health Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

body_weight_df['rhythm_date'] = pd.to_datetime(body_weight_df['rhythm_date'])

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
body_weight_df = body_weight_df[
    (body_weight_df['rhythm_date'] >= pd.to_datetime(start_dt)) &
    (body_weight_df['rhythm_date'] <= pd.to_datetime(end_dt))
]

####################################
####### Body Weight Tracker ########
####################################

st.markdown("## Body Weight Over Time")

chart_1 = alt.Chart(body_weight_df).mark_line().encode(
    x = alt.X('rhythm_date'),
    y = alt.Y('body_weight', scale=alt.Scale(domain=[140, 160]))
)

# Display the chart in Streamlit
st.altair_chart(chart_1, use_container_width=True)

#################################
####### Last 5 Weigh Ins ########
#################################

st.markdown("## Last 5 Weigh Ins")

# Display the table
st.dataframe(body_weight_df.sort_values(by='rhythm_date', ascending=False).head(5), hide_index=True)