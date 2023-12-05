begin;

\set pg_api_user `echo $PG_API_USER`
\set pg_api_password `echo $PG_API_PASSWORD`
\set pg_worker_user `echo $PG_WORKER_USER`
\set pg_worker_password `echo $PG_WORKER_PASSWORD`

create schema if not exists private;

create extension if not exists vector;
create extension if not exists plpython3u;

create role external_anonymous nologin;
create role external_user nologin;
create role internal_worker nologin;

create role :pg_api_user noinherit login password :'pg_api_password';
grant external_anonymous to :pg_api_user;
grant external_user to :pg_api_user;
grant internal_worker to :pg_api_user;

create role :pg_worker_user noinherit login password :'pg_worker_password';

\ir include/auth.sql
\ir include/pagestream.sql
\ir include/file.sql
\ir include/prompt.sql

create table private.data_page (
    id bigint not null,
    text character varying not null,
    metadata_ json,
    node_id character varying,
    embedding vector(1536)
);

create sequence private.data_page_id_seq start with 1 increment by 1 no minvalue no maxvalue cache 1;
alter sequence private.data_page_id_seq owned by private.data_page.id;
alter table private.data_page alter column id set default nextval('private.data_page_id_seq'::regclass);
alter table private.data_page add constraint data_page_pkey primary key (id);

grant usage on schema public to external_user;
grant usage on schema private to external_user;
grant usage on schema public to internal_worker;
grant usage on schema private to internal_worker;

grant usage on schema public to :pg_worker_user;
grant usage on schema private to :pg_worker_user;
grant all on all tables in schema private to :pg_worker_user;
grant usage, select on all sequences in schema private to :pg_worker_user;

commit;
