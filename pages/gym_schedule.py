import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM fct__all_dates_activity;', ttl="10m")

##############################
####### Data Cleaning ########
##############################

df['calendar_date'] = pd.to_datetime(df['calendar_date'])


###########################
####### Title Page ########
###########################

st.title("""📈Gym Routine""")

st.divider()

########################
####### Filters ########
########################

df['first_active_date'] = df['calendar_date']
start_dt = st.sidebar.date_input('From Date', value=df['first_active_date'].min())

df['last_active_date'] = df['calendar_date']
end_dt = st.sidebar.date_input('To Date', value=df['last_active_date'].max())

df = df[(df['calendar_date'] >= pd.to_datetime(start_dt)) & (df['calendar_date'] <= pd.to_datetime(end_dt))]

##########################
####### Bar Chart ########
##########################

st.write(df.groupby('week_start_date').sum('had_activity'))

######################
####### Table ########
######################

st.markdown(f"This is the table")

st.write(df)

