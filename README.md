# CVG Flight Delays & Weather Analytics Dash MVP

## Project Overview
This Dash application is an interactive analytics dashboard for the **Flight Delays and Weather Impact Analysis at CVG** project. The dashboard connects to a PostgreSQL database, reads the `vw_monthly_flight_weather_summary` reporting view, and helps users evaluate how weather conditions relate to monthly flight delays, cancellations, diversions, and on-time performance at Cincinnati/Northern Kentucky International Airport.

## Business Questions
The dashboard is designed to answer:

1. Which months had the weakest on-time flight performance?
2. Do months with more severe weather days also show higher delay percentages?
3. How do cancellations, diversions, and arrival delays compare across months or seasons?
4. What overall KPI metrics summarize CVG operating performance for a selected period?

## Required Features Covered

- **Database connectivity:** Uses SQLAlchemy and `psycopg2-binary` to connect to PostgreSQL through `POSTGRES_URL`.
- **Live/refreshed data:** Queries the database reporting view when the app loads.
- **2+ visualizations:** Includes trend line, disruption bar chart, weather scatter plot, and severe weather bar chart.
- **Interactive filter:** Season dropdown updates KPIs, charts, and data table.
- **KPI cards:** Shows total operations, average on-time rate, total delays, and severe weather days.
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
│   └── create_reporting_view.sql
└── screenshots/
```

## How to Run the App

### 1. Clone the repository

```bash
git clone <your-github-repo-link>
cd cvg_dash_mvp
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

For Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL connection

Copy the environment example file:

```bash
copy .env.example .env
```

For Mac/Linux:

```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL connection string:

```text
POSTGRES_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/cvg_flight_weather
ALLOW_SAMPLE_FALLBACK=false
```

### 5. Create the reporting view

After your Week 3 ETL pipeline loads the PostgreSQL tables, run:

```bash
psql -d cvg_flight_weather -f sql/create_reporting_view.sql
```

Or run the SQL file inside pgAdmin Query Tool.

### 6. Start the Dash app

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

When fallback mode is enabled, the app displays embedded sample data and shows a banner that the database is not being used. For grading, keep `ALLOW_SAMPLE_FALLBACK=false` and confirm the app connects to PostgreSQL.

## Dashboard Screenshots

Add screenshots or a short demo GIF to the `screenshots/` folder before submitting. Recommended screenshots:

1. Performance Overview tab with KPI cards and charts.
2. Weather Relationship tab showing the precipitation vs. delay scatter plot.
3. Data Table tab with filtered monthly results.

Markdown example after adding a screenshot:

```markdown
![Performance Overview](screenshots/performance_overview.png)
```

## Business Insights Summary

The dashboard highlights that CVG's on-time performance weakened during the summer months in the sample data. June and July show lower on-time percentages and higher delayed percentages compared with winter and spring months. The weather relationship view helps identify whether months with higher precipitation or more severe weather days also had more delays, cancellations, or diversions. These insights can support airport operations planning, staffing, disruption monitoring, and communication strategies during high-risk weather periods.

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
- [ ] Add PostgreSQL connection details locally.
- [ ] Run the Week 3 ETL pipeline and load the PostgreSQL database.
- [ ] Run `sql/create_reporting_view.sql`.
- [ ] Start the Dash app successfully.
- [ ] Add screenshots or a demo GIF to the README.
- [ ] Submit the GitHub repository link.
