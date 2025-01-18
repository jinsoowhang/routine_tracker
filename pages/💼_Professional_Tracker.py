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

########################
####### Filters ########
########################

st.markdown("## Filters")

# Define the columns and corresponding filter names
filter_columns = {
    "Application Status": "application_status",
    "Application Phase": "application_phase",
    "Application Phase Desc": "application_phase_desc",
    "Company Name": "company_name",
    "Job Title": "job_title",
    "Job Location": "job_location"
}

# Create the filters dynamically
filters = {}
with st.container():
    cols = st.columns(len(filter_columns))  # Create the necessary number of columns
    for i, (label, column) in enumerate(filter_columns.items()):
        with cols[i]:
            # Filter out None or NaN values and sort the remaining values
            sorted_values = sorted(professional_df[column].dropna().unique().tolist())
            filters[column] = st.selectbox(
                label,
                options=["All"] + sorted_values,
                index=0
            )

# Apply filters dynamically
filtered_df = professional_df.copy()
for column, selected_value in filters.items():
    if selected_value != "All":
        filtered_df = filtered_df[filtered_df[column] == selected_value]

# User Input
last_activity_prompt = st.text_input("Free Text Field filter 👇")

# Filter data by user input
filter_by_user_prompt = filtered_df[filtered_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

# Show number of applications
if last_activity_prompt == '':
    st.write('There is no input from user. Please write the desired filter in text box ☝️')
else: 
    st.write(f"You've applied {len(filter_by_user_prompt)} times to this company")

st.divider()

####### High Level KPIs ########

# High Level KPIs
st.markdown("### High Level KPIs")

# Columns for KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Applications", value=filter_by_user_prompt['application_id'].nunique())
    st.metric(label="Applications This Year", 
              value=filter_by_user_prompt[filter_by_user_prompt['application_date'] >= pd.Timestamp.now().replace(month=1, day=1)]['application_id'].nunique())
    st.metric(label="Applications This Month", 
              value=filter_by_user_prompt[filter_by_user_prompt['application_date'] >= pd.Timestamp.now().replace(day=1)]['application_id'].nunique())

with col2:
    most_common_company = filter_by_user_prompt['company_name'].mode().iloc[0]
    most_common_company_count = filter_by_user_prompt[filter_by_user_prompt['company_name'] == most_common_company].shape[0]
    st.metric(label="Most Common Company", value=f"{most_common_company} ({most_common_company_count})")

    most_common_job_title = filter_by_user_prompt['job_title'].mode().iloc[0]
    most_common_job_title_count = filter_by_user_prompt[filter_by_user_prompt['job_title'] == most_common_job_title].shape[0]
    st.metric(label="Most Common Job Title", value=f"{most_common_job_title} ({most_common_job_title_count})")

    most_common_location = filter_by_user_prompt['job_location'].mode().iloc[0]
    most_common_location_count = filter_by_user_prompt[filter_by_user_prompt['job_location'] == most_common_location].shape[0]
    st.metric(label="Most Common Location", value=f"{most_common_location} ({most_common_location_count})")

with col3:
    st.metric(label="Unique Companies", value=filter_by_user_prompt['company_name'].nunique())
    st.metric(label="Unique Job Titles", value=filter_by_user_prompt['job_title'].nunique())
    st.metric(label="Unique Locations", value=filter_by_user_prompt['job_location'].nunique())

st.divider()


####### Stacked Bar Chart: Applications Over Time by Phase ########

# Convert application_date to datetime if not already
filter_by_user_prompt['application_date'] = pd.to_datetime(filter_by_user_prompt['application_date'])

# Group data by date and phase
applications_over_time = (
    filter_by_user_prompt.groupby(['application_date', 'application_phase'])
    .size()
    .reset_index(name='count')
)

# Create an Altair line chart with application phases stacked
chart = alt.Chart(applications_over_time).mark_bar().encode(
    x=alt.X('application_date:T', title='Application Date'),
    y=alt.Y('count:Q', title='Number of Applications'),
    color=alt.Color('application_phase:N', title='Application Phase'),
    tooltip=[
        alt.Tooltip('application_date:T', title='Date'),
        alt.Tooltip('application_phase:N', title='Phase'),
        alt.Tooltip('count:Q', title='Count')
    ]
).properties(
    width=800,
    height=400,
    title='Applications Over Time by Phase'
)

# Display in Streamlit
st.altair_chart(chart, use_container_width=True)

####### Detailed Table ########

# Sort by date in descending order
sorted_prompt = filter_by_user_prompt.sort_values(by='application_date', ascending=False)

# Display the dataframe
st.markdown("##### Application Details")
st.dataframe(sorted_prompt, use_container_width=True, hide_index=True)


