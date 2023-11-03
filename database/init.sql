begin;

\set authenticator `echo $PGUSER`
\set authenticator_password `echo $PGPASSWORD`
\set web_anon `echo $PGRST_DB_ANON_ROLE`

create role :web_anon nologin;
create role web_user nologin;

create role :authenticator noinherit login password :'authenticator_password';
grant :web_anon to :authenticator;
grant web_user to :authenticator;

create schema insight;
grant usage on schema insight to web_user;

create table insight.files (
  id serial primary key,
  name text not null
);
grant all on insight.files to web_user;
grant usage, select on sequence insight.files_id_seq to web_user;

commit;
