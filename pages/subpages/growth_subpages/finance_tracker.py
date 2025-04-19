import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
from datetime import timedelta

def render_finance_tracker(shared_start_date, shared_end_date):
    st.title("💵 Finance Tracker")
    st.divider()

    # Initialize connection
    conn = st.connection("postgresql", type="sql")
    finance_transactions_df = conn.query('SELECT * FROM fct__finance_transactions;', ttl="10m")

    # Convert date column
    finance_transactions_df['transaction_date'] = pd.to_datetime(finance_transactions_df['transaction_date'])
    finance_transactions_df['year_month'] = finance_transactions_df['transaction_date'].dt.to_period('M')

    # Filter by shared dates
    date_filtered_finance_df = finance_transactions_df[
        (finance_transactions_df['transaction_date'].dt.date >= shared_start_date) &
        (finance_transactions_df['transaction_date'].dt.date <= shared_end_date)
    ]

    # Filters
    st.markdown("## Filters")
    filter_columns = {
        "Transaction Type": "transaction_type",
        "Supplier": "supplier",
        "Parent Supplier": "parent_supplier",
        "Spend Category": "spend_category",
        "Card Owner": "card_owner",
        "Bank Name": "bank_name",
    }

    filters = {}
    with st.container():
        cols = st.columns(len(filter_columns))
        for i, (label, column) in enumerate(filter_columns.items()):
            with cols[i]:
                sorted_values = sorted(date_filtered_finance_df[column].dropna().unique().tolist())
                filters[column] = st.selectbox(
                    label,
                    options=["All"] + sorted_values,
                    index=0
                )

    filtered_df = date_filtered_finance_df.copy()
    for column, selected_value in filters.items():
        if selected_value != "All":
            filtered_df = filtered_df[filtered_df[column] == selected_value]

    st.divider()

    # Chart
    grouped_df = filtered_df.groupby(['year_month', 'spend_category'], as_index=False)['amount'].sum()
    chart = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('year_month:T', title='Year-Month'),
        y=alt.Y('sum(amount):Q', title='Total Amount'),
        color='spend_category:N',
        tooltip=['year_month', 'spend_category', 'sum(amount)']
    ).properties(
        title='Total Spend by Category (Year-Month)',
        width=1200,
        height=400
    )
    st.altair_chart(chart)

    st.divider()
    st.markdown('## Transaction Table')
    st.dataframe(filtered_df, hide_index=True)