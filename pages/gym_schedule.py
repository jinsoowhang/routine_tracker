import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# CSV File Path
csv_file_path = 'data/raw_data/raw_gym.csv'
df = pd.read_csv(csv_file_path)

###########################
####### Title Page ########
###########################

st.title("""📈Gym Routine""")

st.divider()

######################
####### Table ########
######################

st.write(df)

