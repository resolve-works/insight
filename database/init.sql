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

create table insight.upload (
    id uuid not null default gen_random_uuid(),
    name text not null,
    primary key (id)
);
grant all on insight.upload to web_user;

create table insight.file (
    id uuid not null default gen_random_uuid(),
    upload_id uuid not null,
    name text not null,

    primary key (id),
    foreign key(upload_id) references insight.upload (id) match simple on delete restrict not valid
);

grant all on insight.file to web_user;

commit;
