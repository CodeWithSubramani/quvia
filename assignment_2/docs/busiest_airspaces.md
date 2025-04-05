### Busiest Airspaces

![img.png](img.png)

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

To optimize for the above query, did the following:

1. Created materialized columns

```sql
    lon_grid_materialized Float64 MATERIALIZED floor(longitude/0.5)*0.5,
    lat_grid_materialized Float64 MATERIALIZED floor(latitude/0.5)*0.5
```

2. Used `AggregatingMergeTree`

```shell
ENGINE = AggregatingMergeTree()
```

3. Using `Adaptive Partitioning`
   For the current 2 days it's partitioned by the hour, and for previous one's its done by the day

```
PARTITION BY (
    CASE 
        WHEN date >= today() - 1 THEN toStartOfHour(timestamp)
        ELSE toDate(timestamp)
    END
)
```