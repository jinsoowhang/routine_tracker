import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_body_weight_tracker(shared_start_date, shared_end_date):

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

    # Filter the DataFrame to include only the selected date range from the wellness tracker
    body_weight_df = body_weight_df[
        (body_weight_df['rhythm_date'] >= pd.to_datetime(shared_start_date)) &
        (body_weight_df['rhythm_date'] <= pd.to_datetime(shared_end_date))
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
