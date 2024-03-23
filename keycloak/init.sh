#!/bin/bash

# Server config
/opt/keycloak/bin/kcadm.sh config credentials \
    --server $KEYCLOAK_SERVER \
    --realm master \
    --user $KEYCLOAK_ADMIN \
    --password $KEYCLOAK_ADMIN_PASSWORD

if /opt/keycloak/bin/kcadm.sh get realms/insight | grep -q "default-roles-insight"; then
    echo "Keycloak already configured"
    exit 0
fi

# Create main insight realm, client and roles
/opt/keycloak/bin/kcadm.sh create realms -s realm=insight -s enabled=true
/opt/keycloak/bin/kcadm.sh create client-scopes -r insight -f /opt/keycloak_init/scope-insight-roles.json

INSIGHT_CID=$(/opt/keycloak/bin/kcadm.sh create clients -r insight -f /opt/keycloak_init/client-insight.json -i)
/opt/keycloak/bin/kcadm.sh create clients/$INSIGHT_CID/roles -r insight -s name=external_user

# Create rabbitmq client and roles
RABBITMQ_CID=$(/opt/keycloak/bin/kcadm.sh create clients -r insight -f /opt/keycloak_init/client-rabbitmq.json -i)
/opt/keycloak/bin/kcadm.sh create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.read:%2F/user-*/*"
/opt/keycloak/bin/kcadm.sh create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.configure:%2F/user-*/*"
/opt/keycloak/bin/kcadm.sh create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.write:%2F/user-*/*"
/opt/keycloak/bin/kcadm.sh create clients/$RABBITMQ_CID/roles -r insight -s name="rabbitmq.write:%2F/insight/*"

# Add created roles as default to realm
/opt/keycloak/bin/kcadm.sh create roles -r insight -f /opt/keycloak_init/role-insight-default.json
/opt/keycloak/bin/kcadm.sh update realms/insight -f /opt/keycloak_init/realm-insight.json
