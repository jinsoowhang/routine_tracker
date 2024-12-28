import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
professional_df = conn.query('SELECT * FROM stg__professional;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""💼 Professional Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

professional_df['application_date'] = pd.to_datetime(professional_df['application_date'])

# Calculate the default start and end dates
default_end_date = dt.today()
default_start_date = professional_df['application_date'].min()

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
professional_df = professional_df[
    (professional_df['application_date'] >= pd.to_datetime(start_dt)) &
    (professional_df['application_date'] <= pd.to_datetime(end_dt))
]

#########################################################

# Create a new column to concatenate all relevant columns
columns_to_concatenate = ['application_status', 'application_phase', 'application_phase_desc',\
                          'company_name', 'job_title', 'job_location']

professional_df['concatenated_values'] = professional_df[columns_to_concatenate].astype(str).apply(
    lambda row: ' | '.join(row.values), axis=1
)

#################################################
####### Last Occurrence of Application X ########
#################################################

st.title('Last Occurrence of Application X')

# User Input
last_activity_prompt = st.text_input("Write the application you want to track in lowercase 👇")

# Filter data by user input
filter_by_user_prompt = professional_df[professional_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

# Show number of applications
if last_activity_prompt == '':
    st.write('There is no input from user. Please write the activity in text box ☝️')
else: 
    st.write(f"You've applied {len(filter_by_user_prompt)} times to this company")

# Sort by date in descending order
sorted_prompt = filter_by_user_prompt.sort_values(by='application_date', ascending=False)

# Display the dataframe
st.dataframe(sorted_prompt, use_container_width=True)
