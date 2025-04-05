import os

import clickhouse_connect


def get_query(file_name: str):
    root_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_path, 'clickhouse_queries', file_name), 'r') as f:
        query = f.read()
    return query


def execute_file(file_name: str):
    query = get_query(file_name)
    client = clickhouse_connect.get_client(host='localhost', port=8123, user='default')
    res = client.command(query)
    return res
