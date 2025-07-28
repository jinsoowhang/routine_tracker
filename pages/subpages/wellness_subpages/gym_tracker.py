import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta
from src.helpers.openai_helper import ask_openai_chat

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_gym_tracker(shared_start_date, shared_end_date, date_prefix="gym_"):

    # Perform query.
    df = conn.query('SELECT * FROM fct__all_dates_activity;', ttl="10m")
    gym_exercises_df = conn.query('SELECT * FROM fct__gym_exercises;', ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("""🏋️ Gym Tracker""")
    st.divider()
    st.markdown("## Activity Counts")

    ##############################
    ####### Data Cleaning ########
    ##############################

    df['calendar_date'] = pd.to_datetime(df['calendar_date'])

    ########################
    ####### Filters ########
    ########################

    df = df[
        (df['calendar_date'] >= pd.to_datetime(shared_start_date)) &
        (df['calendar_date'] <= pd.to_datetime(shared_end_date))
    ]

    ####################################################
    ####### Stacked Bar Chart: Activity by week ########
    ####################################################

    list_of_activity_type = df['type_of_activity'].unique().tolist()
    activity_filter = st.multiselect(
        'Select Activity',
        options=list_of_activity_type,
        default=list_of_activity_type,
        key=f"{date_prefix}activity_filter"
    )

    activity_by_week_df = df[df['type_of_activity'].isin(activity_filter)]

    chart = alt.Chart(activity_by_week_df).mark_bar().encode(
        x=alt.X('week_start_date:T', title='Week Start Date', axis=alt.Axis(format='%b %d %y')),
        y=alt.Y('had_activity:Q', title='Had Activity'),
        color=alt.Color('type_of_activity:N', title='Type of Activity')
    ).properties(
        width=800,
        height=400,
        title='Stacked Bar Chart of Weekly Activities'
    )

    st.altair_chart(chart, use_container_width=True)

    #############################################
    ####### Bar Chart: Count by Activity ########
    #############################################

    activity_count_df = df.groupby('type_of_activity')['had_activity'].sum().reset_index()
    activity_count_df.columns = ['Activity', 'Count']

    chart_2 = alt.Chart(activity_count_df).mark_bar().encode(
        x='Count:Q',
        y=alt.Y('Activity:N', sort='-x'),
        color='Activity:N'
    ).properties(
        width=600,
        height=400,
        title='Bar Chart by Activity Type'
    )

    st.altair_chart(chart_2, use_container_width=True)

    st.divider()

    ########################################
    ####### Weight Lifting Progress ########
    ########################################

    st.markdown("## Weight Lifting")

    gym_exercise_type_selection = st.selectbox(
        "Gym Exercise Type",
        options=gym_exercises_df['gym_exercise_type'].str.strip().unique(),
        key=f"{date_prefix}exercise_type"
    )

    # Filter data based on selected gym exercise and same date range
    gym_exercises_df['gym_date'] = pd.to_datetime(gym_exercises_df['gym_date'])

    gym_exercise_filtered = gym_exercises_df[
        (gym_exercises_df['gym_date'] >= pd.to_datetime(shared_start_date)) &
        (gym_exercises_df['gym_date'] <= pd.to_datetime(shared_end_date)) &
        (gym_exercises_df['gym_exercise_type'].str.strip() == gym_exercise_type_selection)
    ]

    chart_3 = alt.Chart(gym_exercise_filtered).mark_bar().encode(
        x=alt.X('gym_date:T', title='Gym Date', axis=alt.Axis(format='%b %d %y')),
        y=alt.Y('sum(gym_exercise_repetitions):Q', title='Total Reps'),
        color=alt.Color('gym_exercise_weight:N', title='Weight'),
        tooltip=[
            'gym_date:T',
            'gym_exercise_weight:N',
            alt.Tooltip('sum(gym_exercise_repetitions):Q', title='Total Reps')
        ]
    ).properties(
        width=800,
        height=400,
        title='Sum of Weekly Weight Lifting Reps'
    )

    st.altair_chart(chart_3, use_container_width=True)

    #####################
    ###### Ask AI #######
    #####################

    st.markdown("## 💬 Ask AI Assistant")

    ask_ai_key = 'ask_ai_button_gym_tracker'

    user_question = st.text_input(
                        "Enter your question (e.g. 'What are my most common exercises?')",
                        key=f'{ask_ai_key}_1'
                        )

    if st.button("Ask AI", key=f'{ask_ai_key}_2'):
        if not user_question:
            st.warning("Please enter a question.")
        elif df.empty:
            st.warning("No journal data available to provide context.")
        else:
            with st.spinner("Getting AI response..."):
                answer = ask_openai_chat(user_question, context_df=df)
            st.success("AI response:")
            st.write(answer)