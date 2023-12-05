
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
  create the roles: `external_user` and `internal_worker`.
- Edit the "Client Scope" `roles`, add a "User Client Role" mapper to it "by
  configuration". Name the mapper `insight roles`, select the `insight` client.
  Set `roles` for "Token Claim Name" and make sure "Multivalued" and "Add to
  access token" are enabled.
- Create a client `insight_worker` with service account flow enabled. Under this
  clients "Service account role" menu, assign `insight:internal_worker`.
- Under the realm settings, assign the `insight:external_user` and
  `account:view-groups` roles to the "Default roles" under "User registration".

When keycloak has been configured you should save the "client credentials" of the
`insight_worker` client to your `.env` file as `AUTH_CLIENT_SECRET`.

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

In this container you can run the `insight` tool.
