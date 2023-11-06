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

create table insight.uploads (
    id uuid not null default gen_random_uuid(),
    name text not null,
    primary key (id)
);
grant all on insight.uploads to web_user;

create table insight.files (
    id uuid not null default gen_random_uuid(),
    upload_id uuid not null,
    name text not null,

    primary key (id),
    foreign key(upload_id) references insight.uploads (id) match simple on delete restrict not valid
);
grant all on insight.files to web_user;

commit;
