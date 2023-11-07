
# Insight

Insight aims to turn data into information, by puttin it into context.


## Authentication

Authentication is handled through the use of Json Web Tokens (JWT). These tokens
can be provided by most oAuth providers. For example, to use
[Keycloak](https://www.keycloak.org/), you'd have to:

- Create a realm `insight`
- Create a client `insight-cli`
- Add the `web_user` as a realm role

You'll need to pass a Json Web Key (JWK) to Postgrest so it can decode the
tokens. You can get the key from your oAuth provider. For example, for a
keycloak provider:
```
curl https://secure.ftm.nl/realms/insight/protocol/openid-connect/certs | jq -r ".keys[0]" > ./.jwk
```
