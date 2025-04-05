
-- Current positions view (latest position per flight)
CREATE MATERIALIZED VIEW flight_data.current_flight_positions
ENGINE = ReplacingMergeTree()
ORDER BY flight_id
POPULATE
AS
SELECT
    flight_id,
    argMax(callsign, timestamp) AS callsign,
    argMax(latitude, timestamp) AS latitude,
    argMax(longitude, timestamp) AS longitude,
    argMax(altitude, timestamp) AS altitude,
    argMax(speed, timestamp) AS speed,
    argMax(heading, timestamp) AS heading,
    argMax(geo_point, timestamp) AS geo_point,
    max(timestamp) AS last_update
FROM flight_data.flight_positions
GROUP BY flight_id;

CREATE MATERIALIZED VIEW flight_data.flight_trajectories
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (flight_id, date)
AS
WITH ordered_flights AS (
    SELECT
        flight_id,
        toDate(timestamp) AS date,
        timestamp,
        geo_point,
        speed,
        neighbor(geo_point.1, 1, 0) AS next_lon,
        neighbor(geo_point.2, 1, 0) AS next_lat,
        neighbor(flight_id, 1) AS next_flight_id
    FROM flight_data.flight_positions
    ORDER BY flight_id, timestamp
)
SELECT
    flight_id,
    date,
    min(timestamp) AS first_seen,
    max(timestamp) AS last_seen,
    sum(if(next_flight_id = flight_id,
           greatCircleDistance(geo_point.1, geo_point.2, next_lon, next_lat),
           0)) AS distance_traveled,
    avg(speed) AS avg_speed,
    groupArray(geo_point) AS path
FROM ordered_flights
GROUP BY flight_id, date;