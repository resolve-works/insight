
dev:
	docker-compose up -d

backbone:
	docker-compose up -d keycloak minio minio_init opensearch postgres postgrest rabbitmq

workers:
	docker-compose up -d worker ingest

install_dependencies:
	npm install && npx playwright install

run_test:
	npx playwright test -j 4

test_ui:
	npx playwright test --ui

codegen:
	npx playwright codegen --browser firefox --ignore-https-errors http://localhost:3000

reset_database:
	docker-compose exec postgres /bin/sh -c 'dropdb --username=$$POSTGRES_USER insight'
	docker-compose exec postgres /bin/sh -c 'createdb --username=$$POSTGRES_USER insight'
	docker-compose exec postgres /bin/sh -c 'psql --username=$$POSTGRES_USER -f /docker-entrypoint-initdb.d/init.sql'

mc:
	docker-compose run minio_init /bin/sh -c 'mc alias set insight $$MINIO_ENDPOINT $$MINIO_ROOT_USER $$MINIO_ROOT_PASSWORD && /bin/sh'

rabbitmq_dump_definitions:
	docker-compose exec rabbitmq rabbitmqctl export_definitions - | jq

rabbitmq_hash_password:
	docker run -it rabbitmq rabbitmqctl hash_password

opensearch_hash_password:
	docker run -it opensearchproject/opensearch:2.12.0 /usr/share/opensearch/plugins/opensearch-security/tools/hash.sh
