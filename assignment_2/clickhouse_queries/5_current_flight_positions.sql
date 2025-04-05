CREATE MATERIALIZED VIEW flight_data.current_flight_positions
ENGINE = AggregatingMergeTree
ORDER BY flight_id
POPULATE AS
SELECT
    flight_id,
    argMaxState(hex, timestamp) AS hex_state,
    argMaxState(callsign, timestamp) AS callsign_state,
    argMaxState(latitude, timestamp) AS latitude_state,
    argMaxState(longitude, timestamp) AS longitude_state,
    argMaxState(track, timestamp) AS track_state,
    argMaxState(altitude, timestamp) AS altitude_state,
    argMaxState(gspeed, timestamp) AS gspeed_state,
    argMaxState(vspeed, timestamp) AS vspeed_state,
    argMaxState(squawk, timestamp) AS squawk_state,
    max(timestamp) AS last_update,
    now() AS query_time
FROM flight_data.flight_positions
GROUP BY flight_id;
