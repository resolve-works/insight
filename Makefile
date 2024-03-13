
pg_format:
	pg_format ./database/**/*.sql -i

rabbitmq_dump_definitions:
	docker-compose exec rabbitmq rabbitmqctl export_definitions - | jq
