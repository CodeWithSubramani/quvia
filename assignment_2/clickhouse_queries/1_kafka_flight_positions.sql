CREATE TABLE flight_data.kafka_flight_positions
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
    squawk Nullable(String)
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