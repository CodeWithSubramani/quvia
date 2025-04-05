from clickhouse_client import execute_file


def test_run_flight_data():
    res = execute_file('1_create_database.sql')
    res = execute_file('1_kafka_flight_positions.sql')
    res = execute_file('2_flight_positions.sql')
    res = execute_file('3_flight_positions_mv.sql')
    res = execute_file('4_test.sql')
    print('\n')
    print(res)
    assert True
