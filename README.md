
# Insight

Insight turns data into information, by putting it into context. It allows you
to search through a set of documents by keyword, and to prompt a
[LLM](https://en.wikipedia.org/wiki/Large_language_model) about sets documents
through the use of
[RAG](https://research.ibm.com/blog/retrieval-augmented-generation-RAG).

## Setting up

Insight makes use of a external authentication service and a external LLM
provider, we'll have to supply some configuration to make use of these.

First copy the provided `.env.sample` environment file to a `.env` file:
```
cp .env.sample .env
```

### Authentication

OpenID Connect is used as the authentication standard that all parts of insight
use to communicate. We use [Keycloak](https://www.keycloak.org/). If Keycloak
hasn't been configured yet:
- Create a realm `insight`.
- Create a client `insight` with device auth flow enabled. Under this client,
  create the role: `external_user`.
- Create a client `rabbitmq` with all flows disabled. Under this client, create
  the roles: `rabbitmq.read:*/*/*`, `rabbitmq.configure:*/*/*`
- Edit the "Client Scope" `roles`, add a "User Client Role" mapper to it "by
  configuration". Name the mapper `insight roles`, select the `insight` client.
  Set `roles` for "Token Claim Name" and make sure "Multivalued" and "Add to
  access token" are enabled.
- Edit the "Client Scope" `roles`, add a "User Client Role" mapper to it "by
  configuration". Name the mapper `rabbitmq roles`, select the `rabbitmq` client.
  Set `rabbitmq_roles` for "Token Claim Name" and make sure "Multivalued" and "Add to
  access token" are enabled.
- Under the realm settings, assign the following roles to the "Default roles"
  under "User registration": `insight:external_user`, `account:view-groups`,
  `rabbitmq:rabbitmq.read:*/*/*` and `rabbitmq:rabbitmq.configure:*/*/*`.

Insights services need to know about the certificates the auth provider uses to
validate the authentication tokens. To supply your `docker-compose` environment
with this token you can store it in a `.jwk` file:
```
curl https://secure.ftm.nl/realms/insight/protocol/openid-connect/certs | jq -r ".keys[0]" > ./.jwk
```

You'll also want to create a user for yourself in the `insight` realm.

### LLM configuration

You'll need to add a [OpenAI api key](https://platform.openai.com/api-keys) to
the `.env` file as `OPENAI_API_KEY`.


### Certificates

To encrypt traffic, we'll need some cerificates. In our development environment,
we will be using self-signed certificates. You can easily generate those with
[`mkcert`](https://github.com/FiloSottile/mkcert). Make sure the root CA is
installed and generate development certificates:
```
mkcert -install
mkdir certs
cp `mkcert -CAROOT`/rootCA.pem ./certs
mkcert -cert-file ./certs/opensearch.pem -key-file ./certs/opensearch-key.pem opensearch 
```

As requests can come from our browser, or from the containerized processes, we
can't use the `localhost` hostname, as that will resolve to container localhost
instead of our nginx gateway. To reach your local development setup, you'll need
the `insight` DNS name for your host.
```
mkcert -cert-file ./certs/insight.pem -key-file ./certs/insight-key.pem insight
chmod -R 644 ./certs/insight*
echo "127.0.0.1 insight" | sudo tee -a /etc/hosts
```


## Running

After configuration, you can run the development environment:
```
docker-compose up -d
```

To see what's going on you can `--follow` the logs:
```
docker-compose logs --follow
```

To stop the running services:
```
docker-compose down
```

While taking down the environment, you can also destroy the related data:
```
docker-compose down --volumes
```


## Using the CLI

The easiest way to use the CLI in your development environment is by using the
`cli` container:
```
docker-compose run cli
```

In this container you can run the `insight` tool. The `data` directory is
mounted in the container, which you can use to upload files.
