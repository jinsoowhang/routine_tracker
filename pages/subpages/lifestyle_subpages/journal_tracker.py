import streamlit as st
import pandas as pd
from datetime import datetime as dt
from src.helpers.openai_helper import ask_openai_chat

# Initialize connection
conn = st.connection("postgresql", type="sql")

def render_journal_tracker(start_dt, end_dt):
    # Perform query
    journal_df = conn.query("""
        SELECT 
            rhythm_date,
            highlight,
            lowlight,
            dream,
            lesson
        FROM stg__journal;
    """, ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("📓 Journal Tracker")

    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    # Convert journal_date to datetime
    journal_df['rhythm_date'] = pd.to_datetime(journal_df['rhythm_date'], format='%Y%m%d')

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame to include only the selected date range
    journal_df = journal_df[
        (journal_df['rhythm_date'] >= pd.to_datetime(start_dt)) & 
        (journal_df['rhythm_date'] <= pd.to_datetime(end_dt))
    ]

    ##############################
    ####### Track Journal ########
    ##############################

    st.markdown('## Track Journal Entries')

    # User Input
    journal_entry_prompt = st.text_input("Write your journal entry")

    # Create a new column to concatenate all relevant columns
    columns_to_concatenate = journal_df.columns

    journal_df['concatenated_values'] = journal_df[columns_to_concatenate].astype(str).apply(
        lambda row: ' | '.join(row.values), axis=1
    )

    # Filter data by user input
    filter_by_entry = journal_df[journal_df['concatenated_values'].str.lower().str.contains(journal_entry_prompt, na=False)]

    # Display the filtered journal entries
    st.write(f"Found {len(filter_by_entry)} journal entries matching your input")

    ###############################
    ####### Journal Table ########
    ###############################

    st.markdown('## Journal Table')

    # Display the filtered journal entries
    st.dataframe(filter_by_entry, use_container_width=True, hide_index=True)

    st.divider()

    #####################
    ###### Ask AI #######
    #####################

    st.markdown("## 💬 Ask AI Assistant")

    ask_ai_key = 'ask_ai_button_journal_tracker'

    user_question = st.text_input(
                        "Enter your question (e.g. 'What are my most common highlights?')",
                        key=f'{ask_ai_key}_1'
                        )

    if st.button("Ask AI", key=f'{ask_ai_key}_2'):
        if not user_question:
            st.warning("Please enter a question.")
        elif journal_df.empty:
            st.warning("No journal data available to provide context.")
        else:
            with st.spinner("Getting AI response..."):
                answer = ask_openai_chat(user_question, context_df=journal_df)
            st.success("AI response:")
            st.write(answer)