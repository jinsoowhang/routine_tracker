import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Navigation
p1 = st.Page(
    "pages/routine_schedule.py",
    title = "Routine Schedule",
    icon = "📅"
)

pg = st.navigation({
    "Metrics": [p1]
})

pg.run()