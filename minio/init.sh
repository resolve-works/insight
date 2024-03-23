#!/bin/bash

mc alias set insight $MINIO_ENDPOINT $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

mc mb -p insight/insight

# Create policies (role bindings / permissions)
mc admin policy create insight external_user ./external_user.json
mc admin policy create insight internal_worker ./internal_worker.json

# Create worker user for service account access
mc admin user add insight $MINIO_WORKER_USER $MINIO_WORKER_PASSWORD
# mc errors on re-attach
mc admin policy attach insight internal_worker --user $MINIO_WORKER_USER || true
