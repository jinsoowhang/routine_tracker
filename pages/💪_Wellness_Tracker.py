import streamlit as st
from pages.subpages.wellness_subpages.tennis_tracker import render_tennis_tracker
from pages.subpages.wellness_subpages.gym_tracker import render_gym_tracker
from pages.subpages.wellness_subpages.health_tracker import render_body_weight_tracker  
from pages.subpages.wellness_subpages.sleep_tracker import render_sleep_tracker  
from datetime import datetime, timedelta

# Page config
st.set_page_config(layout='wide')
st.title("💪 Wellness Tracker")

# Shared date filters in sidebar
st.sidebar.markdown("## Date Filters")
default_end_date = datetime.today()
default_start_date = default_end_date - timedelta(days=30)

shared_start_date = st.sidebar.date_input("From Date", default_start_date, key="shared_start_date")
shared_end_date = st.sidebar.date_input("To Date", default_end_date, key="shared_end_date")

# Tabs for organizing different trackers
tab1, tab2, tab3, tab4 = st.tabs(["🎾 Tennis", "🏋️ Gym", "💊 Health", "😴 Sleep"])

with tab1:
    render_tennis_tracker(shared_start_date, shared_end_date)

with tab2:
    render_gym_tracker(shared_start_date, shared_end_date)

with tab3:
    render_body_weight_tracker(shared_start_date, shared_end_date)

with tab4:
    render_sleep_tracker(shared_start_date, shared_end_date)
