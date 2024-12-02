import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Title page 
st.markdown("# 📙 About")

st.markdown("## 🚀 Goal")
st.markdown("""
The goal of this project is to analyze my daily habits, identify positive patterns to maintain, and replace any negative habits with healthier alternatives.
""")

st.markdown("### 🔗 Useful Links")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### [🌐 GitHub](https://github.com/jinsoowhang/routine_tracker)")
    st.write("Link to the source code")

with col2:
    st.markdown("### [📙 The Compound Effect](https://www.amazon.com/Compound-Effect-Darren-Hardy/dp/159315724X)")
    st.write("The book that started this journey on tracking daily habits")