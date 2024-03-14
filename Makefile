
rabbitmq_dump_definitions:
	docker-compose exec rabbitmq rabbitmqctl export_definitions - | jq

rabbitmq_hash_password:
	docker run -it rabbitmq rabbitmqctl hash_password

opensearch_hash_password:
	docker run -it opensearchproject/opensearch /usr/share/opensearch/plugins/opensearch-security/tools/hash.sh
