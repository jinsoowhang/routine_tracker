import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta
from src.helpers.openai_helper import ask_openai_chat

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_body_weight_tracker(shared_start_date, shared_end_date):

    # Perform query.
    body_weight_df = conn.query("""
        SELECT 
            rhythm_date,
            body_weight
        FROM public.stg__journal
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

    #####################
    ###### Ask AI #######
    #####################

    st.markdown("## 💬 Ask AI Assistant")

    ask_ai_key = 'ask_ai_button_health_tracker'

    user_question = st.text_input(
                        "Enter your question (e.g. 'What is my weight trend?')",
                        key=f'{ask_ai_key}_1'
                        )

    if st.button("Ask AI", key=f'{ask_ai_key}_2'):
        if not user_question:
            st.warning("Please enter a question.")
        elif body_weight_df.empty:
            st.warning("No journal data available to provide context.")
        else:
            with st.spinner("Getting AI response..."):
                answer = ask_openai_chat(user_question, context_df=body_weight_df)
            st.success("AI response:")
            st.write(answer)