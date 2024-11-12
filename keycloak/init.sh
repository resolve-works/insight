#!/bin/bash

TRUSTSTORE=/opt/keycloak/conf/truststores/insight.jks
TRUSTPASS=insight

function kcadm() { 
    /opt/keycloak/bin/kcadm.sh $@ --truststore=$TRUSTSTORE --trustpass=$TRUSTPASS
}

# Create a java keystore from our CA cert
keytool -importcert \
    -trustcacerts \
    -file /opt/keycloak/conf/truststores/insight.pem \
    -keystore $TRUSTSTORE \
    -alias "keycloak" -storepass $TRUSTPASS -noprompt

# Server config
kcadm config credentials \
    --server $KEYCLOAK_SERVER \
    --realm master \
    --user $KEYCLOAK_ADMIN \
    --password $KEYCLOAK_ADMIN_PASSWORD

if kcadm get realms/insight | grep -q "default-roles-insight"; then
    echo "Keycloak already configured"
    exit 0
fi

# Create main insight realm, client and roles
# We manually disable HSTS as it breaks our localhost setup: https://github.com/keycloak/keycloak/issues/32366
kcadm create realms -f /opt/keycloak_init/realm-insight.json
kcadm create client-scopes -r insight -f /opt/keycloak_init/scope-insight-roles.json

INSIGHT_CID=$(kcadm create clients -r insight -f /opt/keycloak_init/client-insight.json -i)
kcadm create clients/$INSIGHT_CID/roles -r insight -s name=external_user

# Create rabbitmq client and roles
RABBITMQ_CID=$(kcadm create clients -r insight -f /opt/keycloak_init/client-rabbitmq.json -i)
kcadm create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.read:%2F/user*/*"
kcadm create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.configure:%2F/user*/*"
kcadm create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.write:%2F/user*/*"

# Add created roles as default to realm
kcadm add-roles -r insight \
  --rname default-roles-insight \
  --cclientid insight \
  --rolename "external_user"
kcadm add-roles -r insight \
  --rname default-roles-insight \
  --cclientid account \
  --rolename "view-groups"
kcadm add-roles -r insight \
  --rname default-roles-insight \
  --cclientid rabbitmq \
  --rolename "rabbitmq.read:%2F/user*/*" \
  --rolename "rabbitmq.configure:%2F/user*/*" \
  --rolename "rabbitmq.write:%2F/user*/*"

# Test user for manual testing
kcadm create users -r insight \
    -s username=john -s firstName=John -s lastName=Doe -s email="john@example.com" -s enabled=true
kcadm set-password -r insight --username john -p test

kcadm create users -r insight \
    -s username=jane -s firstName=Jane -s lastName=Doe -s email="jane@example.com" -s enabled=true
kcadm set-password -r insight --username jane -p test
