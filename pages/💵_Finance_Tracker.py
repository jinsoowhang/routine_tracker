import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

st.set_page_config(layout='wide')

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
finance_transactions_df = conn.query('SELECT * FROM fct__finance_transactions;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""💵 Finance Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

finance_transactions_df['transaction_date'] = pd.to_datetime(finance_transactions_df['transaction_date'])

# Calculate the default start and end dates
default_end_date = dt.today()
default_start_date = finance_transactions_df['transaction_date'].min()

# Add date input widgets with default values
start_dt = st.sidebar.date_input('From Date', value=default_start_date)
end_dt = st.sidebar.date_input('To Date', value=default_end_date)

# Filter the DataFrame to include only the selected date range
date_filtered_finance_df = finance_transactions_df[
    (finance_transactions_df['transaction_date'] >= pd.to_datetime(start_dt)) &
    (finance_transactions_df['transaction_date'] <= pd.to_datetime(end_dt))
]

########################
####### Filters ########
########################

st.markdown("## Filters")

# Define the columns and corresponding filter names
filter_columns = {
    "Transaction Type": "transaction_type",
    "Supplier": "supplier",
    "Parent Supplier": "parent_supplier",
    "Spend Category": "spend_category",
    "Card Owner": "card_owner",
    "Bank Name": "bank_name",
}

# Create the filters dynamically
filters = {}
with st.container():
    cols = st.columns(len(filter_columns))  # Create the necessary number of columns
    for i, (label, column) in enumerate(filter_columns.items()):
        with cols[i]:
            # Filter out None or NaN values and sort the remaining values
            sorted_values = sorted(date_filtered_finance_df[column].dropna().unique().tolist())
            filters[column] = st.selectbox(
                label,
                options=["All"] + sorted_values,
                index=0
            )

# Apply filters dynamically
filtered_df = date_filtered_finance_df.copy()
for column, selected_value in filters.items():
    if selected_value != "All":
        filtered_df = filtered_df[filtered_df[column] == selected_value]

st.divider()

##################################
####### Transaction Table ########
##################################

st.markdown('## Transaction Table')

st.dataframe(filtered_df)