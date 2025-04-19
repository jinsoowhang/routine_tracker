import streamlit as st
from pages.subpages.growth_subpages.finance_tracker import render_finance_tracker
from pages.subpages.growth_subpages.professional_tracker import render_professional_tracker
from datetime import datetime, timedelta

# Page config
st.set_page_config(layout='wide')
st.title("📈 Growth Tracker")

# Shared date filters in sidebar
st.sidebar.markdown("## Date Filters")
default_end_date = datetime.today()
default_start_date = default_end_date - timedelta(days=365)

shared_start_date = st.sidebar.date_input("From Date", default_start_date, key="shared_start_date")
shared_end_date = st.sidebar.date_input("To Date", default_end_date, key="shared_end_date")

# Tabs for organizing different trackers
tab1, tab2 = st.tabs(["💵 Finance Tracker", "💼 Professional Tracker"])

with tab1:
    render_finance_tracker(shared_start_date, shared_end_date)

with tab2:
    render_professional_tracker(shared_start_date, shared_end_date)