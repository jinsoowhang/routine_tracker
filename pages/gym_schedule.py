import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt
import july
from july.utils import date_range

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM fct__all_dates_activity;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""📈Gym Routine""")

st.divider()

######################
####### Table ########
######################

st.write(df)

##############################
####### Calendar View ########
##############################

## Create a figure with a single axes
fig, ax = plt.subplots()

## Tell july to make a plot in a specific axes
july.month_plot(df.calendar_date, df.had_activity, month=2, date_label=True, ax=ax, colorbar=True)

st.title("📊 A `july.month_plot()` in streamlit")
## Tell streamlit to display the figure
st.pyplot(fig)