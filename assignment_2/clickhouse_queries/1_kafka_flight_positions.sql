-- Kafka engine table
CREATE TABLE flight_data.kafka_flight_positions
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
    source Nullable(String)
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'flight_positions',
    kafka_group_name = 'clickhouse_consumer_group',
    kafka_format = 'AvroConfluent',
    format_avro_schema_registry_url = 'http://schema-registry:8081',
    kafka_num_consumers = 3,
    kafka_skip_broken_messages = 100;

