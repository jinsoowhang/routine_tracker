import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt

def render_professional_tracker(start_dt, end_dt):
    st.markdown("## 💼 Professional Tracker")
    st.divider()

    # Initialize connection.
    conn = st.connection("postgresql", type="sql")

    # Perform query.
    professional_df = conn.query('SELECT * FROM stg__professional;', ttl="10m")
    rhythm_df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

    # --- Data Cleaning ---
    professional_df['application_date'] = pd.to_datetime(professional_df['application_date'])
    rhythm_df['rhythm_date'] = pd.to_datetime(rhythm_df['rhythm_date'], format='%Y%m%d')

    # --- Date Filtering ---
    professional_df = professional_df[
        (professional_df['application_date'] >= pd.to_datetime(start_dt)) &
        (professional_df['application_date'] <= pd.to_datetime(end_dt))
    ]

    rhythm_df = rhythm_df[
        (rhythm_df['rhythm_date'] >= pd.to_datetime(start_dt)) &
        (rhythm_df['rhythm_date'] <= pd.to_datetime(end_dt))
    ]

    # --- Job Activity Tracker ---
    st.markdown('## Job Activity Tracker')

    work_df = rhythm_df[rhythm_df['attribute_1'] == 'work'].copy()

    job_activity_tracker_df = (
        work_df[['attribute_3']]
        .groupby('attribute_3')
        .value_counts()
        .sort_values(ascending=False)
        .rename('counts')
        .reset_index()
    )

    job_activity_tracker_df['hours_spent'] = job_activity_tracker_df['counts'] / 4
    total_counts = job_activity_tracker_df['counts'].sum()
    job_activity_tracker_df['proportion(%)'] = (job_activity_tracker_df['counts'] / total_counts * 100).round()

    st.dataframe(
        job_activity_tracker_df[['attribute_3', 'hours_spent', 'proportion(%)']],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --- Job Application Tracker ---
    st.markdown('## Job Application Tracker')

    columns_to_concatenate = ['application_status', 'application_phase', 'application_phase_desc',
                              'company_name', 'job_title', 'job_location']

    professional_df['concatenated_values'] = professional_df[columns_to_concatenate].astype(str).apply(
        lambda row: ' | '.join(row.values), axis=1
    )

    # --- Filters ---
    st.markdown("### Filters")

    filter_columns = {
        "Application Status": "application_status",
        "Application Phase": "application_phase",
        "Application Phase Desc": "application_phase_desc",
        "Company Name": "company_name",
        "Job Title": "job_title",
        "Job Location": "job_location"
    }

    filters = {}
    with st.container():
        cols = st.columns(len(filter_columns))
        for i, (label, column) in enumerate(filter_columns.items()):
            with cols[i]:
                sorted_values = sorted(professional_df[column].dropna().unique().tolist())
                filters[column] = st.selectbox(label, options=["All"] + sorted_values, index=0)

    filtered_df = professional_df.copy()
    for column, selected_value in filters.items():
        if selected_value != "All":
            filtered_df = filtered_df[filtered_df[column] == selected_value]

    last_activity_prompt = st.text_input("Free Text Field filter 👇")
    filter_by_user_prompt = filtered_df[filtered_df['concatenated_values'].str.lower().str.contains(last_activity_prompt, na=False)]

    if last_activity_prompt == '':
        st.write('There is no input from user. Please write the desired filter in text box ☝️')
    else:
        st.write(f"You've applied {len(filter_by_user_prompt)} times to this company")

    st.divider()

    # --- High Level KPIs ---
    st.markdown("### High Level KPIs")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Applications", value=filter_by_user_prompt['application_id'].nunique())
        st.metric(label="Applications This Year", value=filter_by_user_prompt[
            filter_by_user_prompt['application_date'] >= pd.Timestamp.now().replace(month=1, day=1)
        ]['application_id'].nunique())
        st.metric(label="Applications This Month", value=filter_by_user_prompt[
            filter_by_user_prompt['application_date'] >= pd.Timestamp.now().replace(day=1)
        ]['application_id'].nunique())

    with col2:
        most_common_company = filter_by_user_prompt['company_name'].mode().iloc[0]
        st.metric(label="Most Common Company", value=f"{most_common_company} ({(filter_by_user_prompt['company_name'] == most_common_company).sum()})")
        most_common_job_title = filter_by_user_prompt['job_title'].mode().iloc[0]
        st.metric(label="Most Common Job Title", value=f"{most_common_job_title} ({(filter_by_user_prompt['job_title'] == most_common_job_title).sum()})")
        most_common_location = filter_by_user_prompt['job_location'].mode().iloc[0]
        st.metric(label="Most Common Location", value=f"{most_common_location} ({(filter_by_user_prompt['job_location'] == most_common_location).sum()})")

    with col3:
        st.metric(label="Unique Companies", value=filter_by_user_prompt['company_name'].nunique())
        st.metric(label="Unique Job Titles", value=filter_by_user_prompt['job_title'].nunique())
        st.metric(label="Unique Locations", value=filter_by_user_prompt['job_location'].nunique())

    st.divider()

    # --- Applications Over Time ---
    filter_by_user_prompt['application_date'] = pd.to_datetime(filter_by_user_prompt['application_date'])

    applications_over_time = (
        filter_by_user_prompt.groupby(['application_date', 'application_phase'])
        .size()
        .reset_index(name='count')
    )

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

    st.altair_chart(chart, use_container_width=True)

    # --- Application Details Table ---
    sorted_prompt = filter_by_user_prompt.sort_values(by='application_date', ascending=False)
    st.markdown("##### Application Details")
    st.dataframe(sorted_prompt, use_container_width=True, hide_index=True)
