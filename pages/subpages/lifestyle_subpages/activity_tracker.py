import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def render_activity_tracker(start_dt, end_dt):  # Accept date filters as arguments

    # Perform query.
    rhythm_df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

    ###########################
    ####### Title Page ########
    ###########################

    st.title("""📝Activity Tracker""")

    st.divider()

    ##############################
    ####### Data Cleaning ########
    ##############################

    # Convert to date
    rhythm_df['rhythm_date'] = pd.to_datetime(rhythm_df['rhythm_date'], format='%Y%m%d')

    # Create a new columns to show days since rhythm_date
    rhythm_df['days_since_rhythm_date'] = -(pd.Timestamp.today() - rhythm_df['rhythm_date']).dt.days

    # Create a new column to concatenate all relevant columns
    columns_to_concatenate = ['activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']

    rhythm_df['concatenated_values'] = rhythm_df[columns_to_concatenate].astype(str).apply(
        lambda row: ' | '.join(row.values), axis=1
    )

    ########################
    ####### Filters ########
    ########################

    # Filter the DataFrame to include only the selected date range
    rhythm_df = rhythm_df[
        (rhythm_df['rhythm_date'] >= pd.to_datetime(start_dt)) & 
        (rhythm_df['rhythm_date'] <= pd.to_datetime(end_dt))
    ]

    ###############################
    ####### Track Activity ########
    ###############################

    st.markdown('## Track Activity')

    # User Input
    last_activity_prompt = st.text_input("Write the activity you want to track in lowercase 👇")

    # Filter data by user input
    filter_by_user_prompt = rhythm_df[rhythm_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

    # Display the amount of time spent in this activity
    activity_hours_spent = int(len(filter_by_user_prompt)/4)
    activity_days_spent = int(activity_hours_spent/24)
    activity_proportion_spent = round(len(filter_by_user_prompt) / len(rhythm_df) * 100, 1)
    activity_count_of_days = filter_by_user_prompt['rhythm_date'].nunique()

    # Sort by date in descending order
    columns_to_display = ['days_since_rhythm_date', 'rhythm_date', 'weekday', 'activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']

    sorted_prompt = filter_by_user_prompt.sort_values(by='rhythm_date', ascending=False)[columns_to_display]

    st.divider()

    ################################
    ####### High Level KPIs ########
    ################################

    st.markdown('## High Level KPIs')

    if last_activity_prompt == '':
        st.write('There is no input from user. Please write the activity in text box ☝️')
    else: 
        # Columns for KPIs
        st.write(f'Time {"{str(last_activity_prompt)}"} duration: {activity_hours_spent} hours or {activity_days_spent} total days, accounts for {activity_proportion_spent}% of total activities')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Count of unique days", value=activity_count_of_days)
            
        with col2:
            st.metric(label="Sum of Hours", value=activity_hours_spent)
            
        with col3:
            st.metric(label="Sum of Days", value=activity_days_spent)

        with col4:
            st.metric(label="Proportion of Activities", value=f'{activity_proportion_spent}%')

    st.divider()

    ##############################################
    ####### Activity Distribution by Date ########
    ##############################################

    # Define simplified grouped colors
    custom_colors = {
        "work": "#006400",  
        "study": "#228B22",  
        "productive": "#32CD32",  

        "clean": "#66CDAA",  
        "grocery": "#8FBC8F",  
        "read": "#98FB98",  
        "side_hustle": "#00FA9A",  
        "learn": "#ADFF2F",  
        "exercise": "#637939",  
        "meet": "#2E8B57",  
        "church": "#20B2AA",  

        "commute": "#778899",  
        "cook": "#FF7F50",  
        "vacation": "#A9A9A9",  
        "travel": "#A9A9A9", 
        "leisure": "#FF4500",  
        "hangout": "#FF6A6A",  

        "sleep": "#696969",  
        "hygiene": "#D3D3D3",  
        "wake_up": "#B0C4DE",  
        "walk": "#B0C4DE",  
        "sick": "#708090",  
        "eat": "#D3D3D3",  

        "shopping": "#DCDCDC",  
        "love": "#E6E6FA",  
        "call": "#D8BFD8"  
    }

    # rhythm_date and attribute_1 should exist in your dataframe
    stacked_bar_chart = alt.Chart(sorted_prompt).mark_bar(size=30).encode(
        x=alt.X(
            'rhythm_date:T', 
            title='Rhythm Date'
        ),
        y=alt.Y(
            'sum(hours):Q', 
            title='Total Time (Hours)'  
        ),
        color=alt.Color(
            'attribute_1:N', 
            title='Activity Type',
            scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values()))
        ),
        order=alt.Order(
            'sum(hours):Q'
        ),
        tooltip=[
            'rhythm_date:T', 
            'attribute_1:N', 
            alt.Tooltip('sum(hours):Q', title='Total Time (Hours)', format=".2f"),  
            alt.Tooltip('weekday:O', title='Weekday')  
        ]
    ).transform_calculate(
        hours="15 / 60"  
    ).properties(
        title='Activity Distribution by Date',
        width=800,
        height=600
    )

    # Display the chart in Streamlit
    st.altair_chart(stacked_bar_chart, use_container_width=True)

    ###############################
    ####### Activity Table ########
    ###############################

    st.markdown('## Activity Table')

    # Display the dataframe
    st.dataframe(sorted_prompt, use_container_width=True, hide_index=True)

    st.divider()

    ######################################
    ####### High Level Activities ########
    ######################################

    st.markdown("## High Level Activities")

    # Function to calculate proportions and total hours/days
    def calculate_proportions(df, activity_column):
        # Group by the selected column and calculate counts
        proportion_df = df[['activity_id', activity_column]].groupby(activity_column).size().reset_index(name='count')
        
        # Add total hours, total days, and proportion
        proportion_df['total_hours'] = round(proportion_df['count'] / 4)
        proportion_df['total_days'] = round(proportion_df['total_hours'] / 24)
        proportion_df['proportion (%)'] = round(proportion_df['count'] / proportion_df['count'].sum() * 100, 1)
        
        # Calculate last activity (smallest days_since_rhythm_date)
        last_occurrence_df = df.groupby(activity_column)['days_since_rhythm_date'].max().reset_index()
        last_occurrence_df.rename(columns={'days_since_rhythm_date': 'days_since_last'}, inplace=True)

        # Merge last occurrence into proportion_df
        proportion_df = proportion_df.merge(last_occurrence_df, on=activity_column, how='left')

        # Reorder columns
        return proportion_df[[activity_column, 'days_since_last', 'total_hours', 'total_days', 'proportion (%)']]

    # Display Proportion by Activity Hierarchy
    st.markdown("#### Proportion by Activity Hierarchy")
    activity_hierarchy = st.selectbox(
        "Select activity hierarchy",
        ['attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places'],
        index=0
    )
    activity_proportion_df = calculate_proportions(rhythm_df, activity_hierarchy)
    st.dataframe(activity_proportion_df, hide_index=True)

    ######################################

    # Display Proportion by Activity Hierarchy Group
    st.markdown("#### Proportion by Activity Hierarchy Group")
    sub_activity_hierarchy = st.selectbox(
        "Select sub activity",
        rhythm_df[activity_hierarchy].unique(),
        index=5
    )
    groupby_activity_hierarchy = st.selectbox(
        "Select activity hierarchy to group by",
        ['attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places']
    )

    # Filter data for selected sub activity
    grouped_rhythm_df = rhythm_df[rhythm_df[activity_hierarchy] == sub_activity_hierarchy]
    activity_proportion_2_df = calculate_proportions(grouped_rhythm_df, groupby_activity_hierarchy)
    st.dataframe(activity_proportion_2_df, hide_index=True)

    st.divider()
