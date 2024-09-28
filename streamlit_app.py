import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.write("# Welcome to Routine Schedule")

st.markdown(
    """
    We'll display the routines and stats of this user
    """
)

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

# Print results
st.write(df)