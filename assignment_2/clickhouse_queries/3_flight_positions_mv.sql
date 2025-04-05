CREATE MATERIALIZED VIEW flight_data.flight_positions_mv TO flight_data.flight_positions
AS SELECT * FROM flight_data.kafka_flight_positions;


