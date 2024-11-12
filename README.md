# Insight

Insight turns data into information, by putting it into context. It allows you
to search through a set of documents by keyword, and to prompt a
[LLM](https://en.wikipedia.org/wiki/Large_language_model) about sets documents
through the use of
[RAG](https://research.ibm.com/blog/retrieval-augmented-generation-RAG).

The initial development of Insight was funded by Follow the Money
([ftm.nl](https://ftm.nl)/ [ftm.eu](https://ftm.eu)) to process large amount of
FOIA requests.

## Setting up

First copy the provided `.env.sample` environment file to a `.env` file:

```
cp .env.example .env
```

You'll need to add a [OpenAI api key](https://platform.openai.com/api-keys) to
the `.env` file as `OPENAI_API_KEY`.

### Certificates

We have to encrypt the traffic to our local keycloak instance because rabbitMQ
is [very serious about following the
spec](https://github.com/rabbitmq/rabbitmq-server/blob/main/deps/rabbitmq_auth_backend_oauth2/README.md#variables-configurable-in-rabbitmqconf),
and won't allow us to use a HTTP key server. Opensearch also requires SSL
certificates to run.

You can easily generate certificates with
[`mkcert`](https://github.com/FiloSottile/mkcert). To generate development
certificates:

```
mkdir certs
cp `mkcert -CAROOT`/rootCA.pem ./certs
mkcert -cert-file ./certs/opensearch.pem -key-file ./certs/opensearch-key.pem opensearch
mkcert -cert-file ./certs/keycloak.pem -key-file ./certs/keycloak-key.pem keycloak localhost
```

## Running

After configuration, you can run the development environment:

```
docker-compose up -d
```

After which you can [create a user](https://localhost:8000) before [accessing
the gui](http://localhost:3000).

## Development

Playwright tests are included

```
make install_dependencies
make run_test
```
