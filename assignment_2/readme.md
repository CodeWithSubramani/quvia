airflow creds

Airflow Credentials

```shell
admin
admin
```

clickhouse creds

```shell
default
admin
```

I could not get the network issues between docker containers solved, so the ingestion i am doing outside of airflow

### Analytics

1. Below query shall in realtime give the top 10 busiest air spaces

```sql
SELECT 
    floor(longitude/0.5)*0.5 AS lon_grid,
    floor(latitude/0.5)*0.5 AS lat_grid,
    count() AS flight_count
FROM flight_data.flight_positions
WHERE timestamp >= now() - INTERVAL 1 HOUR
GROUP BY lon_grid, lat_grid
ORDER BY flight_count DESC
LIMIT 10;
```

2. Tracking specific flights over time

```sql
-- Latest position for a specific flight by callsign
SELECT *
FROM flight_data.flight_positions
WHERE callsign = 'AAR501'
ORDER BY timestamp DESC
LIMIT 1;

-- Flight path for a specific flight
SELECT 
    timestamp,
    longitude,
    latitude,
    altitude
FROM flight_data.flight_positions
WHERE flight_id = '39c13279'
ORDER BY timestamp;

-- Current flights in a specific area (real-time bounding box)
SELECT 
    flight_id,
    callsign,
    altitude,
    gspeed,
    timestamp
FROM flight_data.flight_positions
WHERE 
    longitude BETWEEN -122.5 AND -122.3 AND
    latitude BETWEEN 37.7 AND 37.9 AND
    timestamp >= now() - INTERVAL 5 MINUTE
ORDER BY timestamp DESC;

```

3. Flight Patterns

```sql

-- at what hour there are most flights in the air
SELECT 
    hour,
    count() AS flights
FROM flight_data.flight_positions
WHERE date BETWEEN today() - 7 AND today()
GROUP BY hour
ORDER BY hour;

-- Average altitude by hour of day
SELECT 
    hour,
    avg(altitude) AS avg_altitude
FROM flight_data.flight_positions
WHERE date BETWEEN today() - 30 AND today()
GROUP BY hour
ORDER BY hour;

-- Flight path frequency (popular routes)
SELECT
    geoToH3(longitude, latitude, 7) AS h3_cell,
    count() AS frequency
FROM flight_data.flight_positions
WHERE date BETWEEN today() - INTERVAL 30 DAY AND today()
GROUP BY h3_cell
ORDER BY frequency DESC
LIMIT 100;


-- Seasonal flight pattern changes (monthly comparison)
SELECT 
    toMonth(timestamp) AS month,
    count() AS flight_count
FROM flight_data.flight_positions
WHERE timestamp >= now() - INTERVAL 1 YEAR
GROUP BY month
ORDER BY month;


```