
backbone:
	docker-compose up -d keycloak minio minio_init opensearch postgres postgrest rabbitmq

workers:
	docker-compose up -d worker ingest

install_dependencies:
	npm install && npx playwright install

run_test:
	npx playwright test

run_test_headed:
	npx playwright test --headed

codegen:
	npx playwright codegen --browser firefox --ignore-https-errors http://localhost:3000

reset_database:
	docker-compose exec postgres /bin/sh -c 'dropdb --username=$$POSTGRES_USER insight'
	docker-compose exec postgres /bin/sh -c 'createdb --username=$$POSTGRES_USER insight'
	docker-compose exec postgres /bin/sh -c 'psql --username=$$POSTGRES_USER -f /docker-entrypoint-initdb.d/init.sql'

rabbitmq_dump_definitions:
	docker-compose exec rabbitmq rabbitmqctl export_definitions - | jq

rabbitmq_hash_password:
	docker run -it rabbitmq rabbitmqctl hash_password

opensearch_hash_password:
	docker run -it opensearchproject/opensearch /usr/share/opensearch/plugins/opensearch-security/tools/hash.sh
