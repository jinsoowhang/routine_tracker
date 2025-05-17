import streamlit as st

# Set page config FIRST — before any other Streamlit code runs
st.set_page_config(layout="wide", page_title="Lifestyle Tracker")

# Import necessary libraries
from pages.subpages.lifestyle_subpages.activity_tracker import render_activity_tracker
from pages.subpages.lifestyle_subpages.habit_tracker import render_habit_tracker
from pages.subpages.lifestyle_subpages.journal_tracker import render_journal_tracker 
from pages.subpages.lifestyle_subpages.todo_tracker import render_todo_tracker
from datetime import datetime, timedelta

# Page config
st.title("🌱 Lifestyle Tracker")

# Shared date filters in sidebar
st.sidebar.markdown("## Date Filters")
default_end_date = datetime.today()
default_start_date = default_end_date - timedelta(days=30)

shared_start_date = st.sidebar.date_input("From Date", default_start_date, key="shared_start_date")
shared_end_date = st.sidebar.date_input("To Date", default_end_date, key="shared_end_date")

# Tabs for organizing different trackers
tab1, tab2, tab3, tab4 = st.tabs(["📝 Activity", "💡 Habit", "📓 Journal", "📋 TODOs"])  

with tab1:
    render_activity_tracker(shared_start_date, shared_end_date)

with tab2:
    render_habit_tracker(shared_start_date, shared_end_date)

with tab3:
    render_journal_tracker(shared_start_date, shared_end_date) 

with tab4:
    render_todo_tracker(shared_start_date, shared_end_date) 