# USGS-Earthquake-Mini-Pipeline

Daily automated ETL pipeline that ingests recent earthquake events from the USGS Earthquake API, processes the data, and loads it into a PostgreSQL database using Apache Airflow.

This project is designed as a small, production-style data engineering workflow to practice building scheduled pipelines, working with APIs, and managing data in a relational database.

---

## Project Overview

- **Source:** USGS Earthquake API (GeoJSON format)
- **Orchestration:** Apache Airflow (Docker)
- **Storage:** PostgreSQL
- **Frequency:** Daily run (cron: `0 0 * * *`)
- **Goal:** Maintain an up-to-date dataset of global earthquakes for analysis and reporting.

On each run, the pipeline:

1. Calls the USGS API for earthquakes over a configured time window (e.g., last 24 hours, minimum magnitude filter, sort by time).
2. Stores the raw GeoJSON response for reproducibility and auditing.
3. Transforms the raw payload into a clean tabular structure (magnitude, location, time, coordinates, depth, etc.).
4. Loads the curated records into a PostgreSQL table for querying and downstream analytics.

---

## Key Features

- **End-to-end ETL**: Automated extract, transform, and load steps managed through an Airflow DAG.
- **Daily scheduling**: DAG configured to run once per day with proper `start_date`, `schedule_interval`, and `catchup` settings.
- **Resilient design**: Task-level separation for fetching, transforming, and loading data; easier to monitor and debug.
- **Structured storage**: Earthquake events stored in Postgres for use with BI tools, dashboards, or ad-hoc SQL analysis.
- **Versioned raw data (optional)**: Raw API responses can be persisted to disk for backfills, reprocessing, or QA.

---

## Tech Stack

- **Python** – Core ETL logic and data transformations  
- **Apache Airflow** – Workflow orchestration and scheduling  
- **PostgreSQL** – Relational database for storing processed earthquake events  
- **Docker / Docker Compose** – Local containerized Airflow and Postgres environment  
- **Requests** – HTTP client for interacting with the USGS API  
- **Pendulum / datetime** – Date and time handling for scheduling and API parameters  

---

## Data Source

- **Provider:** United States Geological Survey (USGS)  
- **Endpoint Example:**
