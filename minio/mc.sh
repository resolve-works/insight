#!/bin/bash

mc alias set insight $MINIO_ENDPOINT $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

mc mb insight/insight

mc admin policy create insight external_user ./external_user.json
mc admin policy create insight internal_worker ./internal_worker.json
