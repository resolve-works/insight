
test:
	npx playwright test

test-headed:
	npx playwright test --headed

codegen:
	npx playwright codegen http://localhost:3000 --viewport-size "1900, 1000"

rabbitmq_dump_definitions:
	docker-compose exec rabbitmq rabbitmqctl export_definitions - | jq

rabbitmq_hash_password:
	docker run -it rabbitmq rabbitmqctl hash_password

opensearch_hash_password:
	docker run -it opensearchproject/opensearch /usr/share/opensearch/plugins/opensearch-security/tools/hash.sh
