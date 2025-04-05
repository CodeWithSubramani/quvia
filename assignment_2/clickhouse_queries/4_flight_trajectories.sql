CREATE MATERIALIZED VIEW flight_data.flight_trajectories_mv
ENGINE = ReplacingMergeTree(timestamp)
PARTITION BY toDate(timestamp)
ORDER BY (flight_id, timestamp)
POPULATE AS
SELECT
    flight_id,
    callsign,
    hex,
    timestamp,
    latitude,
    longitude,
    altitude,
    gspeed,
    vspeed,
    track,
    toDate(timestamp) AS date
FROM flight_data.flight_positions;