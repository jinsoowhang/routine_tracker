import streamlit as st
import pandas as pd
from datetime import datetime as dt
from src.helpers.openai_helper import ask_openai_chat

# Initialize connection
conn = st.connection("postgresql", type="sql")

def render_todo_tracker(start_dt, end_dt):
    # Perform query
    todo_df = conn.query("""
        SELECT 
            todo_id,
            creation_date,
            category,
            description,
            status,
            priority,
            completion_date,
            notes
        FROM stg__todo
        ORDER BY creation_date;
    """, ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("📋 TODO Tracker")

    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    # Convert creation_date to datetime
    todo_df['creation_date'] = pd.to_datetime(todo_df['creation_date'], format='mixed')

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame to include only the selected date range
    todo_df = todo_df[
        (todo_df['creation_date'] >= pd.to_datetime(start_dt)) & 
        (todo_df['creation_date'] <= pd.to_datetime(end_dt))
    ]

    ######################
    ####### TODOs ########
    ######################

    st.markdown('## TODO Table')

    st.dataframe(todo_df)

    #####################
    ###### Ask AI #######
    #####################

    st.markdown("## 💬 Ask AI Assistant")

    ask_ai_key = 'ask_ai_button_todo_tracker'

    user_question = st.text_input(
                        "Enter your question (e.g. 'What are my most common TODO tasks?')",
                        key=f'{ask_ai_key}_1'
                        )

    if st.button("Ask AI", key=f'{ask_ai_key}_2'):
        if not user_question:
            st.warning("Please enter a question.")
        elif todo_df.empty:
            st.warning("No journal data available to provide context.")
        else:
            with st.spinner("Getting AI response..."):
                answer = ask_openai_chat(user_question, context_df=todo_df)
            st.success("AI response:")
            st.write(answer)