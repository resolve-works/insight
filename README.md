
# Insight

Insight turns data into information, by puttin it into context.

## What does it do?

Insight ingests PDF documents and indexes them. In this process, it tries to
strip away as much useless information as possbile. It does this by allowing
users to label pages. These labels are then used to predict labels for unlabeled
pages.


## Authentication

Authentication is handled through the use of Json Web Tokens (JWT). These tokens
can be provided by most oAuth providers. For example, to use
[Keycloak](https://www.keycloak.org/), you'd have to:

- Create a realm `insight`
- Create a client `insight_user` with device auth flow enabled
- Create a client `insight_worker` with service account flow enabled

You'll need to pass a Json Web Key (JWK) to Postgrest so it can decode the
tokens. You can get the key from your oAuth provider. For example, for a
keycloak provider:
```
curl https://secure.ftm.nl/realms/insight/protocol/openid-connect/certs | jq -r ".keys[0]" > ./.jwk
```
