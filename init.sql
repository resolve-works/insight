
\set pg_postgrest_password `echo $PG_POSTGREST_PASSWORD`
\set pg_worker_password `echo $PG_WORKER_PASSWORD`

CREATE SCHEMA IF NOT EXISTS private;
CREATE EXTENSION IF NOT EXISTS vector;

-- Postgrest "authenticator" user that switches into different roles
CREATE ROLE insight_authenticator noinherit LOGIN PASSWORD :'pg_postgrest_password';

-- Postgrest anonymous user for unauthenticated requests
CREATE ROLE external_anonymous nologin;
GRANT external_anonymous TO insight_authenticator;
-- Postgrest JWT authenticated user
CREATE ROLE external_user nologin;
GRANT external_user TO insight_authenticator;
GRANT usage ON SCHEMA public TO external_user;
GRANT usage ON SCHEMA private TO external_user;

-- Internal worker processes
CREATE ROLE insight_worker noinherit LOGIN PASSWORD :'pg_worker_password';
GRANT usage ON SCHEMA public TO insight_worker;
GRANT usage ON SCHEMA private TO insight_worker;

-- Remove public access to functions as they are exposed by postgrest
ALTER DEFAULT privileges REVOKE EXECUTE ON functions FROM public;
