from methods.clickhouse_client import execute_file

execute_file('1_create_database.sql')
execute_file('1_kafka_flight_positions.sql')
execute_file('2_flight_positions.sql')
execute_file('3_flight_positions_mv.sql')
execute_file('4_flight_trajectories.sql')
execute_file('5_current_flight_positions.sql')
