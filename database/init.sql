begin;

\set pguser `echo $PGUSER`
\set pgpassword `echo $PGPASSWORD`
\set pgrst_db_anon_role `echo $PGRST_DB_ANON_ROLE`

create schema insight;

create role :pgrst_db_anon_role nologin;

create role :pguser noinherit login password :'pgpassword';
grant :pgrst_db_anon_role to :pguser;

create table insight.files (
  id serial primary key,
  name text not null
);

commit;
