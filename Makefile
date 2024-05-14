
backbone:
	docker-compose up -d keycloak minio minio_init opensearch postgres postgrest rabbitmq

install:
	npm install && npx playwright install firefox

run_test:
	npx playwright test

run_test_headed:
	npx playwright test --headed

codegen:
	npx playwright codegen -b firefox --ignore-https-errors http://localhost:3000

rabbitmq_dump_definitions:
	docker-compose exec rabbitmq rabbitmqctl export_definitions - | jq

rabbitmq_hash_password:
	docker run -it rabbitmq rabbitmqctl hash_password

opensearch_hash_password:
	docker run -it opensearchproject/opensearch /usr/share/opensearch/plugins/opensearch-security/tools/hash.sh
