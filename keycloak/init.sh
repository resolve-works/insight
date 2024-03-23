#!/bin/bash

/opt/keycloak/bin/kcadm.sh config credentials --server $KEYCLOAK_SERVER --realm master --user $KEYCLOAK_ADMIN --password $KEYCLOAK_ADMIN_PASSWORD

