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

###########################
####### Title Page ########
###########################

st.title("""📈Gym Routine""")

st.divider()

######################
####### Table ########
######################

st.write(df)