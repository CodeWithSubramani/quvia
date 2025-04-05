
-- Final table
CREATE TABLE IF NOT EXISTS flight_data.flight_positions
(
    flight_id String,
    hex Nullable(String),
    callsign Nullable(String),
    latitude Float64,
    longitude Float64,
    track Float32,
    altitude Float32,
    gspeed Float32,
    vspeed Float32,
    squawk Nullable(String),
    timestamp DateTime64(3),
    source Nullable(String),
    -- Generated columns for optimization
    date Date DEFAULT toDate(timestamp),
    hour UInt8 DEFAULT toHour(timestamp),
    geo_point Point DEFAULT (longitude, latitude),
    -- Materialized columns created
    lon_grid_materialized Float64 MATERIALIZED floor(longitude/0.5)*0.5,
    lat_grid_materialized Float64 MATERIALIZED floor(latitude/0.5)*0.5
)
ENGINE = AggregatingMergeTree()-- Plan is to run frequent aggregations on this in real time
PARTITION BY (
    CASE
        WHEN date >= today() - 7 THEN toStartOfHour(timestamp)
        ELSE toDate(timestamp)
    END
)
ORDER BY (flight_id, timestamp)
SETTINGS index_granularity = 8192;
