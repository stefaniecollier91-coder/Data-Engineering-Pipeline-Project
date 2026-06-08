"""
Dash MVP: Flight Delays and Weather Impact Analysis at CVG
Author: Stefanie Collier

This app matches the CVG Database Project Deliverables schema. It connects to
PostgreSQL through POSTGRES_URL and reads vw_monthly_flight_weather_summary,
which joins airport, date_month, flight_monthly_performance, and weather_daily.
"""

import os
from datetime import datetime

import dash
from dash import Dash, Input, Output, State, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

APP_TITLE = "CVG Flight Delays & Weather Analytics"
POSTGRES_URL = os.getenv("POSTGRES_URL")
ALLOW_SAMPLE_FALLBACK = os.getenv("ALLOW_SAMPLE_FALLBACK", "false").lower() == "true"

REPORTING_QUERY = """
SELECT
    airport_code,
    airport_name,
    year_number,
    month_number,
    month_name,
    season,
    flight_operations,
    on_time_arrivals,
    on_time_pct,
    arrival_delays,
    delayed_pct,
    flight_cancelled,
    cancelled_pct,
    diverted_flights,
    avg_temperature_f,
    total_precipitation_inches,
    total_snowfall_inches,
    avg_wind_speed_mph,
    severe_weather_days
FROM vw_monthly_flight_weather_summary
ORDER BY year_number, month_number;
"""

# Local fallback mirrors the uploaded initial_postgresql_load_script.sql sample.
# Final grading should use PostgreSQL with ALLOW_SAMPLE_FALLBACK=false.
SAMPLE_DATA = [
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":1,"month_name":"January","season":"Winter","flight_operations":3319,"on_time_arrivals":2460,"on_time_pct":74.12,"arrival_delays":700,"delayed_pct":18.31,"flight_cancelled":156,"cancelled_pct":4.70,"diverted_flights":3,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":2,"month_name":"February","season":"Winter","flight_operations":3128,"on_time_arrivals":2337,"on_time_pct":74.71,"arrival_delays":739,"delayed_pct":20.50,"flight_cancelled":48,"cancelled_pct":1.53,"diverted_flights":4,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":3,"month_name":"March","season":"Spring","flight_operations":3833,"on_time_arrivals":2918,"on_time_pct":76.13,"arrival_delays":865,"delayed_pct":19.20,"flight_cancelled":43,"cancelled_pct":1.12,"diverted_flights":7,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":4,"month_name":"April","season":"Spring","flight_operations":3704,"on_time_arrivals":2776,"on_time_pct":74.95,"arrival_delays":890,"delayed_pct":19.36,"flight_cancelled":32,"cancelled_pct":0.86,"diverted_flights":6,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":5,"month_name":"May","season":"Spring","flight_operations":3745,"on_time_arrivals":2699,"on_time_pct":72.07,"arrival_delays":998,"delayed_pct":23.26,"flight_cancelled":44,"cancelled_pct":1.17,"diverted_flights":4,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":6,"month_name":"June","season":"Summer","flight_operations":3828,"on_time_arrivals":2503,"on_time_pct":65.39,"arrival_delays":1229,"delayed_pct":27.70,"flight_cancelled":85,"cancelled_pct":2.22,"diverted_flights":11,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
    {"airport_code":"CVG","airport_name":"Cincinnati/Northern Kentucky International Airport","year_number":2023,"month_number":7,"month_name":"July","season":"Summer","flight_operations":3939,"on_time_arrivals":2471,"on_time_pct":62.73,"arrival_delays":1322,"delayed_pct":27.72,"flight_cancelled":128,"cancelled_pct":3.25,"diverted_flights":18,"avg_temperature_f":None,"total_precipitation_inches":0,"total_snowfall_inches":0,"avg_wind_speed_mph":None,"severe_weather_days":0},
]


def get_engine():
    if not POSTGRES_URL:
        raise RuntimeError("POSTGRES_URL is not set. Add it to your .env file.")
    return create_engine(POSTGRES_URL, pool_pre_ping=True)


def load_data():
    """Load reporting data from PostgreSQL, with an optional local fallback."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text(REPORTING_QUERY), conn)
        mode = "PostgreSQL live/refreshed data"
    except Exception as exc:
        if not ALLOW_SAMPLE_FALLBACK:
            raise RuntimeError(
                "Database connection failed. Confirm POSTGRES_URL is correct and "
                "vw_monthly_flight_weather_summary exists. Original error: " + str(exc)
            ) from exc
        df = pd.DataFrame(SAMPLE_DATA)
        mode = "Sample fallback data - configure PostgreSQL for final submission"

    numeric_cols = [
        "flight_operations", "on_time_arrivals", "on_time_pct", "arrival_delays",
        "delayed_pct", "flight_cancelled", "cancelled_pct", "diverted_flights",
        "avg_temperature_f", "total_precipitation_inches", "total_snowfall_inches",
        "avg_wind_speed_mph", "severe_weather_days",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # The uploaded initial SQL uses placeholder weather rows. Treat missing totals
    # as zero so the MVP remains readable until the ETL weather load is complete.
    for col in ["total_precipitation_inches", "total_snowfall_inches", "severe_weather_days"]:
        df[col] = df[col].fillna(0)

    df["month_label"] = df["month_name"].str.slice(0, 3) + " " + df["year_number"].astype(str)
    df = df.sort_values(["year_number", "month_number"])
    refreshed_at = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    return df, mode, refreshed_at


def metric_card(label, value, helper=""):
    return dbc.Col(
        html.Div(
            [
                html.Div(label, className="kpi-label"),
                html.Div(value, className="kpi-value"),
                html.Div(helper, className="kpi-label"),
            ],
            className="kpi-card",
        ),
        md=3,
    )


def format_number(value):
    return "N/A" if pd.isna(value) else f"{value:,.0f}"


def format_pct(value):
    return "N/A" if pd.isna(value) else f"{value:.1f}%"


df_initial, data_mode, refreshed_at = load_data()
season_options = [{"label": "All Seasons", "value": "All"}] + [
    {"label": s, "value": s} for s in sorted(df_initial["season"].dropna().unique())
]
metric_options = [
    {"label": "On-Time %", "value": "on_time_pct"},
    {"label": "Delayed %", "value": "delayed_pct"},
    {"label": "Cancelled %", "value": "cancelled_pct"},
    {"label": "Severe Weather Days", "value": "severe_weather_days"},
]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title=APP_TITLE)
server = app.server

app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(
                [
                    html.H1(APP_TITLE, className="app-title"),
                    html.P(
                        "Interactive MVP dashboard connected to the CVG PostgreSQL flight performance and weather schema.",
                        className="subtitle",
                    ),
                    html.Div(id="mode-banner", className="mode-banner panel"),
                ]
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Filter by Season"),
                            dcc.Dropdown(id="season-filter", options=season_options, value="All", clearable=False),
                        ],
                        className="panel",
                    ),
                    md=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Trend Metric"),
                            dcc.Dropdown(id="metric-filter", options=metric_options, value="on_time_pct", clearable=False),
                        ],
                        className="panel",
                    ),
                    md=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Refresh Database Data"),
                            html.Br(),
                            html.Button("Refresh", id="refresh-button", n_clicks=0, className="refresh-button"),
                        ],
                        className="panel",
                    ),
                    md=4,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(id="kpi-row", className="mb-3"),
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Performance Overview",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(html.Div(dcc.Graph(id="trend-chart"), className="panel"), md=7),
                                dbc.Col(html.Div(dcc.Graph(id="disruption-bar"), className="panel"), md=5),
                            ],
                            className="mt-3",
                        )
                    ],
                ),
                dbc.Tab(
                    label="Weather Relationship",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(html.Div(dcc.Graph(id="weather-scatter"), className="panel"), md=7),
                                dbc.Col(html.Div(dcc.Graph(id="weather-days-bar"), className="panel"), md=5),
                            ],
                            className="mt-3",
                        )
                    ],
                ),
                dbc.Tab(
                    label="Data Table",
                    children=[
                        html.Div(
                            dash_table.DataTable(
                                id="data-table",
                                page_size=10,
                                sort_action="native",
                                filter_action="native",
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left", "padding": "8px"},
                                style_header={"fontWeight": "bold"},
                            ),
                            className="panel mt-3",
                        )
                    ],
                ),
            ]
        ),
    ],
)


@app.callback(
    Output("mode-banner", "children"),
    Output("kpi-row", "children"),
    Output("trend-chart", "figure"),
    Output("disruption-bar", "figure"),
    Output("weather-scatter", "figure"),
    Output("weather-days-bar", "figure"),
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Input("season-filter", "value"),
    Input("metric-filter", "value"),
    Input("refresh-button", "n_clicks"),
)
def update_dashboard(selected_season, selected_metric, _refresh_clicks):
    df, mode, refreshed_at = load_data()
    if selected_season != "All":
        df = df[df["season"] == selected_season]

    total_ops = df["flight_operations"].sum()
    avg_on_time = df["on_time_pct"].mean()
    total_delays = df["arrival_delays"].sum()
    severe_days = df["severe_weather_days"].sum()

    kpis = [
        metric_card("Total Flight Operations", format_number(total_ops), "Selected period"),
        metric_card("Average On-Time Rate", format_pct(avg_on_time), "Higher is better"),
        metric_card("Total Arrival Delays", format_number(total_delays), "Delay count"),
        metric_card("Severe Weather Days", format_number(severe_days), "From weather_daily"),
    ]

    metric_label = next(item["label"] for item in metric_options if item["value"] == selected_metric)
    trend_fig = px.line(
        df,
        x="month_label",
        y=selected_metric,
        markers=True,
        title=f"Monthly Trend: {metric_label}",
        labels={"month_label": "Month", selected_metric: metric_label},
    )
    trend_fig.update_layout(margin=dict(l=20, r=20, t=55, b=20))

    disruption_fig = px.bar(
        df,
        x="month_label",
        y=["arrival_delays", "flight_cancelled", "diverted_flights"],
        title="Monthly Flight Disruptions",
        labels={"month_label": "Month", "value": "Flights", "variable": "Disruption Type"},
        barmode="group",
    )
    disruption_fig.update_layout(margin=dict(l=20, r=20, t=55, b=20))

    scatter_fig = px.scatter(
        df,
        x="total_precipitation_inches",
        y="delayed_pct",
        size="flight_operations",
        hover_name="month_label",
        title="Precipitation vs. Delay Rate",
        labels={
            "total_precipitation_inches": "Total Precipitation (inches)",
            "delayed_pct": "Delayed %",
            "flight_operations": "Flight Operations",
        },
    )
    scatter_fig.update_layout(margin=dict(l=20, r=20, t=55, b=20))

    weather_fig = px.bar(
        df,
        x="month_label",
        y="severe_weather_days",
        title="Severe Weather Days by Month",
        labels={"month_label": "Month", "severe_weather_days": "Days"},
    )
    weather_fig.update_layout(margin=dict(l=20, r=20, t=55, b=20))

    table_df = df[[
        "year_number", "month_name", "season", "flight_operations", "on_time_pct", "delayed_pct",
        "flight_cancelled", "diverted_flights", "total_precipitation_inches", "avg_wind_speed_mph", "severe_weather_days"
    ]].copy()
    columns = [{"name": col.replace("_", " ").title(), "id": col} for col in table_df.columns]
    banner = f"Data source mode: {mode} | Last refreshed: {refreshed_at}"

    return banner, kpis, trend_fig, disruption_fig, scatter_fig, weather_fig, table_df.to_dict("records"), columns


if __name__ == "__main__":
    app.run(debug=True)
