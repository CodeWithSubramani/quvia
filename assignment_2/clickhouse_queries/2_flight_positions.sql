CREATE TABLE if not exists  flight_data.flight_positions
(
    flight_id String,
    callsign Nullable(String),
    latitude Float64,
    longitude Float64,
    altitude Float32,
    speed Float32,
    heading Float32,
    vertical_rate Nullable(Float32),
    timestamp DateTime64(3),
    origin Nullable(String),
    destination Nullable(String),
    squawk Nullable(String),
    -- Generated columns for optimization
    date Date DEFAULT toDate(timestamp),
    hour UInt8 DEFAULT toHour(timestamp),
    geo_point Point DEFAULT (longitude, latitude)
)
ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (flight_id, timestamp)
SETTINGS index_granularity = 8192;

