import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
rhythm_df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""⏱️Activity Tracker""")

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

##############################
####### Data Cleaning ########
##############################

# Convert to datetime
rhythm_df['rhythm_date'] = pd.to_datetime(rhythm_df['rhythm_date'], format='%Y%m%d')

########################
####### Filters ########
########################

default_end_date = dt.today()
default_start_date = default_end_date - timedelta(days=30)

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
rhythm_df = rhythm_df[
    (rhythm_df['rhythm_date'] >= pd.to_datetime(start_dt)) &
    (rhythm_df['rhythm_date'] <= pd.to_datetime(end_dt))
]

##############################################
####### Last Occurrence of Activity X ########
##############################################

st.title('Last Occurrence of Activity X')

# User Input
last_activity_prompt = st.text_input("Write the activity you want to track in lowercase 👇")

# Filter data by user input
filter_by_user_prompt = rhythm_df[rhythm_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

# Display the amount of time spent in this activity
activity_hours_spent = int(len(filter_by_user_prompt)/4)
activity_days_spent = int(activity_hours_spent/24)
activity_proportion_spent = round(len(filter_by_user_prompt) / len(rhythm_df) * 100, 1)

if last_activity_prompt == '':
    st.write('There is no input from user. Please write the activity in text box ☝️')
else: 
    st.write(f'All time {'"'+str(last_activity_prompt)+'"'} duration: {activity_hours_spent} hours or {activity_days_spent} days, accounts for {activity_proportion_spent}% of total activities')

# Sort by date in descending order
columns_to_display = ['days_since_rhythm_date', 'rhythm_date', 'weekday', 'activity', 'attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places', 'people', 'notes']

sorted_prompt = filter_by_user_prompt.sort_values(by='rhythm_date', ascending=False)[columns_to_display]

# Display the dataframe
st.dataframe(sorted_prompt, use_container_width=True)

##############################################
####### Activity Distribution by Date ########
##############################################

# Define simplified grouped colors
custom_colors = {
    # Highly Productive (Dark Green)
    "work": "#006400",  # Dark Green
    "study": "#228B22",  # Forest Green
    "productive": "#32CD32",  # Lime Green

    # Moderately Productive (Medium Green)
    "clean": "#66CDAA",  # Medium Aquamarine
    "grocery": "#8FBC8F",  # Dark Sea Green
    "read": "#98FB98",  # Pale Green
    "side_hustle": "#00FA9A",  # Medium Spring Green
    "learn": "#ADFF2F",  # Green Yellow
    "exercise": "#637939",  # Dark Green
    "meet": "#2E8B57",  # Sea Green
    "church": "#20B2AA",  # Light Sea Green

    # Leisure (Lighter Red shades for distinction)
    "commute": "#778899",  # Light Slate Gray
    "cook": "#FF7F50",  # Coral 
    "vacation": "#A9A9A9",  # Dark Gray 
    "leisure": "#FF4500",  # Orange Red
    "hangout": "#FF6A6A",  # Light Red

    # Personal Care (Gray-Green shades)
    "sleep": "#696969",  # Dim Gray
    "hygiene": "#D3D3D3",  # Light Gray
    "wake_up": "#B0C4DE",  # Light Steel Blue
    "walk": "#B0C4DE",  # Light Steel Blue
    "sick": "#708090",  # Slate Gray
    "eat": "#D3D3D3",  # Light Gray (for vacation)

    # Social Activities (Gray shades)
    "shopping": "#DCDCDC",  # Gainsboro
    "love": "#E6E6FA",  # Lavender
    "call": "#D8BFD8"  # Thistle
}


# rhythm_date and attribute_1 should exist in your dataframe
stacked_bar_chart = alt.Chart(sorted_prompt).mark_bar(size=30).encode(
    x=alt.X(
        'rhythm_date:T', 
        title='Rhythm Date'
    ),
    y=alt.Y(
        'sum(hours):Q', 
        title='Total Time (Hours)'  # Aggregate hours
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
        alt.Tooltip('sum(hours):Q', title='Total Time (Hours)', format=".2f"),  # Tooltip for hours
        alt.Tooltip('weekday:O', title='Weekday')  # Add weekday to tooltip
    ]
).transform_calculate(
    hours="15 / 60"  # Each count represents 15 minutes, converted to hours
).properties(
    title='Activity Distribution by Date',
    width=800,
    height=600
)

# Display the chart in Streamlit
st.altair_chart(stacked_bar_chart, use_container_width=True)

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
    
    # Reorder columns
    return proportion_df[[activity_column, 'total_hours', 'total_days', 'proportion (%)']]

# Display Proportion by Activity Hierarchy
st.markdown("#### Proportion by Activity Hierarchy")
activity_hierarchy = st.selectbox(
    "Select activity hierarchy",
    ['attribute_1', 'attribute_2', 'attribute_3', 'attribute_4', 'places'],
    index=0
)
activity_proportion_df = calculate_proportions(rhythm_df, activity_hierarchy)
st.write(activity_proportion_df)

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
st.write(activity_proportion_2_df)

st.divider()