import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta
from src.helpers.openai_helper import ask_openai_chat

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_food_tracker(shared_start_date, shared_end_date):
    
    # Perform query.
    df = conn.query("""
        SELECT *
        FROM public.stg__food;
    """, ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("""🍽️ Food Tracker""")
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

    df = df.sort_values(by='rhythm_date', ascending=False)

    ##############################
    ####### Food Tracker #########
    ##############################

    # Filters
    st.markdown("## Filters")
    filter_columns = {
        "Food Activity": "food_activity",
        "Meal of Day": "meal_of_day",
        "Food": "food",
        "Restaurant": "restaurant"
    }

    filters = {}
    with st.container():
        cols = st.columns(len(filter_columns))
        for i, (label, column) in enumerate(filter_columns.items()):
            with cols[i]:
                sorted_values = sorted(df[column].dropna().unique().tolist())
                filters[column] = st.selectbox(
                    label,
                    options=["All"] + sorted_values,
                    index=0
                )

    filtered_df = df.copy()
    for column, selected_value in filters.items():
        if selected_value != "All":
            filtered_df = filtered_df[filtered_df[column] == selected_value]

    st.divider()

    st.markdown("## Food Table")

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    #####################
    ###### Ask AI #######
    #####################

    st.markdown("## 💬 Ask AI Assistant")

    ask_ai_key = 'ask_ai_button_food_tracker'

    user_question = st.text_input(
                        "Enter your question (e.g. 'What are my most common meals?')",
                        key=f'{ask_ai_key}_1'
                        )

    if st.button("Ask AI", key=f'{ask_ai_key}_2'):
        if not user_question:
            st.warning("Please enter a question.")
        elif filtered_df.empty:
            st.warning("No journal data available to provide context.")
        else:
            with st.spinner("Getting AI response..."):
                answer = ask_openai_chat(user_question, context_df=filtered_df)
            st.success("AI response:")
            st.write(answer)