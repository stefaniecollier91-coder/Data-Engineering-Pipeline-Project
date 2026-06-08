-- Reporting view for Dash MVP
-- Matches the CVG Database Project Deliverables schema and the uploaded
-- initial_postgresql_load_script.sql file.

CREATE OR REPLACE VIEW vw_monthly_flight_weather_summary AS
SELECT
    a.airport_code,
    a.airport_name,
    dm.year_number,
    dm.month_number,
    dm.month_name,
    dm.season,
    f.flight_operations,
    f.on_time_arrivals,
    f.on_time_pct,
    f.arrival_delays,
    f.delayed_pct,
    f.flight_cancelled,
    f.cancelled_pct,
    f.diverted_flights,
    ROUND(AVG(w.temperature_avg_f)::numeric, 2) AS avg_temperature_f,
    COALESCE(ROUND(SUM(w.precipitation_inches)::numeric, 3), 0) AS total_precipitation_inches,
    COALESCE(ROUND(SUM(w.snowfall_inches)::numeric, 3), 0) AS total_snowfall_inches,
    ROUND(AVG(w.wind_speed_avg_mph)::numeric, 2) AS avg_wind_speed_mph,
    COALESCE(SUM(CASE WHEN w.severe_weather_flag THEN 1 ELSE 0 END), 0) AS severe_weather_days
FROM flight_monthly_performance f
JOIN airport a ON f.airport_id = a.airport_id
JOIN date_month dm ON f.month_id = dm.month_id
LEFT JOIN weather_daily w
    ON w.airport_id = a.airport_id
    AND DATE_TRUNC('month', w.weather_date)::date = dm.month_start_date
GROUP BY
    a.airport_code, a.airport_name, dm.year_number, dm.month_number,
    dm.month_name, dm.season, f.flight_operations, f.on_time_arrivals,
    f.on_time_pct, f.arrival_delays, f.delayed_pct, f.flight_cancelled,
    f.cancelled_pct, f.diverted_flights
ORDER BY dm.year_number, dm.month_number;
