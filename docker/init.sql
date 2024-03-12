
\set pg_postgrest_user `echo $PG_POSTGREST_USER`
\set pg_postgrest_password `echo $PG_POSTGREST_PASSWORD`
\set pg_worker_user `echo $PG_WORKER_USER`
\set pg_worker_password `echo $PG_WORKER_PASSWORD`

CREATE SCHEMA IF NOT EXISTS private;
CREATE EXTENSION IF NOT EXISTS vector;

-- Postgrest "authenticator" user that switches into different roles
CREATE ROLE :pg_postgrest_user noinherit LOGIN PASSWORD :'pg_postgrest_password';

-- Postgrest anonymous user for unauthenticated requests
CREATE ROLE external_anonymous nologin;
GRANT external_anonymous TO :pg_postgrest_user;
-- Postgrest JWT authenticated user
CREATE ROLE external_user nologin;
GRANT external_user TO :pg_postgrest_user;

-- Internal worker processes
CREATE ROLE :pg_worker_user noinherit LOGIN PASSWORD :'pg_worker_password';
GRANT usage ON SCHEMA public TO :pg_worker_user;
GRANT usage ON SCHEMA private TO :pg_worker_user;
GRANT ALL PRIVILEGES ON ALL tables IN SCHEMA private TO :pg_worker_user;
GRANT ALL PRIVILEGES ON ALL tables IN SCHEMA public TO :pg_worker_user;
GRANT usage, SELECT ON ALL sequences IN SCHEMA private TO :pg_worker_user;

-- Remove public access to functions as they are exposed by postgrest
ALTER DEFAULT privileges REVOKE EXECUTE ON functions FROM public;

-- JWT authenticated user
GRANT usage ON SCHEMA public TO external_user;
GRANT usage ON SCHEMA private TO external_user;
GRANT usage, SELECT ON ALL sequences IN SCHEMA private TO external_user;

