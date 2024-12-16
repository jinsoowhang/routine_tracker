import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
body_weight_df = conn.query('SELECT * FROM fct__weight_tracking;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""💊 Health Tracker""")

st.divider()

####################################
####### Body Weight Tracker ########
####################################

st.markdown("## Body Weight Over Time")

chart_1 = alt.Chart(body_weight_df).mark_line().encode(
    x = alt.X('weigh_in_date'),
    y = alt.Y('body_weight', scale=alt.Scale(domain=[140, 160]))
)

# Display the chart in Streamlit
st.altair_chart(chart_1, use_container_width=True)

#################################
####### Last 5 Weigh Ins ########
#################################

st.markdown("## Last 5 Weigh Ins")

# Display the table
st.dataframe(body_weight_df.sort_values(by='weigh_in_date', ascending=False).head(5))