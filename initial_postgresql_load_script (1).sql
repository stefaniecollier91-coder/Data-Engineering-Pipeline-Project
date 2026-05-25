-- Initial PostgreSQL Load Script
-- Project: Flight Delays and Weather Impact Analysis at Cincinnati/Northern Kentucky International Airport (CVG)
-- Author: Stefanie Collier
-- Purpose: Create the database schema and load initial sample data for the CVG flight delay and weather impact project.

DROP TABLE IF EXISTS weather_daily CASCADE;
DROP TABLE IF EXISTS flight_monthly_performance CASCADE;
DROP TABLE IF EXISTS etl_run_log CASCADE;
DROP TABLE IF EXISTS date_month CASCADE;
DROP TABLE IF EXISTS airline CASCADE;
DROP TABLE IF EXISTS airport CASCADE;

CREATE TABLE airport (
    airport_id SERIAL PRIMARY KEY,
    airport_code VARCHAR(10) NOT NULL UNIQUE,
    airport_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'USA',
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6)
);

CREATE TABLE airline (
    airline_id SERIAL PRIMARY KEY,
    carrier_code VARCHAR(10) NOT NULL UNIQUE,
    carrier_name VARCHAR(150) NOT NULL
);

CREATE TABLE date_month (
    month_id SERIAL PRIMARY KEY,
    month_start_date DATE NOT NULL UNIQUE,
    year_number INTEGER NOT NULL,
    month_number INTEGER NOT NULL CHECK (month_number BETWEEN 1 AND 12),
    month_name VARCHAR(20) NOT NULL,
    season VARCHAR(20) NOT NULL,
    CONSTRAINT uq_year_month UNIQUE (year_number, month_number)
);

CREATE TABLE flight_monthly_performance (
    performance_id SERIAL PRIMARY KEY,
    airport_id INTEGER NOT NULL REFERENCES airport(airport_id),
    airline_id INTEGER REFERENCES airline(airline_id),
    month_id INTEGER NOT NULL REFERENCES date_month(month_id),
    on_time_arrivals INTEGER NOT NULL CHECK (on_time_arrivals >= 0),
    on_time_pct NUMERIC(5,2) CHECK (on_time_pct >= 0 AND on_time_pct <= 100),
    arrival_delays INTEGER NOT NULL CHECK (arrival_delays >= 0),
    delayed_pct NUMERIC(5,2) CHECK (delayed_pct >= 0 AND delayed_pct <= 100),
    flight_cancelled INTEGER NOT NULL CHECK (flight_cancelled >= 0),
    cancelled_pct NUMERIC(5,2) CHECK (cancelled_pct >= 0 AND cancelled_pct <= 100),
    diverted_flights INTEGER NOT NULL CHECK (diverted_flights >= 0),
    flight_operations INTEGER NOT NULL CHECK (flight_operations >= 0),
    source_system VARCHAR(100) DEFAULT 'BTS TranStats',
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_performance_record UNIQUE (airport_id, airline_id, month_id)
);

CREATE TABLE weather_daily (
    weather_id SERIAL PRIMARY KEY,
    airport_id INTEGER NOT NULL REFERENCES airport(airport_id),
    weather_date DATE NOT NULL,
    temperature_avg_f NUMERIC(6,2),
    precipitation_inches NUMERIC(8,3) DEFAULT 0,
    snowfall_inches NUMERIC(8,3) DEFAULT 0,
    wind_speed_avg_mph NUMERIC(6,2),
    weather_condition VARCHAR(100),
    severe_weather_flag BOOLEAN DEFAULT FALSE,
    source_system VARCHAR(100) DEFAULT 'Open-Meteo API',
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_airport_weather_date UNIQUE (airport_id, weather_date)
);

CREATE TABLE etl_run_log (
    run_id SERIAL PRIMARY KEY,
    run_name VARCHAR(100) NOT NULL,
    source_system VARCHAR(100) NOT NULL,
    run_status VARCHAR(30) NOT NULL,
    records_loaded INTEGER DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    notes TEXT
);

CREATE INDEX idx_flight_perf_airport_month ON flight_monthly_performance(airport_id, month_id);
CREATE INDEX idx_weather_airport_date ON weather_daily(airport_id, weather_date);
CREATE INDEX idx_date_month_year_month ON date_month(year_number, month_number);

INSERT INTO airport (airport_code, airport_name, city, state, latitude, longitude)
VALUES ('CVG', 'Cincinnati/Northern Kentucky International Airport', 'Hebron', 'Kentucky', 39.048801, -84.667801);

INSERT INTO airline (carrier_code, carrier_name)
VALUES ('ALL', 'All Marketing Carriers - Monthly Aggregate');

INSERT INTO date_month (month_start_date, year_number, month_number, month_name, season)
VALUES
('2023-01-01', 2023, 1, 'January', 'Winter'),
('2023-02-01', 2023, 2, 'February', 'Winter'),
('2023-03-01', 2023, 3, 'March', 'Spring'),
('2023-04-01', 2023, 4, 'April', 'Spring'),
('2023-05-01', 2023, 5, 'May', 'Spring'),
('2023-06-01', 2023, 6, 'June', 'Summer'),
('2023-07-01', 2023, 7, 'July', 'Summer');

-- Initial BTS TranStats sample rows supplied for CVG monthly performance.
INSERT INTO flight_monthly_performance (
    airport_id, airline_id, month_id, on_time_arrivals, on_time_pct,
    arrival_delays, delayed_pct, flight_cancelled, cancelled_pct,
    diverted_flights, flight_operations
)
SELECT a.airport_id, al.airline_id, dm.month_id, v.on_time_arrivals, v.on_time_pct,
       v.arrival_delays, v.delayed_pct, v.flight_cancelled, v.cancelled_pct,
       v.diverted_flights, v.flight_operations
FROM (VALUES
    ('2023-01-01'::date, 2460, 74.12, 700, 18.31, 156, 4.70, 3, 3319),
    ('2023-02-01'::date, 2337, 74.71, 739, 20.50, 48, 1.53, 4, 3128),
    ('2023-03-01'::date, 2918, 76.13, 865, 19.20, 43, 1.12, 7, 3833),
    ('2023-04-01'::date, 2776, 74.95, 890, 19.36, 32, 0.86, 6, 3704),
    ('2023-05-01'::date, 2699, 72.07, 998, 23.26, 44, 1.17, 4, 3745),
    ('2023-06-01'::date, 2503, 65.39, 1229, 27.70, 85, 2.22, 11, 3828),
    ('2023-07-01'::date, 2471, 62.73, 1322, 27.72, 128, 3.25, 18, 3939)
) AS v(month_start_date, on_time_arrivals, on_time_pct, arrival_delays, delayed_pct, flight_cancelled, cancelled_pct, diverted_flights, flight_operations)
JOIN airport a ON a.airport_code = 'CVG'
JOIN airline al ON al.carrier_code = 'ALL'
JOIN date_month dm ON dm.month_start_date = v.month_start_date;

-- Daily weather rows below are placeholders to confirm table structure.
-- Replace or append these rows with Open-Meteo API output generated by the Python ETL pipeline.
INSERT INTO weather_daily (
    airport_id, weather_date, temperature_avg_f, precipitation_inches,
    snowfall_inches, wind_speed_avg_mph, weather_condition, severe_weather_flag
)
SELECT airport_id, weather_date, temperature_avg_f, precipitation_inches, snowfall_inches,
       wind_speed_avg_mph, weather_condition, severe_weather_flag
FROM airport a
CROSS JOIN (VALUES
    ('2023-01-01'::date, NULL::numeric, NULL::numeric, NULL::numeric, NULL::numeric, 'Open-Meteo load pending', FALSE),
    ('2023-02-01'::date, NULL::numeric, NULL::numeric, NULL::numeric, NULL::numeric, 'Open-Meteo load pending', FALSE),
    ('2023-03-01'::date, NULL::numeric, NULL::numeric, NULL::numeric, NULL::numeric, 'Open-Meteo load pending', FALSE)
) AS w(weather_date, temperature_avg_f, precipitation_inches, snowfall_inches, wind_speed_avg_mph, weather_condition, severe_weather_flag)
WHERE a.airport_code = 'CVG';

INSERT INTO etl_run_log (run_name, source_system, run_status, records_loaded, completed_at, notes)
VALUES
('Initial airport and airline reference load', 'Manual seed data', 'Completed', 2, CURRENT_TIMESTAMP, 'Loaded CVG airport and aggregate carrier reference rows.'),
('Initial flight performance load', 'BTS TranStats', 'Completed', 7, CURRENT_TIMESTAMP, 'Loaded initial monthly CVG flight performance sample rows.'),
('Initial weather structure load', 'Open-Meteo API', 'Pending', 0, NULL, 'Weather API extraction will populate daily weather records.');

-- Useful reporting view for Power BI.
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
    AVG(w.temperature_avg_f) AS avg_temperature_f,
    SUM(w.precipitation_inches) AS total_precipitation_inches,
    SUM(w.snowfall_inches) AS total_snowfall_inches,
    AVG(w.wind_speed_avg_mph) AS avg_wind_speed_mph,
    SUM(CASE WHEN w.severe_weather_flag THEN 1 ELSE 0 END) AS severe_weather_days
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
