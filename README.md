# CVG Flight Delays & Weather Analytics Dash MVP

## Project Overview
This Dash application is an interactive analytics dashboard for the **Flight Delays and Weather Impact Analysis at CVG** project. The app matches the uploaded database deliverables and connects to the PostgreSQL schema created by `initial_postgresql_load_script.sql`.

The dashboard reads from `vw_monthly_flight_weather_summary`, a reporting view that joins:

- `airport`
- `date_month`
- `flight_monthly_performance`
- `weather_daily`

The project focuses on Cincinnati/Northern Kentucky International Airport (CVG), monthly BTS TranStats flight performance data, and Open-Meteo weather observations.

## Business Questions
The dashboard is designed to answer:

1. Which months had the weakest on-time flight performance?
2. Which months had the highest arrival delay percentage?
3. How do delays, cancellations, and diversions compare by month or season?
4. Do weather indicators such as precipitation and severe weather days align with flight disruptions?
5. What KPI metrics summarize CVG operations for a selected period?

## Required Features Covered

- **Database connectivity:** Uses SQLAlchemy and `psycopg2-binary` to connect to PostgreSQL through `POSTGRES_URL`.
- **Live/refreshed data:** Queries the PostgreSQL reporting view and includes a Refresh button.
- **2+ visualizations:** Includes a trend line chart, disruption bar chart, precipitation vs. delay scatter plot, and severe weather days bar chart.
- **Interactive filter:** Season dropdown updates KPI cards, charts, and the data table.
- **KPI cards:** Shows total operations, average on-time rate, total arrival delays, and severe weather days.
- **Navigation/layout:** Uses tabs for Performance Overview, Weather Relationship, and Data Table.
- **Professional design:** Uses Dash Bootstrap Components and custom CSS.

## Repository Structure

```text
cvg_dash_mvp/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── assets/
│   └── style.css
├── sql/
│   ├── initial_postgresql_load_script.sql
│   └── create_reporting_view.sql
├── docs/
│   ├── database_schema_documentation.docx
│   ├── er_diagram.png
│   └── er_diagram.dot
└── screenshots/
```

## How to Run the App

### 1. Clone the repository

```bash
git clone <your-github-repo-link>
cd cvg_dash_mvp
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create and load the PostgreSQL database

Create a PostgreSQL database named something like:

```text
cvg_flight_weather
```

Then run the provided SQL file:

```bash
psql -d cvg_flight_weather -f sql/initial_postgresql_load_script.sql
```

You can also open `sql/initial_postgresql_load_script.sql` in pgAdmin Query Tool and run it there.

### 5. Confirm or recreate the reporting view

The initial load script already creates `vw_monthly_flight_weather_summary`. If you need to refresh just the Dash reporting view, run:

```bash
psql -d cvg_flight_weather -f sql/create_reporting_view.sql
```

### 6. Configure PostgreSQL connection

Copy the environment example file:

```bash
copy .env.example .env
```

Mac/Linux:

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL connection string:

```text
POSTGRES_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/cvg_flight_weather
ALLOW_SAMPLE_FALLBACK=false
```

### 7. Start the Dash app

```bash
python app.py
```

Open the browser link shown in the terminal, usually:

```text
http://127.0.0.1:8050/
```

## Optional Local Demo Mode

The final submission should use PostgreSQL. If you only need to preview the layout before your database is ready, set this in `.env`:

```text
ALLOW_SAMPLE_FALLBACK=true
```

When fallback mode is enabled, the app displays embedded sample data based on the uploaded initial SQL file and shows a banner that the database is not being used. For grading, keep `ALLOW_SAMPLE_FALLBACK=false` and confirm the app connects to PostgreSQL.

## Dashboard Screenshots

The `screenshots/` folder includes screenshots captured from the running Dash MVP.

### Weather Relationship Tab

![Weather Relationship Tab](screenshots/weather_relationship_1.png)

### Weather Relationship Tab - Alternate View

![Weather Relationship Alternate View](screenshots/weather_relationship_2.png)

### Data Table Tab

![Data Table Tab](screenshots/data_table.png)

## Business Insights Summary

The dashboard highlights CVG monthly flight performance using the seven months of sample data in the project database. In the loaded sample, June and July show weaker on-time performance and higher delayed percentages than the earlier months. The disruption chart shows how arrival delays, cancellations, and diversions compare across months. The weather relationship tab is ready to show precipitation and severe weather patterns once the Open-Meteo ETL load fully populates the `weather_daily` table.

## Dependencies

- Dash
- Dash Bootstrap Components
- Plotly
- Pandas
- SQLAlchemy
- psycopg2-binary
- python-dotenv

## Submission Checklist

- [ ] Upload this project folder to GitHub.
- [ ] Confirm `.env` is not committed.
- [ ] Run `sql/initial_postgresql_load_script.sql` in PostgreSQL.
- [ ] Confirm `POSTGRES_URL` works locally.
- [ ] Start the Dash app successfully.
- [ ] Add screenshots or a demo GIF to the README.
- [ ] Submit the GitHub repository link.
