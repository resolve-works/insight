BEGIN;
\set pg_api_user `echo $PG_API_USER`
\set pg_api_password `echo $PG_API_PASSWORD`
\set pg_worker_user `echo $PG_WORKER_USER`
\set pg_worker_password `echo $PG_WORKER_PASSWORD`
CREATE SCHEMA IF NOT EXISTS private;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS plpython3u;
ALTER DEFAULT privileges REVOKE EXECUTE ON functions FROM public;
CREATE ROLE external_anonymous nologin;
CREATE ROLE external_user nologin;
CREATE ROLE internal_worker nologin;
CREATE ROLE :pg_api_user noinherit LOGIN PASSWORD :'pg_api_password';
GRANT external_anonymous TO :pg_api_user;
GRANT external_user TO :pg_api_user;
GRANT internal_worker TO :pg_api_user;
CREATE ROLE :pg_worker_user noinherit LOGIN PASSWORD :'pg_worker_password';
\ir include/tables.sql
\ir include/views.sql
\ir include/functions.sql
\ir include/triggers.sql
GRANT usage ON SCHEMA public TO external_user;
GRANT usage ON SCHEMA private TO external_user;
GRANT usage ON SCHEMA public TO internal_worker;
GRANT usage ON SCHEMA private TO internal_worker;
GRANT usage ON SCHEMA public TO :pg_worker_user;
GRANT usage ON SCHEMA private TO :pg_worker_user;
GRANT ALL PRIVILEGES ON ALL tables IN SCHEMA private TO :pg_worker_user;
GRANT ALL PRIVILEGES ON ALL tables IN SCHEMA public TO :pg_worker_user;
GRANT usage, SELECT ON ALL sequences IN SCHEMA private TO :pg_worker_user;
COMMIT;

