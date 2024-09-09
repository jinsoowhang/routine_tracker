import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# CSV File Path
csv_file_path = 'data/raw_data/raw_rhythm.csv'
df = pd.read_csv(csv_file_path)

st.write(df)
