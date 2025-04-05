#!/bin/bash

curl -X POST http://localhost:8081/subjects/flight_positions-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schema": "{\"type\":\"record\",\"name\":\"FlightPosition\",\"namespace\":\"com.flight.analytics\",\"fields\":[{\"name\":\"flight_id\",\"type\":\"string\"},{\"name\":\"callsign\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"latitude\",\"type\":\"double\"},{\"name\":\"longitude\",\"type\":\"double\"},{\"name\":\"altitude\",\"type\":\"float\"},{\"name\":\"speed\",\"type\":\"float\"},{\"name\":\"heading\",\"type\":\"float\"},{\"name\":\"vertical_rate\",\"type\":[\"null\",\"float\"],\"default\":null},{\"name\":\"timestamp\",\"type\":\"long\"},{\"name\":\"origin\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"destination\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"squawk\",\"type\":[\"null\",\"string\"],\"default\":null}]}"
  }'
