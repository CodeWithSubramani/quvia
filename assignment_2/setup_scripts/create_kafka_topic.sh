#Create Kafka topic
docker exec -it kafka bash -c \
  "kafka-topics --bootstrap-server kafka:9092 --list | grep -q '^flight_positions$' || \
   kafka-topics --bootstrap-server kafka:9092 \
     --create \
     --topic flight_positions \
     --partitions 3 \
     --replication-factor 1 \
     --config retention.ms=604800000"