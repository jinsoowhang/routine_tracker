# 📅 Routine Tracker

A Streamlit app to track and visualize lifestyle, wellness, growth, and social interactions over time

![dashboard](/assets/images/about.PNG)

---

### About the App
- **Tech Stack:** Docker, Airflow, dbt, Streamlit, PostgreSQL, PGAdmin, Google Sheets
- **Data Flow:**
  - Using an Airflow DAG, it pulls data from multiple Google Sheets into PostgreSQL.
  - Data transformation is done using dbt.
  - The transformed data is visualized through Streamlit dashboards.

---