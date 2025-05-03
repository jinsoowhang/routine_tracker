import streamlit as st

# Set page config FIRST — before any other Streamlit code runs
st.set_page_config(layout="wide", page_title="Social Tracker")

# Import necessary libraries
from pages.subpages.social_subpages.connections_tracker import render_connections_tracker
from datetime import datetime, timedelta

# Page config
st.title("🤝 Social Tracker")

# Shared date filters in sidebar
st.sidebar.markdown("## Date Filters")
default_end_date = datetime.today()
default_start_date = default_end_date - timedelta(days=30)

shared_start_date = st.sidebar.date_input("From Date", default_start_date, key="shared_start_date")
shared_end_date = st.sidebar.date_input("To Date", default_end_date, key="shared_end_date")

# Tabs for organizing different trackers
tab1, = st.tabs(["👥 Connections Tracker"])

with tab1:
    render_connections_tracker(shared_start_date, shared_end_date)

