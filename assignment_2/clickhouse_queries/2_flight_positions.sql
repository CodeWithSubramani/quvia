
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
    geo_point Point DEFAULT (longitude, latitude)
)
ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (flight_id, timestamp)
SETTINGS index_granularity = 8192;
