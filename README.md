# Routine Tracker

A fully dockerized ETL pipeline that tracks personal lifestyle, wellness, growth, and social habits over time. Data flows from Google Sheets through Airflow, gets transformed with dbt, and is visualized in a Streamlit dashboard — with OpenAI-powered insights.

![dashboard](/assets/images/about.png)

## What It Tracks

| Dashboard | Metrics |
|-----------|---------|
| **Lifestyle** | Daily activity scores, habit streaks, journal entries, todos |
| **Wellness** | Tennis matches, gym exercises, body weight, sleep, nutrition |
| **Growth** | Spending across credit cards (Amex, Chase, BoA), professional development |
| **Social** | Connection frequency, interaction logs |

## Architecture

```
Google Sheets ──→ Airflow DAG ──→ PostgreSQL (raw)
                                       │
                                   dbt models
                                       │
                              staging → dim → fact
                                       │
                              Streamlit + OpenAI
```

**Pipeline runs daily:**
1. Airflow extracts data from Google Sheets into PostgreSQL
2. dbt transforms raw data through staging, dimension, and fact layers
3. Streamlit reads transformed tables and renders interactive dashboards
4. OpenAI (gpt-4o-mini) generates natural language summaries of trends

## Tech Stack

| Layer | Technology |
|-------|------------|
| Orchestration | Apache Airflow 2.9.1 |
| Warehouse | PostgreSQL |
| Transformation | dbt |
| Visualization | Streamlit, Altair, Plotly, Seaborn |
| AI Insights | OpenAI API (gpt-4o-mini) |
| Data Source | Google Sheets (gspread) |
| Infrastructure | Docker, docker-compose |
| Admin | PGAdmin |

## Project Structure

```
routine_tracker/
├── airflow/dags/              # Daily ETL DAG
├── src/
│   ├── etl_rhythm/            # Google Sheets → PostgreSQL
│   ├── etl_finance/           # Credit card CSV transforms
│   └── helpers/openai_helper.py
├── dbt/models/
│   ├── staging/               # 8 staging views
│   ├── dimension/             # Date + supplier dimensions
│   └── mart/                  # 6 fact tables (activity scores, gym, tennis, finance)
├── pages/                     # Streamlit dashboard pages
│   ├── Lifestyle_Tracker/
│   ├── Wellness_Tracker/
│   ├── Growth_Tracker/
│   └── Social_Tracker/
├── Dockerfile
└── streamlit_app.py           # Entry point
```

## Key Feature: Activity Scoring

The `fct__daily_activity_scores` model assigns weighted points to every tracked activity — high-value habits (study, side projects) score higher than passive ones (leisure, sleep). Daily scores are capped at 110 with weekday-adjusted benchmarks, creating a single "how productive was today?" metric.

## Run Locally

```bash
docker-compose up
```

Requires `.env` with database credentials, OpenAI API key, and Google Sheets OAuth credentials.
