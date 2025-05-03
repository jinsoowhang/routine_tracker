import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_sleep_tracker(shared_start_date, shared_end_date):

    # Perform query.
    df = conn.query("""
        SELECT 
            rhythm_date,
            sleep_score
        FROM public.stg__journal
        WHERE sleep_score IS NOT NULL;
    """, ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("""😴 Sleep Tracker""")
    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    df['rhythm_date'] = pd.to_datetime(df['rhythm_date'])

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame to include only the selected date range from the wellness tracker
    df = df[
        (df['rhythm_date'] >= pd.to_datetime(shared_start_date)) &
        (df['rhythm_date'] <= pd.to_datetime(shared_end_date))
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
