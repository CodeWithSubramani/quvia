export PYTHONPATH=$(PWD)

stop:
	docker compose down -v
setup:
	docker compose up -d
	sleep 20 #harcoded for containers to be up
schema:
	bash setup_scripts/register_schema.sh
	python3 setup_scripts/clickhouse_schema_create.py
start:
	make setup
	make schema
	#python3 mocker_flight_service.py
	#python3 producer_to_kafka.py

restart:
	make stop
	make start